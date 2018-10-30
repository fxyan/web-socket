# 客户端
import socket

# socket.AF_INET代表IPv4协议
# socket.SOCK_STREAM代表TCP协议
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 上面的两个值是默认参数，所以使用下面的语句也可以
# s = socket.socket
# 下面是https的写法
# s = ssl.wrap_socket(socket.socket)

# 主机和端口
host = 'daily.zhihu.com'
port = 80

# 连接主机
s.connect((host, port))

# 获取本机的IP和端口
ip, port = s.getsockname()
print('本机的IP{} 和端口{}'.format(ip, port))

# 构造HTTP请求
http_request = 'GET / HTTP/1.1\r\nhost:{}\r\n\r\n'.format(host)
# 使用send函数将请求发送出去，send函数只接受bytes类型的编码，
# 使用encode将str转换成bytes类型，编码为utf-8
request = http_request.encode('utf-8')
print('请求', request)
s.send(request)

# 接收服务器的响应数据
# 我设定参数长度为1024，超过范围的就不接收了
response = s.recv(1024)

print('响应', response)
print('响应的 str 格式', response.decode('utf-8'))

