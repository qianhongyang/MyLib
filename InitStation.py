#coding=utf-8
import requests
import time
from time import sleep
import ReadMysql
from kazoo.client import KazooClient

class InitStation(object):


    def clean_station_pick(self,ip, dbuser, dbpasswd, dbport, dbdatabase,stationname,ordernumber):
        """
        清空拣货订单的数据并使工作站初始化
        :param ip:
        :param dbuser:
        :param dbpasswd:
        :param dbport:
        :param dbdatabase:
        :param stationname:
        :param zkport:
        :param ordernumber:
        :return:
        """

        rm=ReadMysql.ReadMysql()
        try:
            stationid=stationname.split("-")[-1]
            host=rm.get_station_windows_ip(ip, dbuser, dbpasswd, dbport, dbdatabase,stationname)
            print host
            url= "http://" + host + ":8" + stationid + "/stationenginedaemon/resetWorkflow"
            rm.init_station_picking(ip, dbuser, dbpasswd, dbport, dbdatabase,ordernumber)
            sleep(3)
            requests.get(url)
            print(url)
        except Exception as results:
            print u"本地启动工作站机器ip获取连接失败"
            print results

    def clean_station_replen(self,ip, dbuser, dbpasswd, dbport, dbdatabase,stationname):
        """
        清空补货订单的数据并使工作站初始化。
        :param ip:
        :param dbuser:
        :param dbpasswd:
        :param dbport:
        :param dbdatabase:
        :param stationname:
        :return:
        """
        rm = ReadMysql.ReadMysql()
        try:
            stationid = stationname.split("-")[-1]
            host = rm.get_station_windows_ip(ip, dbuser, dbpasswd, dbport, dbdatabase,stationname)
            url = "http://" + host + ":8" + stationid + "/stationenginedaemon/resetWorkflow"
            rm.init_station_replenishment(ip, dbuser, dbpasswd, dbport, dbdatabase)
            sleep(3)
            requests.get(url)
            print(url)
        except Exception as results:
            print u"本地启动工作站机器ip获取连接失败"
            print results


    def clean_zk(self,ip, dbuser, dbpasswd, dbport, dbdatabase,stationname,zkport):
        """
        清空小车在工作站占位情况下的pick节点并清空工作站pick节点。例
        :param ip:
        :param dbuser:
        :param dbpasswd:
        :param dbport:
        :param dbdatabase:
        :param stationname:
        :param zkport:
        :return:
        """
        zkhost = ip + ":" + str(zkport)
        zk = KazooClient(hosts=zkhost)
        rm = ReadMysql.ReadMysql()
        try:
            stationid = stationname.split("-")[-1]
            driverunitid = (rm.get_driverunitid(ip, dbuser, dbpasswd, dbport, dbdatabase))
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




    def reset_driverunit(self,ip, dbuser, dbpasswd, dbport, dbdatabase, stationname, zkport,ordernumber):
        """
        下发小车复位指令。例
        :param ip:
        :param dbuser:
        :param dbpasswd:
        :param dbport:
        :param dbdatabase:
        :param stationname:
        :param zkport:
        :param ordernumber:
        :return:
        """
        reset_jobID = "RESET_" + time.strftime("%m%d%H%M%S")
        rm = ReadMysql.ReadMysql()
        try:
            zkhost = ip + ":" + str(zkport)
            zk = KazooClient(hosts=zkhost)
            driverunitid = (rm.get_driverunitid_in_station(ip, dbuser, dbpasswd, dbport, dbdatabase))


            print  "在工作站的小车列表如下："
            print driverunitid
            if driverunitid==():
                print u"没有小车在工作站"
            for d in driverunitid:
                sleep(1)
                rm.reset_driverunit(ip, dbuser, dbpasswd, dbport, dbdatabase,ordernumber,stationname,reset_jobID)
                zk.start()
                zk.create("/driveunitTasksAssign/" + d[0] + "/jobs/" + reset_jobID,b"")
                sleep(1)
                result = zk.get_children("/driveunitTasksAssign/" + d[0] + "/jobs")
                print(d[0] + u"号小车的节点展示为： " )
                print  (result)
                zk.stop()
        except Exception as results:
            print results
#if __name__ == '__main__':

        # a=InitStation()
        # a.clean_station_pick("192.168.21.14","root","","6014","walle_erp","walle-station-x64-101","6024","0613210518802000")
        # #a.clean_zk("192.168.21.14","root","","6014","walle_erp","walle-station-x64-101","6024")
        #a.reset_driverunit("192.168.21.14","root","","6014","walle_erp","walle-station-x64-101","6024","222")
