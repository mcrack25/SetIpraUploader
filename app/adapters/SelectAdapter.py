from app.adapters.Adapter_1 import Adapter_1
from app.adapters.Adapter_3 import Adapter_3

class SelectAdapter:
    data = dict()

    def __init__(self, data, fileName):
        root = dict()
        version = 0

        if 'tIPRA' in data:
            root = data['tIPRA']

            if '@version' in root:
                version = float(root['@version'])
            elif '@Version' in root:
                version = float(root['@Version'])
            else:
                return
        else:
            return

        if(version < 3.0):
            self.data = Adapter_1(data).getData()
        elif(version >= 3.0) & (version < 4.0):
            self.data = Adapter_3(data).getData()
        else:
            print('Неизвестная версия файла ' + fileName + '!!! Адаптер не существует!!!')
            exit()

    def getData(self):
        return self.data