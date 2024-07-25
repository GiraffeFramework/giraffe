# Getting started

To get started with a simple Giraffe project make a Python file named as you like.

```py
# app.py
from giraffe import Giraffe, Routes, html_respones

app = Giraffe(__name__)
routes = Routes()

@routes.get('/')
def index(request):
    return html_response(request, '<h1 style="text-align: center;">Hello world!</h1>')

app.add_routes(routes)

if __name__ == '__main__':
    app.start()

```

If you want to make a more complex Giraffe project, follow [this](/docs/projects/getting_started.md) guide.