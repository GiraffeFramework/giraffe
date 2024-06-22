from .models import Model
from .fields import fields


class _Giraffe(Model):
    version = fields.String(max_length=10, min_length=1, name="version")