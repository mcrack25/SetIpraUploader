import os
import xmltodict
import json
from packages.dirs import Dirs
from app.adapters.SelectAdapter import SelectAdapter
from app.models.InvalidsTrudo import InvalidsTrudo
from app.models.InvalidsSocial import InvalidsSocial
from packages.config import Config

class SyncController:
    trudoDir = ''
    socialDir = ''

    def __init__(self):
        self.xmlsDir = Dirs().get('xmls')
        self.trudoDir = os.path.join(self.xmlsDir, 'trudo')
        self.socialDir = os.path.join(self.xmlsDir, 'social')

    def getData(self, type, fileXml):
        dir = None
        if type == 'social':
            dir = self.socialDir
        elif type == 'trudo':
            dir = self.trudoDir
        else:
            exit('Не верная папка!!!')

        filePath = os.path.join(dir, fileXml)

        # Открываем файл, присваиваем значение переменной и закрываем файл
        xmlContent = dict()
        with open(filePath, "r", encoding='utf-8') as fileOpen:
            xmlContent = xmltodict.parse(fileOpen.read())
        fileOpen.close()

        # Пропускаем данные XML через Адаптер-преобразователь
        return SelectAdapter(xmlContent, fileXml).getData()

    def validate(self, raw):
        data = ''
        return data

    def trudoSend(self):
        type = 'trudo'
        dir = self.trudoDir
        data = self.dataGet(type, dir)
        self.sendToDb(type, data)

    def socialSend(self):
        type = 'social'
        dir = self.socialDir
        data = self.dataGet(type, dir)
        self.sendToDb(type, data)

    def sendToDb(self, type, data):
        invalidsModel = None
        if (type == 'trudo'):
            invalidsModel = InvalidsTrudo
        elif (type == 'social'):
            invalidsModel = InvalidsSocial
        else:
            print('Ошибка!!! Не возможно загрузить данные в базу!!!')
            exit()

        dbType = Config('database').get('dbType')
        if (dbType == 'mysql' or dbType =='sqlite'):
            for item in data:
                if not (item['mseid'] == None):
                    result = (invalidsModel.insert(
                        mseid=item['mseid'],
                        buro_full_name=item['buro_full_name'],
                        fio=item['fio'],
                        lname=item['lname'],
                        fname=item['fname'],
                        sname=item['sname'],
                        disability_group=item['disability_group_value'],
                        disability_cause=item['disability_cause_value'],
                        disability_end_date=item['disability_end_date'],
                        doc_title=item['doc_title'],
                        doc_series=item['doc_series'],
                        doc_number=item['doc_number'],
                        doc_issuer=item['doc_issuer'],
                        doc_issuedate=item['doc_issuedate'],
                        phones=item['phones'],
                        isfirst=item['isfirst'],
                        enddate=item['enddate'],
                        snils=item['snils'],
                        gndr=item['gndr'],
                        dt=item['dt'],
                        bdate=item['bdate'],
                        oivid=item['recipient_type_id'],
                        docnum=item['docnum'],
                        docdt=item['docdt'],
                        okr_id=item['okr_id'],
                        nreg=item['nreg'],
                        prg=item['prg'],
                        prgnum=item['prgnum'],
                        prgdt=item['prgdt'],
                        citizenship_id=item['citizenship_id'],
                        groupinv_id=item['disability_group_id'],
                        prichinv_id=item['disability_cause_id'],
                        reqirehelp_ids=item['reqirehelp_ids'],
                        specializburo_id=item['specializburo_id'],
                        address_jitelstva=item['living_address'],
                        address_registracii=item['reg_address'],
                        address_search=item['address_search']
                    ).on_conflict('replace').execute())
        elif (dbType == 'postgres'):
            # Works with Postgresql (which supports ON CONFLICT ... UPDATE).
            result = (invalidsModel.insert(
                mseid='123',
                fio='bar',
                address_search='125'
            ).on_conflict(conflict_target=(invalidsModel.mseid,),preserve=(invalidsModel.mseid),update={invalidsModel.fio: 'abc'}).execute())

            print(result)

    def dataGet(self, type, dirXmls):
        data_all = []
        for fileXml in os.listdir(dirXmls):
            if fileXml.endswith('.xml'):
                data = self.getData(type, fileXml)

                mseid = data['MseId']
                buro = data['Buro']
                buro_full_name = buro['FullName']
                specializburo_id = buro['Number']

                # Person **************************
                person = data['Person']

                # Person FIO
                fio = person['FIO']

                lname = ''
                if (fio['LastName']):
                    lname = fio['LastName'].lower().strip()
                    lname = lname.title()

                fname = ''
                if (fio['FirstName']):
                    fname = fio['FirstName'].lower().strip()
                    fname = fname.title()

                sname = ''
                if (fio['SecondName']):
                    sname = fio['SecondName'].lower().strip()
                    sname = sname.title()

                fio = ' '.join([lname, fname, sname])

                # Person IdentityDoc
                doc_title = None
                doc_series = None
                doc_number = None
                doc_issuer = None
                doc_issuedate = None
                identity_doc = person['IdentityDoc']
                if (identity_doc['Title']):
                    doc_title = identity_doc['Title']

                if (identity_doc['Series']):
                    doc_series = identity_doc['Series']

                if (identity_doc['Number']):
                    doc_number = identity_doc['Number']

                if (identity_doc['Issuer']):
                    doc_issuer = identity_doc['Issuer']

                if (identity_doc['IssueDate']):
                    doc_issuedate = identity_doc['IssueDate']

                # Person Phones
                phones = None
                phonesMass = person['Phones']
                if(phonesMass):
                   phones = json.dumps(phonesMass)

                snils = person['SNILS']
                gndr = person['IsMale']
                bdate = person['BirthDate']

                PersonCitizenship = person['Citizenship']
                citizenship_id = PersonCitizenship['Id']

                disability_group = data['DisabilityGroup']
                disability_group_value = disability_group['Value']
                disability_group_id = disability_group['Id']

                disability_cause = data['DisabilityCause']
                disability_cause_value = disability_cause['Value']
                disability_cause_id = disability_cause['Id']

                disability_end_date = data['DisabilityEndDate']
                isfirst = data['IsFirst']
                enddate = data['EndDate']
                dt = data['DevelopDate']
                recipient = data['Recipient']
                recipient_type_id = recipient['Id']
                docnum = data['ProtocolNum']
                docdt = data['ProtocolDate']
                prgnum = data['Number']

                okr_id = data['okr_id']
                nreg = data['nreg']
                prg = data['prg']
                prgdt = data['IssueDate']

                reqirehelp = data['RequiredHelp']
                reqirehelp_ids = None
                if (reqirehelp):
                    helps = []
                    for help in reqirehelp:
                        for help_one in help:
                            helps.append(help_one['Id'])
                    reqirehelp_ids = json.dumps(helps)

                address_search = None
                reg_address = person['RegAddress']
                living_address = person['LivingAddress']

                if (reg_address):
                    address_search = reg_address
                if (living_address):
                    address_search = living_address

                data_one = dict({
                    "mseid":mseid,
                    "buro_full_name":buro_full_name,
                    "fio":fio,
                    "lname":lname,
                    "fname":fname,
                    "sname":sname,
                    "disability_group_value":disability_group_value,
                    "disability_cause_value":disability_cause_value,
                    "disability_end_date":disability_end_date,
                    "doc_title":doc_title,
                    "doc_series":doc_series,
                    "doc_number":doc_number,
                    "doc_issuer":doc_issuer,
                    "doc_issuedate":doc_issuedate,
                    "phones":phones,
                    "isfirst":isfirst,
                    "enddate":enddate,
                    "snils": snils,
                    "gndr": gndr,
                    "dt": dt,
                    "bdate": bdate,
                    "recipient_type_id": recipient_type_id,
                    "docnum": docnum,
                    "docdt": docdt,
                    "okr_id": okr_id,
                    "nreg": nreg,
                    "prg": prg,
                    "prgnum": prgnum,
                    "prgdt": prgdt,
                    "citizenship_id": citizenship_id,
                    "disability_group_id": disability_group_id,
                    "disability_cause_id": disability_cause_id,
                    "reqirehelp_ids": reqirehelp_ids,
                    "specializburo_id": specializburo_id,
                    "living_address": living_address,
                    "reg_address": reg_address,
                    "address_search": address_search
                })
                data_all.append(data_one)
        return data_all