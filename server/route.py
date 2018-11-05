from utils import log
user = []


def route_static(request):
    filename = request.query.get('file', 'tu.png')
    path = 'static/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/png\r\n\r\n'
        response = header + f.read()
        log('响应', response)
        return response


def route_login(request):
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'
    body = template('login.html')
    if request.method == 'POST':
        f = request.form()
        if f in user:
            result = '登陆成功！<br> {}'.format(f)
            log('debug1', result)
        else:
            result = '登录失败'
    else:
        result = ''
    body = body.replace('{{result}}', result)
    response = header + body
    return response.encode(encoding='utf-8')


# 这里有个bug空格被默认成了 +
def route_register(request):
    header = 'HTTP/1.1 200 OK\r\nContent-Type\r\n\r\n'
    body = template('register.html')
    if request.method == 'POST':
        f = request.form()
        if len(f.get('username')) < 2 or len(f.get('password')) < 2:
            result = '用户或者密码的长度小于2'
        else:
            user.append(f)
            result = '注册成功！！<br> {}'.format(user)
    else:
        result = ''
    body = body.replace('{{result}}', result)
    response = header + body
    return response.encode(encoding='utf-8')


def template(name):
    path = 'templates/' + name
    with open(path, 'r', encoding=('utf-8')) as f:
        return f.read()


def route_index(request):
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = template('index.html')
    response = header + '\r\n' + body
    log('响应', response)
    return response.encode(encoding=('utf-8'))


route_dict = {
    '/': route_index,
    '/login': route_login,
    '/register': route_register,
}
