# Views

A view is a Python function that takes a web request and returns a web response. This response can be anything really. The view itself contains whatever logic is necessary to return that response.

```py
def index(request):
    return text_response('Hello world')

def index(request):
    return json_response({'key' : 'Hello world'})

def index(request):
    return html_response('<h1>Hello world</h1>')
```