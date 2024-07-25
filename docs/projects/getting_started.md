# Getting started with a Giraffe project

First you will have to run `giraffe create {project_name}`. This will add the following files to your directory:

```swift
- project_name/
    - __init__.py
    - config.py
- wsgi.py
```

Your root project is __not__ intended to hold any views. Instead, views must be added in a Giraffe app. To create a giraffe app, run `giraffe add {app_name}`. This will add the following files to your directory:

```swift
- app_name/
    - __init__.py
    - models.py
    - views.py
- project_name/
    - __init__.py
    - config.py
```

See your project folder as your utils or commons file. An app can be interpretated as a functionality of your application. Example apps could be `auth`, `basket`, `checkout`, `products`, etc...
Add your routes in `project_name/__init__.py` for them to work.
