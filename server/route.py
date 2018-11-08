from utils import log
import random
# 没有使用数据库所以暂时将数据存在这里每个重启都会刷新数据  只是学习用框架
user = []
session = {}


# 重定向函数
def redirect(url):
    r = {
        'Location': url
    }
    header = response_for_header(r, 302)
    return header


# 处理HTTP header
def response_for_header(headers, code=200):
    header = 'HTTP/1.1 {} OK\r\n'.format(code)
    header += ''.join(['{}: {}\r\n'.format(k, v) for k, v in headers.items()])
    return header


# 产生随机字符串用于session
def random_str():
    s = ''
    seed = 'fhehfejajkveuuhfeoiwf238u894y738hgf873ifh98'
    for i in range(16):
        random_index = random.randint(0, len(seed)-1)
        s += seed[random_index]
    return s


# 判断登录用户用户名返给模板
def current_user(request):
    # 使用session
    session_id = request.cookies.get('user', '')
    username = session.get(session_id, '【游客】')
    log('username', username)
    return username


# 判断注册用户的的账号和密码格式是否正确
def validate_register(user):
    if len(user.get('username')) < 2 or len(user.get('password')) < 2:
        return False
    else:
        return True


# 返回HTML模板
def template(name):
    path = 'templates/' + name
    with open(path, 'r', encoding=('utf-8')) as f:
        return f.read()


# 读取静态文件 比如图片
def route_static(request):
    filename = request.query.get('file', 'tu.png')
    path = 'static/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/png\r\n\r\n'
        response = header + f.read()
        log('响应', response)
        return response


# 主页函数
def route_index(request):
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = template('index.html')
    response = header + '\r\n' + body
    log('响应', response)
    return response.encode(encoding=('utf-8'))


# 登录页面
def route_login(request):
    header = {
        'Content-Type': 'text/html'
    }
    body = template('login.html')
    # 拿到用户名
    username = current_user(request)
    if request.method == 'POST':
        # 得到body传输的数据
        f = request.form()
        if f in user:
            # 随机生成session值
            session_id = random_str()
            # 储存session
            session[session_id] = f.get('username')
            result = '登陆成功！'
            header['Set-cookie'] = 'user={}'.format(session_id)
        else:
            result = '登录失败'
    else:
        result = ''
    # 模板渲染
    body = body.replace('{{result}}', result)
    header = response_for_header(header)
    body = body.replace('{{user}}', username)
    response = header + '\r\n' + body
    log('login的响应', response)
    return response.encode(encoding='utf-8')


# 注册页面 这里有个bug空格被默认成了 +
def route_register(request):
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'
    body = template('register.html')
    if request.method == 'POST':
        # 得到body
        use = request.form()
        # 判断注册格式
        if validate_register(use):
            user.append(use)
            result = '注册成功！！<br> {}'.format(user)
        else:
            result = '用户或者密码的长度小于2'
    else:
        result = ''
    body = body.replace('{{result}}', result)
    response = header + body
    return response.encode(encoding='utf-8')


# 路由字典
route_dict = {
    '/': route_index,
    '/login': route_login,
    '/register': route_register,
}
