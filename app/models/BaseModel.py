from peewee import *
from packages.connection import *

class BaseModel(Model):
    class Meta:
        database = db