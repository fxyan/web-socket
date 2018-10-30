# 服务器
import socket

# 在服务器端host为空字符串，表示接受任意ip地址的连接
# 端口设置无所谓随便设置2000，要1024以上的1024以下的是系统保留的端口
host = ''
port = 2000

# socket实例
s = socket.socket()
# 用于绑定端口
s.bind((host, port))

# 用无限循环来处理请求因为服务器不能挂
while True:
    # 监听
    s.listen(5)
    # 当有连接的时候就会s.accept会返回两个值，分别是连接和客户端ip地址
    connection, address = s.accept()
    # 用来接收返回的数据
    # 参数是接收的字节数，返回值是一个bytes
    request = connection.recv(1024)

    print('ip {} request {}'.format(address, request.decode('utf-8')))

    response = b'HTTP/1.1 200 very ok\r\n\r\n<h1>hello world!</h1>'
    # 发送数据
    connection.sendall(response)
    # 关闭连接
    connection.close()
