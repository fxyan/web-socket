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
        self.cookie = ''

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

    def get_cookie(self):
        self.cookie = self.body.split('=')[1]


request = Request()


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


def error(request, code=404):
    e = {
        404: b'HTTP/1.1 400 NOT FOUND \r\n\r\n<h1>NOT FOUND</h1>'
    }
    return e.get(code, b'')


def response_for_path(path):
    log('分隔前的path', path)
    path, query = get_for_path(path)
    request.path = path
    request.query = query
    log('分割后的path {} query {}'.format(path, query))
    r = {
        '/static': route_static
    }
    r.update(route_dict)
    response = r.get(path, error)
    return response(request)


def run(host='', port=3000):
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
            if len(r.split()) < 2:
                continue
            path = r.split()[1]
            request.method = r.split()[0]
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


