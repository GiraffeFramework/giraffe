from ..giraffe.core.responses import response, json_response, html_response, make_html
from ..giraffe.core.routes import Routes
from ..giraffe import Giraffe

app = Giraffe(__name__)

routes = Routes()

app.add_routes(routes)

@routes.route('/')
def text(request):
    return response(request, 'hello world', 200)


@routes.route('/json')
def json(request):
    return json_response(request, {'hello' : 'world'}, 200)


@routes.route('/html')
def html(request):
    return html_response(request, make_html('<h1>hello world</h1>'), 200)


if __name__ == '__main__':
    app.start()
