import os

class LikeName:
    where = set()
    what = set()

    def __init__(self, where, what):
        self.where = where
        self.what = what

    def get(self):
        where = self.where.lower()
        what = self.what.lower()

        if what in where:
            return True
        return False

    def likeDir(self):
        l = list()
        dirs = self.getDirs()
        for dir in dirs:
            dirName = os.path.basename(dir).lower()
            what = self.what.lower()
            index = dirName.find(what)
            if(index >= 0):
                l.append(dir)
        return l

    def getDirs(self, dir=''):
        l = list()
        path = ''

        if(dir != ''):
            dirList = os.listdir(dir)
            path = dir
        else:
            dirList = os.listdir(self.where)
            path = self.where

        for oneDir in dirList:
            newDir = os.path.join(path, oneDir)
            if os.path.isdir(newDir):
                l.append(newDir)
                ll = self.getDirs(newDir)
                l += ll
        return l