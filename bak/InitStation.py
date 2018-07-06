#coding=utf-8
import requests
import datetime
import xlrd
import time
from time import sleep
import ReadMysql
import pymysql as mdb
from kazoo.client import KazooClient

class InitStation():
    def __init__(self):
        self.zk = KazooClient(hosts=ReadMysql.ReadMysql().zkhost)

    def clean_station_pick(self,ordernumber):
        '''清空拣货订单的数据并使工作站初始化。例
					|ordernumber
		'''
        try:
            host=ReadMysql.ReadMysql().get_station_windows_ip(ReadMysql.ReadMysql().stationid)
            url= "http://" + host + ":8" + ReadMysql.ReadMysql().stationid + "/stationenginedaemon/resetWorkflow"
            ReadMysql.ReadMysql().init_station_picking(ordernumber)
            sleep(3)
            requests.get(url)
            print(url)
        except:
            print u"本地启动工作站机器ip获取连接失败"

    def clean_station_replen(self):
        """清空补货订单的数据并使工作站初始化。
        """
        try:
            host = ReadMysql.ReadMysql().get_station_windows_ip(ReadMysql.ReadMysql().stationid)
            url = "http://" + host + ":8" + ReadMysql.ReadMysql().stationid + "/stationenginedaemon/resetWorkflow"
            ReadMysql.ReadMysql().init_station_replenishment()
            sleep(3)
            requests.get(url)
            print(url)
        except:
            print u"本地启动工作站机器ip获取连接失败"



    def clean_zk(self):
        '''清空小车在工作站占位情况下的pick节点并清空工作站pick节点。例

        		'''
        zk = KazooClient(hosts=ReadMysql.ReadMysql().zkhost)
        stationid = ReadMysql.ReadMysql().stationid
        try:
            driverunitid = (ReadMysql.ReadMysql().get_driverunitid())
            print u"待清空小车列表为： "
            print  driverunitid
        except :
            print(u"没有小车在工作站，没有zookeeper任务节点，无需清理")
        try:
            for i in driverunitid:
                    zk.start()
                    print(u"正在清空的小车号为:  " + i[0])
                    picking_job=zk.get_children("/driveunitTasksAssign/"+ i[0] +"/jobs")
                    picking = zk.get_children("/stationTasksAssign/" + stationid + "/picking")
                    replen = zk.get_children("/stationTasksAssign/" + stationid + "/replenishment")
                    for st in picking:
                        print(stationid + u"号工作站的picking节点为： " + st)
                        sleep(2)
                        zk.delete("/stationTasksAssign/" + stationid + "/picking/" + st, recursive=True)
                    for re in replen:
                        print(stationid + u"号工作站的picking节点为： " + re)
                        sleep(2)
                        zk.delete("/stationTasksAssign/" + stationid + "/replenishment/" + re, recursive=True)
                    for dt in picking_job:
                        print(i[0] + u"号小车的jobs节点为： " + dt)
                        zk.delete("/driveunitTasksAssign/" + i[0] + "/jobs/" + dt, recursive=True)
                    zk.stop()
        except Exception as result:
                print(u"节点已删除")
                print result




    def reset_driverunit(self,ordernumber):
        '''下发小车复位指令。例
        					|ordernumber
        		'''
        try:
            zk = KazooClient(hosts=ReadMysql.ReadMysql().zkhost)
            driverunitid = (ReadMysql.ReadMysql().get_driverunitid_in_station())
            print(ReadMysql.ReadMysql().reset_jobID)
            print  driverunitid
            for d in driverunitid:
                sleep(1)
                ReadMysql.ReadMysql().reset_driverunit(ordernumber)
                zk.start()
                zk.create("/driveunitTasksAssign/" + d[0] + "/jobs/" + ReadMysql.ReadMysql().reset_jobID,b"")
                sleep(1)
                result = zk.get_children("/driveunitTasksAssign/" + d[0] + "/jobs")
                print(d[0] + u"号小车的节点展示为： " )
                print  (result)
                zk.stop()
        except Exception:
            print(u"没有小车在工作站或zk连接失败")

