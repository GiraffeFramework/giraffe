# Create command

For any feature or application of your web app we recommend initiating a new Giraffe app. This can be done through the command line, or you can chose to create the necessary files manually (not recommended).

```bash
giraffe add {name}
```

Add a Giraffe app

```swift
// required
- wsgi.py
- project_name/
  - __init__.py
  - config.py
// newly added
- app_name/
  - __init__.py
  - models.py
  - views.py
```

If you intend on adding views to this app, don't forget to [register your Routes]().
