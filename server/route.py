from utils import log

user = {}


def route_static(request):
    filename = request.query.get('file', 'tu.png')
    path = 'static/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/png\r\n\r\n'
        response = header + f.read()
        log('响应', response)
        return response


def login(request):
    pass


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
}
