import os
import shutil
from packages.dirs import Dirs
from packages.unzip import Unzip
from packages.likename import LikeName

#UploadController
class XmlsController:
    uploadDir = ''
    tempDir = ''
    xmlsDir = ''

    def __init__(self):
        self.uploadDir = Dirs().get('upload')
        self.tempDir = Dirs().get('temp')
        self.xmlsDir = Dirs().get('xmls')

    # Получаем все архивы в папке upload
    def getZips(self):
        filesZip = set()
        for fileZip in os.listdir(self.uploadDir):
            if fileZip.endswith('.zip'):
                filesZip.add(os.path.join(self.uploadDir, fileZip))
        return filesZip

    # Удаляем содержимое папки temp
    def clearTemp(self):
        for dir in os.listdir(self.tempDir):
            shutil.rmtree(os.path.join(self.tempDir, dir))

    # Распаковываем файлы в папку TEMP, предварительно очистив папку TEMP
    def useUnzip(self):
        self.clearTemp()

        filesZip = self.getZips()
        for oneFileZip in filesZip:
            Unzip(oneFileZip, self.tempDir).run()

    def moveTrudo(self):
        # Получаем все папки, в которых содержится название SEC_2
        items = self.likeDir('SEC_2')
        # Перемещаем файлы в папку trudo
        self.movefiles(items, self.xmlsDir, 'trudo')

    def moveSocial(self):
        # Получаем все папки, в которых содержится название SEC_4
        items = self.likeDir('SEC_4')
        # Перемещаем файлы в папку socical
        self.movefiles(items, self.xmlsDir, 'social')

    def sendToXmls(self):
        self.useUnzip()
        self.moveTrudo()
        self.moveSocial()

    @staticmethod
    def likeDir(like):
        tempDir = Dirs().get('temp')
        l = LikeName(tempDir, like).likeDir()
        return l

    @staticmethod
    def movefiles(dirs, xmlsDir, type):
        for dir in dirs:
            for file in os.listdir(dir):
                fileFrom = os.path.join(dir, file)
                fileTo = os.path.join(xmlsDir, type, file)
                shutil.move(fileFrom, fileTo)
