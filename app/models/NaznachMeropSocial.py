import datetime
from peewee import *
from app.models.BaseModel import BaseModel

class NaznachMeropSocial(BaseModel):
    mseid = CharField(max_length=255)
    xml_merop_id = IntegerField()
    xml_merop_name = CharField(max_length=255)
    xml_period_from = DateField(null=True)
    xml_period_to = DateField(null=True)
    xml_need = IntegerField(null=True)
    xml_executor = CharField(max_length=255, null=True)

    created_at = DateTimeField(default=datetime.datetime.now())
    updated_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        db_table = "naznach_merop_socials"
        order_by = ('created_at')