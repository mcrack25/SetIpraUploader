import datetime
from peewee import *
from app.models.BaseModel import BaseModel

class InvalidsTrudo(BaseModel):
    mseid = CharField(max_length=255, unique=True)
    buro_full_name = TextField(null=True)
    disability_group = TextField(null=True)
    disability_cause = TextField(null=True)
    disability_end_date = DateField(null=True)
    send = IntegerField(null=True)
    fio = TextField()
    address_search = TextField(null=True)
    address_jitelstva = TextField(null=True)
    address_registracii = TextField(null=True)
    doc_title = CharField(null=True)
    doc_series = CharField(max_length=100, null=True)
    doc_number = CharField(max_length=100, null=True)
    doc_issuer = TextField(null=True)
    doc_issuedate = DateField(null=True)
    phones = CharField(null=True)
    isfirst = SmallIntegerField(null=True)
    enddate = DateField(null=True)
    okr_id = SmallIntegerField(null=True)
    nreg = SmallIntegerField(null=True)
    dt = DateField(null=True)
    snils = CharField(max_length=15, null=True)
    lname = CharField(max_length=30, null=True)
    fname = CharField(max_length=30, null=True)
    sname = CharField(max_length=30, null=True)
    bdate = DateField(null=True)
    gndr = SmallIntegerField(null=True)
    oivid = IntegerField(null=True)
    docnum = CharField(max_length=20, null=True)
    docdt = CharField(null=True)
    prg = SmallIntegerField(null=True)
    prgnum = CharField(max_length=20, null=True)
    prgdt = DateField(null=True)

    # Справочники
    citizenship_id = IntegerField(null=True)
    groupinv_id = IntegerField(null=True)
    prichinv_id = IntegerField(null=True)
    prognozresult_ids = CharField(max_length=64, null=True)
    reqirehelp_ids = CharField(max_length=64, null=True)
    specializburo_id = IntegerField(null=True)

    closed = SmallIntegerField(null=True)
    created_at = DateTimeField(default=datetime.datetime.now())
    updated_at = DateTimeField(default=datetime.datetime.now())
    #updated_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        db_table = "invalids_trudos"
        order_by = ('created_at')