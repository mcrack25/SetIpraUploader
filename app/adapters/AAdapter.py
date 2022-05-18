import datetime
import re
from packages.config import Config

class AAdapter:
    oldData = dict()
    newData = dict()
    maskDate = '\d{4}-\d\d-\d\d'
    # maskDate = '^\d{4}-\d\d-\d\d$'
    okr_id = 0
    nreg = 0
    prg = 0

    def __init__(self, data):
        self.oldData = data
        self.okr_id = Config().get('okr_id')
        self.nreg = Config().get('nreg')
        self.prg = Config().get('prg')

    # Обрезаем строку на определённое количество символов
    def _halfString(self, string, count):
        if (len(string) > count):
            string = string[0:count - 1]
        return string

    def getData(self):
        root = self.getRoot(self.oldData)
        mseid = self.getMseId(root)
        buro = self.getBuro(root)
        recipient = self.getRecipient(root)
        number = self.getNumber(root)
        isFirst = self.getIsFirst(root)
        endDate = self.getEndDate(root)
        issueDate = self.getIssueDate(root)
        person = self.getPerson(root)
        profSection = self.getProfSection(root)
        socSection = self.getSocSection(root)
        disabilityGroup = self.getDisabilityGroup(root)
        disabilityCause = self.getDisabilityCause(root)
        disabilityEndDate = self.getDisabilityEndDate(root)
        dt = self.getDevelopDate(root)
        docnum = self.getProtocolNum(root)
        docdt = self.getProtocolDate(root)
        requiredHelp = self.getRequiredHelp(root)
        configDate = self.getConfigDate()


        newRoot = dict()
        newRoot.update(configDate)
        newRoot.update(mseid)
        newRoot.update(buro)
        newRoot.update(recipient)
        newRoot.update(number)
        newRoot.update(isFirst)
        newRoot.update(endDate)
        newRoot.update(issueDate)
        newRoot.update(disabilityGroup)
        newRoot.update(disabilityCause)
        newRoot.update(disabilityEndDate)
        newRoot.update(dt)
        newRoot.update(docnum)
        newRoot.update(docdt)
        newRoot.update(requiredHelp)

        newRoot.update(person)
        newRoot.update(profSection)
        newRoot.update(socSection)

        self.newData = newRoot

        return self.newData

    def setRoot(self, data):
        self.newData.update({'tIPRA': data})

    def getRoot(self, root):
        return root['tIPRA']

    def getMseId(self, root):
        mseid = None
        mseid_raw = root['MseId'].strip()
        if not (mseid_raw == None):
            mseid = mseid_raw
        return dict({'MseId': mseid})

    def getProtocolNum(self, root):
        docnum = root['ProtocolNum']
        docnum = docnum.strip()
        docnum = docnum.replace(' ', '')
        return dict({'ProtocolNum': docnum})

    def getProtocolDate(self, root):
        docdt = None
        docdt_raw = root['ProtocolDate']

        # Проверяем, соответствует ли дата маске
        try:
            reg_ok = re.match(self.maskDate, docdt_raw)
        except:
            reg_ok = False

        if (reg_ok != False):
            if not (docdt_raw == '0001-01-01'):
                docdt = datetime.datetime.strptime(docdt_raw, "%Y-%m-%d").date()

        return dict({'ProtocolDate': docdt})

    def getBuro(self, root):
        buro = root['Buro']
        short_name = buro['ShortName']
        full_name = buro['FullName']
        number = buro['Number']
        org_name = buro['OrgName']
        id = buro['Id']
        buro_mass = dict()
        buro_mass.update({'ShortName':short_name,'FullName':full_name,'Number':number,'OrgName':org_name,'Id':id})
        return dict({'Buro':buro_mass})

    def getRecipient(self, root):
        recipient = root['Recipient']
        recipient_type = recipient['RecipientType']

        name = recipient['Name']
        address = recipient['Address']
        id = recipient_type['Id']
        value = recipient_type['Value']

        recipient_mass = dict()
        recipient_mass.update({'Name': name,'Address': address,'Id': id,'Value': value})
        return dict({'Recipient': recipient_mass})

    def getNumber(self, root):
        try:
            prgnum = root['Number'].strip()
            prgnum = self._halfString(prgnum,20)
        except:
            prgnum = None
        return dict({'Number': prgnum})

    def getDevelopDate(self, root):
        dt = None
        dt_raw = root['DevelopDate']

        # Проверяем, соответствует ли дата маске
        try:
            reg_ok = re.match(self.maskDate, dt_raw)
        except:
            reg_ok = False

        if (reg_ok != False):
            if not (dt_raw == '0001-01-01'):
                dt = datetime.datetime.strptime(dt_raw, "%Y-%m-%d").date()

        return dict({'DevelopDate': dt})

    def getEndDate(self, root):
        end_date = None
        end_date_raw = root['EndDate']

        # Проверяем, соответствует ли дата маске
        try:
            reg_ok = re.match(self.maskDate, end_date_raw)
        except:
            reg_ok = False

        if (reg_ok != False):
            if not (end_date_raw == '0001-01-01'):
                end_date = datetime.datetime.strptime(end_date_raw, "%Y-%m-%d").date()

        return dict({'EndDate': end_date})

    def getIssueDate(self, root):
        issue_date = None
        issue_date_raw = root['IssueDate']

        # Проверяем, соответствует ли дата маске
        try:
            reg_ok = re.match(self.maskDate, issue_date_raw)
        except:
            reg_ok = False

        if (reg_ok != False):
            if not (issue_date_raw == '0001-01-01'):
                issue_date = datetime.datetime.strptime(issue_date_raw, "%Y-%m-%d").date()

        return dict({'IssueDate': issue_date})

    def getIsFirst(self, root):
        is_first = 0
        if 'IsFirst' in root:
            if (root['IsFirst'].lower() == 'true'):
                is_first = 1
        return dict({'IsFirst': is_first})

    def getPerson(self, root):
        person = root['Person']
        fio = self.getFIO(person)
        id = self.getPersonId(person)
        age = self.getPersonAge(person)
        citizenship = self.getPersonCitizenship(person)
        snils = self.getSnils(person)
        birthDate = self.getBirthDate(person)
        livingAddress = self.getLivingAddress(person)
        regAddress = self.getRegAddress(person)
        phones = self.getPhones(person)
        identityDoc = self.getIdentityDoc(person)
        isMale = self.getIsMale(person)
        primaryProfession = self.getPrimaryProfession(person)
        primaryProfessionExperience = self.getPrimaryProfessionExperience(person)
        qualification = self.getQualification(person)
        currentJob = self.getCurrentJob(person)
        employmentOrientationExists = self.getEmploymentOrientationExists(person)
        isRegisteredInEmploymentService = self.getIsRegisteredInEmploymentService(person)

        personContent = dict()
        personContent.update(id)
        personContent.update(fio)
        personContent.update(age)
        personContent.update(citizenship)
        personContent.update(snils)
        personContent.update(birthDate)
        personContent.update(livingAddress)
        personContent.update(regAddress)
        personContent.update(phones)
        personContent.update(identityDoc)
        personContent.update(isMale)
        personContent.update(primaryProfessionExperience)
        personContent.update(qualification)
        personContent.update(currentJob)
        personContent.update(employmentOrientationExists)
        personContent.update(isRegisteredInEmploymentService)
        personContent.update(livingAddress)

        return dict({'Person': personContent})

    def getConfigDate(self):
        okr_id = self.okr_id
        nreg = self.nreg
        prg = self.prg

        return dict({'okr_id': okr_id, 'nreg': nreg, 'prg': prg})

    def getFIO(self, person):
        Fio = person['FIO']

        firstName = Fio['FirstName']
        lastName = Fio['LastName']
        secondName = Fio['SecondName']

        fio = dict()
        fio.update({'FirstName': firstName,'LastName': lastName,'SecondName': secondName})

        return dict({'FIO':fio})

    def getLivingAddress(self, person):
        try:
            address = person['LivingAddress']
            address_value = address['Value'].strip()
        except:
            address_value = None

        return dict({'LivingAddress': address_value})

    def getRegAddress(self, person):
        try:
            address = person['RegAddress']
            address_value = address['Value'].strip()
        except:
            address_value = None
        return dict({'RegAddress': address_value})

    def getPersonId(self, person):
        id = person['Id']
        if not (id):
            id = None
        return dict({'Id': id})

    def getPersonAge(self, person):
        years = None
        ages = person['Age']
        if (ages):
            years = int(ages['Years'])
        return dict({'Age': {'Years': years}})

    def getPersonCitizenship(self, person):
        citizenshipId = 0
        citizenshipValue = ''

        if 'Citizenship' in person:
            citizenship = person['Citizenship']
            if 'Id' in citizenship:
                citizenshipId = int(citizenship['Id'])
            if 'Value' in citizenship:
                citizenshipValue = citizenship['Value']

        return dict({'Citizenship': {'Id':citizenshipId,'Value':citizenshipValue}})

    def getSnils(self, person):
        try:
            snils = person['SNILS'].strip()
            if not (len(snils) > 0):
                snils = None
        except:
            snils = None
        return dict({'SNILS': snils})

    def getBirthDate(self, person):
        bdate = None
        bdate_raw = person['BirthDate']

        # Проверяем, соответствует ли дата маске
        try:
            reg_ok = re.match(self.maskDate, bdate_raw)
        except:
            reg_ok = False

        if (reg_ok != False):
            if not (bdate_raw == '0001-01-01'):
                bdate = datetime.datetime.strptime(bdate_raw, "%Y-%m-%d").date()
        return dict({'BirthDate': bdate})


    def getAddreses(self, person, typeAddress):
        Address = dict()
        if typeAddress in person:
            tempAddress = person[typeAddress]
            if 'Type' in tempAddress:
                tempAddress_id = tempAddress['Type']['Id']
                tempAddress_value = tempAddress['Type']['Value']
                Type = dict({'Type': {'Id': tempAddress_id, 'Value': tempAddress_value}})
                Address.update(Type)
            if 'Value' in tempAddress:
                tempValue = tempAddress['Value']
                Value = dict({'Value': tempValue})
                Address.update(Value)
            if 'Fields' in tempAddress:
                tempFields = tempAddress['Fields']
                Fields = dict()
                newFields = dict()

                if 'ZipCode' in tempFields:
                    newFields.update({'ZipCode': tempFields['ZipCode']})
                if 'Country' in tempFields:
                    newFields.update({'Country': tempFields['Country']})
                if 'TerritorySubjectID' in tempFields:
                    newFields.update({'TerritorySubjectID': tempFields['TerritorySubjectID']})
                if 'TerritorySubjectName' in tempFields:
                    newFields.update({'TerritorySubjectName': tempFields['TerritorySubjectName']})
                if 'District' in tempFields:
                    newFields.update({'District': tempFields['District']})
                if 'PlaceTypeId' in tempFields:
                    newFields.update({'PlaceTypeId': tempFields['PlaceTypeId']})
                if 'PlaceTypeName' in tempFields:
                    newFields.update({'PlaceTypeName': tempFields['PlaceTypeName']})
                if 'PlaceKindId' in tempFields:
                    newFields.update({'PlaceKindId': tempFields['PlaceKindId']})
                if 'Place' in tempFields:
                    newFields.update({'Place': tempFields['Place']})
                if 'CityDistrict' in tempFields:
                    newFields.update({'CityDistrict': tempFields['CityDistrict']})
                if 'Street' in tempFields:
                    newFields.update({'Street': tempFields['Street']})
                if 'House' in tempFields:
                    newFields.update({'House': tempFields['House']})
                if 'Corpus' in tempFields:
                    newFields.update({'Corpus': tempFields['Corpus']})
                if 'Building' in tempFields:
                    newFields.update({'Building': tempFields['Building']})
                if 'Appartment' in tempFields:
                    newFields.update({'Appartment': tempFields['Appartment']})

                Fields = dict({'Fields': newFields})
                Address.update(Fields)
        return Address

    def trimSlash(self, string):
        pass

    def getPhones(self, person):
        newPhones = []
        phone_one = True
        if 'Phones' in person:
            phones = person['Phones']
            if (phones):
                if (len(phones['Phone'][0]) == 1):
                    newPhones.append(phones['Phone'])
                else:
                    for phone in phones['Phone']:
                        newPhones.append(phone)
        return dict({'Phones': newPhones})

    def getIdentityDoc(self, person):
        newIdentityDoc = dict()

        if 'IdentityDoc' in person:
            identityDoc = person['IdentityDoc']
            if 'Title' in identityDoc:
                try:
                    title = identityDoc['Title'].strip()
                except:
                    title = None
                newIdentityDoc.update({'Title': title})
            if 'Series' in identityDoc:
                try:
                    series = identityDoc['Series'].strip()
                except:
                    series = None
                newIdentityDoc.update({'Series': series})
            if 'Number' in identityDoc:
                try:
                    number = identityDoc['Number'].strip()
                except:
                    number = None
                newIdentityDoc.update({'Number': number})
            if 'Issuer' in identityDoc:
                try:
                    issuer = identityDoc['Issuer'].strip()
                except:
                    issuer = None
                newIdentityDoc.update({'Issuer': issuer})
            if 'IssueDate' in identityDoc:
                issue_date = None
                issue_date_raw = identityDoc['IssueDate']

                # Проверяем, соответствует ли дата маске
                try:
                    reg_ok = re.match(self.maskDate, issue_date_raw)
                except:
                    reg_ok = False

                if (reg_ok != False):
                    if not (issue_date_raw == '0001-01-01'):
                        issue_date = datetime.datetime.strptime(issue_date_raw, "%Y-%m-%d").date()
                newIdentityDoc.update({'IssueDate': issue_date})
        return dict({'IdentityDoc': newIdentityDoc})

    def getIsMale(self, person):
        isMale = None
        if 'IsMale' in person:
            isMaleRaw = person['IsMale']
            if (isMaleRaw == 'true'):
                isMale = 1
            elif (isMaleRaw == 'false'):
                isMale = 2
        return dict({'IsMale': isMale})

    def getPrimaryProfession(self, person):
        primaryProfession = ''
        if 'PrimaryProfession' in person:
            primaryProfession = person['PrimaryProfession']
        return dict({'PrimaryProfession': primaryProfession})

    def getPrimaryProfessionExperience(self, person):
        primaryProfessionExperience = ''
        if 'PrimaryProfession' in person:
            primaryProfessionExperience = person['PrimaryProfessionExperience']
        return dict({'PrimaryProfessionExperience': primaryProfessionExperience})

    def getQualification(self, person):
        qualification = None
        if 'Qualification' in person:
            qualification_row = person['Qualification']
            if not (qualification_row == '' or qualification_row == None):
                qualification = qualification_row
        return dict({'Qualification': qualification})

    def getCurrentJob(self, person):
        currentJob = ''
        if 'Qualification' in person:
            currentJob = person['CurrentJob']
        return dict({'CurrentJob': currentJob})

    def getEmploymentOrientationExists(self, person):
        employmentOrientationExists = ''
        if 'EmploymentOrientationExists' in person:
            employmentOrientationExists = person['EmploymentOrientationExists']
        return dict({'EmploymentOrientationExists': employmentOrientationExists})

    def getIsRegisteredInEmploymentService(self, person):
        isRegisteredInEmploymentService = ''
        if 'IsRegisteredInEmploymentService' in person:
            isRegisteredInEmploymentService = person['IsRegisteredInEmploymentService']
        return dict({'IsRegisteredInEmploymentService': isRegisteredInEmploymentService})

    def getDisabilityGroup(self, root):
        id = None
        value = None
        if 'DisabilityGroup' in root:
            disability_group = root['DisabilityGroup']
            if 'Id' in disability_group:
                id = disability_group['Id'].strip()
            if 'Value' in disability_group:
                value = disability_group['Value'].strip()
        return dict({'DisabilityGroup': {'Id': id,'Value': value}})

    def getDisabilityCause(self, root):
        id = None
        value = None
        if 'DisabilityCause' in root:
            disability_cause = root['DisabilityCause']
            if 'Id' in disability_cause:
                id_raw = disability_cause['Id'].strip()
                if not (len(id_raw) > 0):
                    id = int(id_raw)
                else:
                    id = int(id_raw)
            if 'Value' in disability_cause:
                value = disability_cause['Value'].strip()
        return dict({'DisabilityCause': {'Id': id,'Value': value}})

    def getRequiredHelp(self, root):
        return_mass = None
        required_help_mass = []
        if 'RequiredHelp' in root:
            required_help = root['RequiredHelp']
            if 'HelpItems' in required_help:
                temp_items = []
                help_items = required_help['HelpItems']
                if (help_items):
                    help_item = help_items['HelpItem']
                    try:
                        many_items = help_item[0]['HelpCategory']
                        for help in help_item:
                            if 'HelpCategory' in help:
                                category = help['HelpCategory']
                                id = int(category['Id'])
                                value = category['Value']
                                temp_items.append(dict({'Id': id, 'Value': value}))
                    except:
                        category = help_item['HelpCategory']
                        id = int(category['Id'])
                        value = category['Value']
                        temp_items.append(dict({'Id': id, 'Value': value}))

                    required_help_mass.append(temp_items)
                    if len(required_help_mass) > 0:
                        return_mass = required_help_mass
        return dict({'RequiredHelp': return_mass})


    def getDisabilityEndDate(self, root):
        disability_end_date = None
        if 'DisabilityEndDate' in root:
            disability_end_date_raw = root['DisabilityEndDate']

            # Проверяем, соответствует ли дата маске
            try:
                reg_ok = re.match(self.maskDate, disability_end_date_raw)
            except:
                reg_ok = False

            if (reg_ok != False):
                if not (disability_end_date_raw == '0001-01-01'):
                    disability_end_date = datetime.datetime.strptime(disability_end_date_raw, "%Y-%m-%d").date()

        return dict({'DisabilityEndDate': disability_end_date})

    def getProfSection(self, root):
        return self._getSection(root, 'ProfSection')

    def getSocSection(self, root):
        return self._getSection(root, 'SocSection')

    def _getSection(self, root, sectionName):
        newSection = dict()
        if sectionName in root:
            Section = root[sectionName]

            newEventGroups = dict()
            if 'EventGroups' in Section:
                xmlEventGroups = Section['EventGroups']
                tGroups = []

                xmlGroups = xmlEventGroups.get("Group")
                eventGroups = []
                if isinstance(xmlGroups, list):
                    for grOne in xmlGroups:
                        eventGroups.append(grOne)
                else:
                    eventGroups.append(xmlGroups)

                for oneGroup in eventGroups:
                    tGroup = dict()
                    if 'Id' in oneGroup:
                        id = dict({'Id': oneGroup['Id']})
                        tGroup.update(id)
                    if 'Need' in oneGroup:
                        need = dict({'Need': oneGroup['Need']})
                        tGroup.update(need)
                    if 'PeriodFrom' in oneGroup:
                        periodFrom = dict({'PeriodFrom': oneGroup['PeriodFrom']})
                        tGroup.update(periodFrom)
                    if 'PeriodTo' in oneGroup:
                        periodTo = dict({'PeriodTo': oneGroup['PeriodTo']})
                        tGroup.update(periodTo)
                    if 'Executor' in oneGroup:
                        executor = dict({'Executor': oneGroup['Executor']})
                        tGroup.update(executor)
                    if 'GroupType' in oneGroup:
                        GroupType = oneGroup['GroupType']
                        gt = dict()
                        if 'Id' in GroupType:
                            gt.update({'Id': GroupType['Id']})
                        if 'Value' in GroupType:
                            gt.update({'Value': GroupType['Value']})
                        tGroup.update({'GroupType': gt})
                    tGroups.append(tGroup)
                newEventGroups = dict({'EventGroups': tGroups})
            newSection.update(newEventGroups)
        return dict({sectionName: newSection})