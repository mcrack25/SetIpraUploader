import os
import zipfile
import shutil
from pathlib import Path

class Unzip:
    filePath = ''
    outPath = ''

    def __init__(self, filePath, outPath):
        self.filePath = filePath
        self.outPath = outPath

    def cleanTemp(self, tempDir):
        dirList = os.listdir(tempDir)
        for dir in dirList:
            newDir = os.path.join(tempDir, dir)
            shutil.rmtree(newDir)
        pass

    def run(self):
        # Очищаем файлы в папке temp
        self.cleanTemp(self.outPath)
        # Разархивируем файлы в папку temp
        fantasy_zip = zipfile.ZipFile(self.filePath)
        fantasy_zip.extractall(self.outPath)
        fantasy_zip.close()
        # Меняем имена с крокозябры, на нормальные
        self.setCharset()

    def getDirs(self, path):
        l = list()
        dirList = os.listdir(path)
        for dir in dirList:
            newDir = os.path.join(path, dir)
            if os.path.isdir(newDir):
                l.append(newDir)
                ll = self.getDirs(newDir)
                l += ll
        return l


    def setCharset(self):
        tempDir = os.path.abspath(self.outPath)
        dirs = self.getDirs(tempDir)

        for dir in dirs:
            dirNameEncode = dir.encode('cp437').decode('cp866')
            os.rename(dir, dirNameEncode)

