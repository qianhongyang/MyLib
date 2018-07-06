#coding=utf-8
from ControlIni import ControlIni as ci

class a(object):
    def __init__(self):
        pass

    def getConf(self, path):
        a=ci(path)
        ip = ci.readIni(a,path,"MYSQL", "ip")
        print ip

if __name__ == '__main__':
    a=a()
    a.getConf("D:\PycharmPoject\MyLib\config.ini")