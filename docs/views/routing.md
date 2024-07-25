# URLs

To map your existing endpoints to their corresponding URLs you will have to add routes.

Initiate a `Routes()` object. You can define a prefix that will be added to all routes.

```py
routes = Routes()

# Prepend all routes registered to 'routes' with '/auth/user'
routes = Routes(prefix='/auth/user')
```

Now you can use the `route()` or `get()`, `post()`, `put()`, `,patch` and `delete()` decorators on the `Routes()` object to add new routes.
When using the `routes()` decorator you can also provide request methods using `methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE']`, this defaults to `get` only.

```py
@routes.route('')
def user(request):
    return text_response(request, 'hello')

@routes.get('/get')
def get_user(request):
    return text_response(request, 'hello')

@routes.post('/post')
def post_user(request):
    return text_response(request, 'hello')

# ...
```