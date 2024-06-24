from .models import Model
from .fields import fields


class _Migration(Model):
    __tablename__ = "migrations"

    name = fields.String(max_length=10, min_length=1, name="name")
    applied_at = fields.Date(name="applied_at")