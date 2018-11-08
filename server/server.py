import socket
from utils import log
from route import route_static
from route import route_dict
import urllib.parse


class Request(object):
    def __init__(self):
        self.method = 'GET'
        self.path = ''
        self.query = {}
        self.body = ''
        self.header = {}
        self.cookies = {}

    # 增加cookie
    def add_cookie(self):
        cookies = self.header.get('Cookie', '')
        log('切片前的cookies', cookies)
        # 按照cookie的分隔符进行切片
        kvs = cookies.split('; ')
        for i in kvs:
            if '=' in i:
                k, v = i.split('=')
                self.cookies[k] = v

    # 从请求中得到HTTP header
    def add_header(self, header):
        log('headers', header)
        lines = header
        # 按照header的标识进行切片
        for line in lines:
            k, v = line.split(': ', 1)
            self.header[k] = v
        #     清空cookie
        self.cookies = {}
        self.add_cookie()
        log('cookie', self.cookies)

    # 将POST请求得到的body解析成字典方便使用
    def form(self):
        f = {}
        args = self.body.split('&')
        for arg in args:
            k, v = arg.split('=')
            # 这个是socket编程的编码转换
            # 网页默认会将&这类的敏感符号转义
            # urllib.parse.unquote函数可以将字符串转义成原始字符串
            k = urllib.parse.unquote(k)
            v = urllib.parse.unquote(v)
            f[k] = v
        return f


request = Request()


# 解析host 分离path 和 query
def get_for_path(path):
    # 首先通过？确定是否有query
    index = path.find('?')
    if index == -1:
        return path, {}
    else:
        # 分隔path和query
        path, query_string= path.split('?', 1)
        log('query', query_string)
        # 通过 & 分隔query
        args = query_string.split('&')
        query = {}
        # 组成字典
        for arg in args:
            k, v = arg.split('=')
            query[k] = v
        return path, query


# 返回404报错
def error(request, code=404):
    e = {
        404: b'HTTP/1.1 400 NOT FOUND \r\n\r\n<h1>NOT FOUND</h1>'
    }
    return e.get(code, b'')


# 路由中转函数从这里判断路由到底应该转到哪个函数进行处理
def response_for_path(path):
    log('分隔前的path', path)
    # 返回path 和 query并记录
    path, query = get_for_path(path)
    request.path = path
    request.query = query
    log('分割后的path {} query {}'.format(path, query))
    r = {
        '/static': route_static
    }
    # 这里更新了路由字典使得程序可以更加松散
    r.update(route_dict)
    response = r.get(path, error)
    return response(request)


# 启动函数
def run(host='', port=3000):
    # socket连接
    with socket.socket() as s:
        s.bind((host, port))
        while True:
            s.listen(5)
            # 获取连接和本机地址
            connection, address = s.accept()
            log('address', address)
            # 接收请求
            r = connection.recv(1024)
            # 转成str方便输出
            log('原始请求', r)
            r = r.decode('utf-8')
            # 输出请求
            log('http request', r)
            # 有时候谷歌浏览器会出现bug
            if len(r.split()) < 2:
                continue
            # 根据HTTP协议的格式分隔出我们想要的所有数据
            path = r.split()[1]
            request.method = r.split()[0]
            request.add_header(r.split('\r\n\r\n')[0].split('\r\n')[1:])
            request.body = r.split('\r\n\r\n')[1]
            log('path {}, method {}, body {}'.format(path, request.method, request.body))
            # 根据path返回响应
            r = response_for_path(path)
            connection.sendall(r)
            connection.close()


def main():
    config = dict(
        host='',
        port=3000,
    )
    run(**config)


if __name__ == '__main__':
    main()


