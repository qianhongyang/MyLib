#-*- coding:utf-8 -*-
'''
    created by hch 2018-5-25
'''



from SendOrder import SendOrder
from InitStation import InitStation
from ReadMysql import ReadMysql
from ControlIni import ControlIni

__version__ = '0.1'

class MyLib(SendOrder,InitStation,ReadMysql,ControlIni):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
