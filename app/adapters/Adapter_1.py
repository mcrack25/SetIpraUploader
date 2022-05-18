import datetime
import re
from app.adapters.AAdapter import AAdapter

class Adapter_1(AAdapter):
    version = 1

    def getMseId(self, root):
        return dict({'MseId':root['Id']})

    def getFIO(self, person):
        Fio = person['FIO']
        firstName = Fio['ct:FirstName']
        lastName = Fio['ct:LastName']
        secondName = Fio['ct:SecondName']
        return dict({'FIO':{'FirstName':firstName,'LastName':lastName,'SecondName':secondName}})

    def getPersonAge(self, person):
        ages = person['Age']
        years = int(ages['ct:Years'])
        return dict({'Age': {'Years':years}})

    def getPersonCitizenship(self, person):
        citizenshipId = 0
        citizenshipValue = ''

        if 'Citizenship' in person:
            citizenship = person['Citizenship']
            if 'ct:Id' in citizenship:
                citizenshipId = int(citizenship['ct:Id'])
            if 'ct:Value' in citizenship:
                citizenshipValue = citizenship['ct:Value']

        return dict({'Citizenship': {'Id':citizenshipId,'Value':citizenshipValue}})

    def getAddreses(self, person, typeAddress):
        Address = dict()
        if typeAddress in person:
            tempAddress = person[typeAddress]
            if 'Type' in tempAddress:
                tempAddress_id = tempAddress['Type']['ct:Id']
                tempAddress_value = tempAddress['Type']['ct:Value']
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
                        if 'ct:Id' in GroupType:
                            gt.update({'Id': GroupType['ct:Id']})
                        if 'ct:Value' in GroupType:
                            gt.update({'Value': GroupType['ct:Value']})
                        tGroup.update({'GroupType': gt})
                    tGroups.append(tGroup)
                newEventGroups = dict({'EventGroups': tGroups})
            newSection.update(newEventGroups)
        return dict({sectionName: newSection})


    def getIdentityDoc(self, person):
        newIdentityDoc = dict()

        if 'IdentityDoc' in person:
            identityDoc = person['IdentityDoc']
            if 'ct:Title' in identityDoc:
                try:
                    title = identityDoc['ct:Title'].strip()
                except:
                    title = None
                newIdentityDoc.update({'Title': title})
            if 'ct:Series' in identityDoc:
                try:
                    series = identityDoc['ct:Series'].strip()
                except:
                    series = None
                newIdentityDoc.update({'Series': series})
            if 'ct:Number' in identityDoc:
                try:
                    number = identityDoc['ct:Number'].strip()
                except:
                    number = None
                newIdentityDoc.update({'Number': number})
            if 'ct:Issuer' in identityDoc:
                try:
                    issuer = identityDoc['ct:Issuer'].strip()
                except:
                    issuer = None
                newIdentityDoc.update({'Issuer': issuer})
            if 'ct:IssueDate' in identityDoc:
                issue_date = None
                issue_date_raw = identityDoc['ct:IssueDate']

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


    def getBuro(self, root):
        buro = root['Buro']
        short_name = buro['ct:ShortName']
        full_name = buro['ct:FullName']
        number = buro['ct:Number']
        org_name = buro['ct:OrgName']
        specializations = buro['ct:Specializations']
        buro_mass = dict()
        buro_mass.update({'ShortName':short_name,'FullName':full_name,'Number':number,'OrgName':org_name,'Specializations':specializations})
        return dict({'Buro':buro_mass})

    def getRecipient(self, root):
        recipient = root['Recipient']
        recipient_type = recipient['RecipientType']

        name = recipient['Name']
        address = recipient['Address']
        id = recipient_type['ct:Id']
        value = recipient_type['ct:Value']

        recipient_mass = dict()
        recipient_mass.update({'Name': name,'Address': address,'Id': id,'Value': value})
        return dict({'Recipient': recipient_mass})

    def getDisabilityGroup(self, root):
        id = ''
        value = ''
        if 'DisabilityGroup' in root:
            disability_group = root['DisabilityGroup']
            if 'ct:Id' in disability_group:
                id = disability_group['ct:Id']
            if 'ct:Value' in disability_group:
                value = disability_group['ct:Value']

        return dict({'DisabilityGroup': {'Id': id, 'Value': value}})

    def getDisabilityCause(self, root):
        id = None
        value = None
        if 'DisabilityCause' in root:
            disability_cause = root['DisabilityCause']
            if 'Id' in disability_cause:
                id_raw = disability_cause['ct:Id'].strip()
                if not (len(id_raw) > 0):
                    id = int(id_raw)
                else:
                    id = int(id_raw)
            if 'Value' in disability_cause:
                value = disability_cause['ct:Value'].strip()
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
                                id = int(category['ct:Id'])
                                value = category['ct:Value']
                                temp_items.append(dict({'Id': id, 'Value': value}))
                    except:
                        category = help_item['HelpCategory']
                        id = int(category['ct:Id'])
                        value = category['ct:Value']
                        temp_items.append(dict({'Id': id, 'Value': value}))

                    required_help_mass.append(temp_items)
                    if len(required_help_mass) > 0:
                        return_mass = required_help_mass
        return dict({'RequiredHelp': return_mass})