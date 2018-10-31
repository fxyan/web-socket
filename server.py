import socket


# 主页函数
def route_index():
    header = 'HTTP/1.1 200 ok\r\nContent-Type: text/html\r\n'
    body = '<img src="/tu2.png"><img src="/tu1.jpg"><img src="/tu3.jpg">'
    response = header + '\r\n' + body
    return response.encode(encoding='utf-8')


# 下面是返回三张图片的函数
def route_img():
    with open('tu2.png', 'rb')as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/png\r\n'
        img = header + b'\r\n' + f.read()
        return img


def route_img_1():
    with open('tu1.jpg', 'rb')as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/jpg\r\n'
        img = header + b'\r\n' + f.read()
        return img


def route_img_3():
    with open('tu3.jpg', 'rb')as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/png\r\n'
        img = header + b'\r\n' + f.read()
        return img


# 返回错误页面
def error():
    header = 'HTTP/1.1 404\r\n'
    body = '<h1>NOT FOUND</h1>'
    response = header + '\r\n' + body
    return response.encode(encoding=('utf-8'))


# 路径处理函数
def get_for_path(path):
    r = {
        '/': route_index,
        '/tu1.jpg': route_img_1,
        '/tu2.png': route_img,
        '/tu3.jpg': route_img_3,
    }
    response = r.get(path, error)
    return response()


def run(host='', port=3000):
    # 使用with来简介的关闭文件
    with socket.socket() as s:
        # 绑定地址和端口
        s.bind((host, port))
        while True:
            s.listen(5)
            # 返回地址和端口
            connection, address = s.accept()
            # 接收请求数据
            request = connection.recv(1024)
            print('ip:', address)
            # 转换成bytes类型
            request = request.decode('utf-8')
            print('http request:', request)
            try:
                # 从url中分离出路径
                path = request.split()[1]
                print('path', path)
                # 返回给路径处理函数
                response = get_for_path(path)
                # 发送数据
                connection.sendall(response)
            except Exception as e:
                print('error', e)
            connection.close()


def main():
    config = dict(
        host='',
        port=3000
    )
    run(**config)


if __name__ == '__main__':
    main()

