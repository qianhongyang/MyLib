#coding=utf-8

import configparser


class ControlIni(object):

   #读配置文件
    def writeIni(self,path,section,option,value):
        """
        读配置文件
        :param path:
        :param section:
        :param option:
        :param value:
        :return:
        """
        cf = configparser.ConfigParser()
        cf.read(path)

        cf.set(section, option,value)
        with open(path,"w+") as f:
            cf.write(f)


    #读配置文件
    def readIni(self,path,section,name):
        """
        读配置文件
        :param path:
        :param section:
        :param name:
        :return:
        """
        cf = configparser.ConfigParser()
        cf.read(path)
        value = cf.get(section, name)
        return value

    #删除配置文件
    def delIni(self,path,section,option):
        """
        删除配置文件
        :param path:
        :param section:
        :param option:
        :return:
        """
        cf = configparser.ConfigParser()
        cf.read(path)
        cf.remove_option(section,option)
        cf.write(open(path,"w+"))

# if __name__ == '__main__':
#     a=ControlIni()
#     print  a.readIni("D:\\PycharmPoject\\MyLib\\config.ini","MYSQL","port")


