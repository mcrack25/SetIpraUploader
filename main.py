from packages.connection import *
from app.models.InvalidsTrudo import InvalidsTrudo
from app.models.InvalidsSocial import InvalidsSocial
from app.models.NaznachMeropTrudo import NaznachMeropTrudo
from app.models.NaznachMeropSocial import NaznachMeropSocial
from app.controllers.XmlsController import XmlsController
from app.controllers.SyncController import SyncController

import datetime

if(__name__ == "__main__"):
    print('Программа запущена!!!')
    try:
        db.connect()
        # Создаём таблицы по занятости
        #InvalidsTrudo.create_table()
        #NaznachMeropTrudo.create_table()
        # Создаём таблицы по соцблоку
        #InvalidsSocial.create_table()
        #NaznachMeropSocial.create_table()
    except:
        print('Ошибка!!! Не удалось подключиться к базе данных!')
        exit()

    # print('Распаковываем архив с файлами XML')
    # XmlsController().sendToXmls()

    print('Загружаем данные по занятости')
    SyncController().trudoSend()

    print('Загружаем данные по соцблоку')
    SyncController().socialSend()

    print('Программа выполнена!!!')