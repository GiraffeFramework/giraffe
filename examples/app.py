from giraffe.core.html import make_html
from giraffe.core.responses import text_response, json_response, html_response
from giraffe.core.routes import Routes
from giraffe import Giraffe

app = Giraffe(__name__)
routes = Routes()


@routes.route('/')
def text(request):
    return text_response(request, 'hello world', 200)


@routes.route('/json')
def json(request):
    return json_response(request, {'hello' : 'world'}, 200)


@routes.route('/html/<param>')
def html(request, param):
    return html_response(request, make_html(f'<h1 style="text-align: center;">{param}</h1>'), 200)


@routes.get('/get')
def get(request):
    return text_response(request, 'easier method to declare endpoint types', 200)


app.add_routes(routes)


if __name__ == '__main__':
    app.start()
