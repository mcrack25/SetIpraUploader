import os
from peewee import *
from packages.config import Config
from packages.dirs import Dirs

dbType = Config('database').get('dbType')
db_user = Config('database').get('dbUser')
db_password = Config('database').get('dbPass')
db_name = Config('database').get('dbName')
db_host = Config('database').get('dbHost')
db_port = int(Config('database').get('dbPort'))

if (dbType == 'mysql'):
    db = MySQLDatabase(db_name, user=db_user, password=db_password,host=db_host, port=db_port)

elif(dbType == 'postgres'):
    db = PostgresqlDatabase(db_name, user=db_user, password=db_password, host=db_host, port=db_port)

elif(dbType == 'sqlite'):
    dirDb = Dirs().get('databases')
    fileDb = os.path.join(dirDb, db_name)
    db = SqliteDatabase(fileDb)

else:
    print('Ошибка!!! Не верный тип базы данных')
    exit()