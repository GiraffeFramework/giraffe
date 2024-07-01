from .models import Model
from .fields import fields


class Migration(Model):
    __tablename__ = "migrations"

    id = fields.Integer(primary_key=True, name="id")
    name = fields.String(max_length=10, min_length=1, name="name")
    applied_at = fields.Date(name="applied_at")
