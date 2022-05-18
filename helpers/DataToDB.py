from app.models.InvalidsTrudo import InvalidsTrudo

class DataToDB:
    _data = dict()
    _file = None

    def __init__(self, data, file=None):
        self._data = data
        self._file = file

    @staticmethod
    def strToLower(string):
        if(string == 'None'):
            return None
        return string.title()

    def upload(self):
        inserted = 0
        updated = 0

        last_name = str(self._data['Person']['FIO']['LastName'])
        first_name = str(self._data['Person']['FIO']['FirstName'])
        second_name = str(self._data['Person']['FIO']['SecondName'])

        params = dict(
            mse_id=self._data['MseId'],
            last_name=self.strToLower(last_name),
            first_name=self.strToLower(first_name),
            second_name=self.strToLower(second_name)
        )

        paramsWhere = InvalidsTrudo.mse_id==params['mse_id']

        haveRecords = InvalidsTrudo.select().where(paramsWhere)
        if (len(haveRecords) > 0):
            InvalidsTrudo.update(params).where(paramsWhere).execute()
            updated += 1
        else:
            InvalidsTrudo.insert(params).on_conflict('replace').execute()
            inserted += 1

        return dict({"updated": updated,"inserted": inserted})