from datetime import datetime
from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import (
    DateTimeField, StringField, IntField, ListField
)

class NAVs(Document):
    meta = {'collection': 'data'}
    nav = StringField()
    scheme_code = IntField()
    date = DateTimeField()

class Schemes(Document):
    x = type
    meta = {'collection': 'meta'}
    name = StringField()
    fund_type = StringField()
    scheme_code = IntField()
    amc = StringField()
    categories = ListField(StringField())
