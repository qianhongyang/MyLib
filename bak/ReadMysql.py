#coding=utf-8
import pymysql as mdb
import time
import xlrd



class ReadMysql(object):
    def __init__(self):
        filepath = "D:\\conf.xls"
        xls_file = xlrd.open_workbook(filename=filepath)
        self.table = xls_file.sheet_by_index(0)
        self.ip = self.table.cell_value(2, 1)
        self.zkport = self.table.cell_value(2, 7)
        self.user = self.table.cell_value(2, 3)
        self.passwd = self.table.cell_value(2, 4)
        self.stationname = self.table.cell_value(6, 1)
        self.stationid = self.stationname.split('-')[1]
        self.db_1='walle_erp'
        self.port=int(self.table.cell_value(2, 8))
        self.db_2="walle_core"
        self.reset_jobID = "RESET_" + time.strftime("%m%d%H%M%S")
        self.nowtime =  time.strftime("%Y-%m-%d %H:%M:%S")
        self.zkhost = self.ip + ":" + self.zkport












    #获取order状态
    def connectMsql(self,orderNumber=""):
        '''获取order状态。例
                					|ordernumber
                		'''
        try:
            con = mdb.connect(ReadMysql().ip, ReadMysql().user, ReadMysql().passwd, ReadMysql().db_1, ReadMysql().port)
            cur = con.cursor()
            cur.execute("SELECT state FROM walle_erp.orders WHERE orderNumber= %s;",(orderNumber))
            order_state=cur.fetchone()
            print(order_state[0])
            cur.close()
            con.close()
            return order_state[0]
        except TypeError:
            print(u"请查看传值是否为空或类型错误")



    #获取二号工作站状态
    def get_station_state(self,stationNumber):
        '''获取二号工作站状态。例
                					|stationnumber
                		'''
        try:
            con = mdb.connect(ReadMysql().ip, ReadMysql().user, ReadMysql().passwd, ReadMysql().db_1, ReadMysql().port)
            cur = con.cursor()
            cur.execute("SELECT state FROM walle_core.stations WHERE stationID=%s;", (stationNumber))
            station_state = cur.fetchone()
            print(station_state[0])
            cur.close()
            con.close()
            return station_state[0]
        except TypeError:
            print(u"请查看传值是否为空或类型错误")



    #获取一个可用的箱号
    def get_box(self):
        '''获取一个可用箱号。例

                		'''
        try:
            con = mdb.connect(ReadMysql().ip, ReadMysql().user, ReadMysql().passwd, ReadMysql().db_1, ReadMysql().port)
            cur = con.cursor()
            cur.execute("SELECT boxNumber from walle_erp.box WHERE walle_erp.box.state = 'PROVIDED';")
            all_box=cur.fetchall()
            box_list = []
            for box in all_box:
                box_list.append(box)
            print("box_1 = "+ box_list[0][0])
            print("box_2 = "+ box_list[1][0])
            print("box_3 = "+ box_list[2][0])
            cur.close()
            con.close()
            return box_list
        except:
            print(u"读取箱号失败")




    #获取picking_packages状态绑定箱号信息
    def get_results(self,orderNumber=""):
        '''获取picking_packages状态绑定箱号信息。例
                					|ordernumber
                		'''
        try:
            con = mdb.connect(ReadMysql().ip, ReadMysql().user, ReadMysql().passwd, ReadMysql().db_1, ReadMysql().port)
            cur = con.cursor()

            cur.execute("SELECT orders.orderID FROM walle_erp.orders WHERE orderNumber = %s;",(orderNumber))
            orderId=cur.fetchall()
            a=orderId[0][0]

            cur.execute("SELECT orderID,quantity,relatedNumber FROM walle_core.picking_packages WHERE orderID = CONCAT('PO_',%s);",(a))
            results=cur.fetchall()
            print(results)
            cur.close()
            con.close()
            return results
        except:
            print(u"查询数据库失败")


    #拿结果表的后三条
    def get_results_three(self):
        '''获取最后三条结果
                		'''
        try:
            con = mdb.connect(ReadMysql().ip, ReadMysql().user, ReadMysql().passwd, ReadMysql().db_1, ReadMysql().port)
            cur = con.cursor()

            cur.execute("select orderID,quantity,relatedNumber FROM walle_core.picking_packages GROUP BY  createdDate DESC limit 3;")
            results=cur.fetchall()
            print(results)
            cur.close()
            con.close()
            return results
        except:
            print(u"查询数据库失败")




    # 拿结果表的后两条
    def get_results_Two(self):
        '''获取最后两条结果
                		'''
        try:
            con = mdb.connect(ReadMysql().ip, ReadMysql().user, ReadMysql().passwd, ReadMysql().db_1, ReadMysql().port)
            cur = con.cursor()
            cur.execute("select orderID,quantity,relatedNumber,createdDate FROM walle_core.picking_packages GROUP BY  createdDate DESC limit 2;")
            results = cur.fetchall()
            print(results)
            cur.close()
            con.close()
            return results
        except:
            print(u"查询数据库失败")



    #造一条测试数据，把商品数量调为10000
    def create_test_data(self):
        '''造一条商品数据并把数量调为一万
                		'''
        try:
            con = mdb.connect(ReadMysql().ip, ReadMysql().user, ReadMysql().passwd, ReadMysql().db_1, ReadMysql().port)
            cur = con.cursor()

            cur.execute("SELECT skuID FROM walle_core.bucket_slot_skus  GROUP BY skuID HAVING count(*) = 1 LIMIT 1;")
            skuid=cur.fetchone()

            cur.execute("SELECT skuNumber from walle_erp.skus where skuID=%s;",(skuid))
            skuNumber=cur.fetchone()
            print("skuNumber = " +  skuNumber[0])

            cur.execute("UPDATE walle_erp.inventorys SET quantity = '10000' WHERE skuID = %s;",(skuid))

            cur.execute("UPDATE walle_core.bucket_slot_skus SET quantity = '10000' WHERE skuID = %s;",(skuid))

            con.commit()
            skuNumber_0=skuNumber[0]
            cur.close()
            con.close()
        except:
            print(u"数据库连接失败")




     #造一条测试数据，把商品数量调为10000,写入ini，skuno_2
    def create_test_data_2(self):
        '''一条商品数据，把商品数量调整为一万，为skuno2
                		'''
        try:
            con = mdb.connect(ReadMysql().ip, ReadMysql().user, ReadMysql().passwd, ReadMysql().db_1, ReadMysql().port)
            cur = con.cursor()

            cur.execute("SELECT skuID FROM walle_core.bucket_slot_skus  GROUP BY skuID HAVING count(*) = 1 LIMIT 2;")
            skuid=cur.fetchall()


            cur.execute("SELECT skuNumber from walle_erp.skus where skuID=%s;",(skuid[1]))
            skuNumber=cur.fetchone()
            print("skuNumber = " +  skuNumber[0])

            cur.execute("UPDATE walle_erp.inventorys SET quantity = '10000' WHERE skuID = %s;",(skuid[1]))

            cur.execute("UPDATE walle_core.bucket_slot_skus SET quantity = '10000' WHERE skuID = %s;",(skuid[1]))

            con.commit()
            cur.close()
            con.close()
        except:
            print(u"数据库连接失败")


#创建商品3
    def create_test_data_3(self):
        '''创造一条商品数据，为skuno3
                		'''
        try:
            con = mdb.connect(ReadMysql().ip, ReadMysql().user, ReadMysql().passwd, ReadMysql().db_1, ReadMysql().port)
            cur = con.cursor()

            cur.execute("SELECT skuID FROM walle_core.bucket_slot_skus  GROUP BY skuID HAVING count(*) = 1 LIMIT 3;")
            skuid=cur.fetchall()


            cur.execute("SELECT skuNumber from walle_erp.skus where skuID=%s;",(skuid[2]))
            skuNumber=cur.fetchone()
            print("skuNumber = " +  skuNumber[0])

            cur.execute("UPDATE walle_erp.inventorys SET quantity = '10000' WHERE skuID = %s;",(skuid[2]))

            cur.execute("UPDATE walle_core.bucket_slot_skus SET quantity = '10000' WHERE skuID = %s;",(skuid[2]))

            con.commit()
            cur.close()
            con.close()
        except:
            print(u"数据库连接失败")







#创建商品4
    def create_test_data_4(self):
        '''创建商品4
                		'''
        try:
            con = mdb.connect(ReadMysql().ip, ReadMysql().user, ReadMysql().passwd, ReadMysql().db_1, ReadMysql().port)
            cur = con.cursor()

            cur.execute("SELECT skuID FROM walle_core.bucket_slot_skus  GROUP BY skuID HAVING count(*) = 1 LIMIT 5;")
            skuid=cur.fetchall()


            cur.execute("SELECT skuNumber from walle_erp.skus where skuID=%s;",(skuid[4]))
            skuNumber=cur.fetchone()
            print("skuNumber = " +  skuNumber[0])

            cur.execute("UPDATE walle_erp.inventorys SET quantity = '10000' WHERE skuID = %s;",(skuid[4]))

            cur.execute("UPDATE walle_core.bucket_slot_skus SET quantity = '10000' WHERE skuID = %s;",(skuid[4]))

            con.commit()
            cur.close()
            con.close()
        except:
            print(u"数据库连接失败")



    #更改ordertype
    def change_ordertype(self,ordertype,orderNumber):
        '''改变订单状态。例
                					|ordertype|ordernumber
                		'''
        try:
            con = mdb.connect(ReadMysql().ip, ReadMysql().user, ReadMysql().passwd, ReadMysql().db_1, ReadMysql().port)
            cur = con.cursor()

            cur.execute("UPDATE walle_erp.orders SET orderType=%s WHERE orderNumber=%s;",(ordertype,orderNumber))
            con.commit()
            cur.close()
            con.close()
            print("Change ordertype success!")
        except:
            print(u"数据库连接失败")

    # 提交订单
    def change_orderstate(self,orderNumber):
        '''提交订单。例
                                    |ordernumber
                        '''
        try:
            con = mdb.connect(ReadMysql().ip, ReadMysql().user, ReadMysql().passwd, ReadMysql().db_1,
                              ReadMysql().port)
            cur = con.cursor()
            cur.execute("UPDATE walle_erp.orders SET state='PENDING_PROCESS' WHERE orderNumber=%s;", (orderNumber))
            con.commit()
            cur.close()
            con.close()
            print("Change orderstate success!")
        except:
            print(u"数据库连接失败")

    #初始化工作站拣货任务
    def init_station_picking(self,ordernumber):
        '''数据库初始化工作站拣货任务。例
                					|ordernumber
                		'''
        try:
            con = mdb.connect(ReadMysql().ip, ReadMysql().user, ReadMysql().passwd, ReadMysql().db_1, ReadMysql().port)
            cur = con.cursor()

            cur.execute("UPDATE walle_erp.orders SET state = 'CANCEL' WHERE orderNumber = %s;",(ordernumber))
            cur.execute("UPDATE walle_erp.picking_orders SET state = 'CANCEL' WHERE orderNumber = %s;", (ordernumber))
            cur.execute("UPDATE walle_core.jobs SET state = 'ROLLBACK' WHERE jobID IN (SELECT jobID FROM walle_core.picking_jobs j LEFT JOIN walle_erp.picking_orders o ON j.orderID = o.orderID WHERE o.orderNumber = %s);", (ordernumber))
            cur.execute("DELETE FROM walle_core.station_slot_bindings WHERE billID IN ( SELECT orderID FROM walle_erp.picking_orders WHERE orderNumber = %s);", (ordernumber))
            cur.execute("DELETE FROM walle_erp.`box_details` WHERE sourceBillID IN (SELECT orderID FROM walle_erp.picking_orders WHERE orderNumber = %s);", (ordernumber))
            cur.execute("UPDATE walle_core.buckets SET driveunitId = NULL WHERE bucketID IN (SELECT bucketID FROM walle_core.picking_jobs j LEFT JOIN walle_erp.picking_orders o ON j.orderID = o.orderID WHERE o.orderNumber = %s);", (ordernumber))
            cur.execute("UPDATE walle_core.driveunits SET bucketID = NULL WHERE bucketID IN (SELECT bucketID FROM walle_core.picking_jobs j LEFT JOIN walle_erp.picking_orders o ON j.orderID = o.orderID WHERE o.orderNumber = %s);", (ordernumber))
            cur.execute("UPDATE walle_core.stations SET state = 'DONE' where state = 'PULLED';")
            con.commit()
            cur.close()
            con.close()
        except:
            print(u"初始化工作站拣货任务,数据库连接失败")

    # 初始化工作站补货任务
    def init_station_replenishment(self):
        '''数据库初始化工作站补货任务。例
                					|ordernumber
                		'''
        try:
            con = mdb.connect(ReadMysql().ip, ReadMysql().user, ReadMysql().passwd, ReadMysql().db_1,
                              ReadMysql().port)
            cur = con.cursor()
            cur.execute("SELECT billID  from   walle_erp.direct_shelve_bills WHERE state = 'DOING';")
            billID=cur.fetchone()
            print u"当前补货任务billID为：" + billID[0]
            cur.execute("UPDATE walle_core.jobs SET state = 'ROLLBACK' WHERE jobID in (SELECT jobID from   walle_core.count_check_jobs WHERE bucketDispatchID = CONCAT('BS_',%s));",(billID[0]))
            # jobIDs = cur.fetchall()
            # for jobID in  jobIDs:
            #     print u"当前补货任务jobID为：" + jobID[0]
            #     cur.execute("UPDATE walle_core.jobs SET state = 'ROLLBACK' WHERE jobID = %s;", (jobID[0]))
            cur.execute("UPDATE walle_erp.direct_shelve_bills SET state = 'DONE';")
            con.commit()
            cur.close()
            con.close()
        except TypeError:
            print (u"补货任务已经全部为Done")
        except Exception as result:
            print result





    #读取工作站启动机器的ip
    def get_station_windows_ip(self,stationid):
        '''读取工作站启动机器的ip。例
                					|stationid
                		'''
        try:
            con = mdb.connect(ReadMysql().ip, ReadMysql().user, ReadMysql().passwd, ReadMysql().db_1, ReadMysql().port)
            cur = con.cursor()

            cur.execute("SELECT sessionID from walle_core.stations where stationID = %s",(stationid))
            stationip=cur.fetchone()
            con.commit()
            cur.close()
            con.close()
            return stationip[0]
        except:
            print(u"数据库连接失败")



    #读取做过任务的小车ID
    def get_driverunitid(self):
        '''读取做过任务的小车ID
                		'''
        try:
            con =mdb.connect(ReadMysql().ip, ReadMysql().user, ReadMysql().passwd, ReadMysql().db_1, ReadMysql().port)
            cur = con.cursor()

            cur.execute("SELECT driveunitID FROM walle_core.driveunits WHERE mileage != 0;")
            driverunitid=cur.fetchall()
            cur.close()
            con.close()
            return  driverunitid
        except:
            print(u"数据库连接失败")

    # 读取在工作站的小车ID
    def get_driverunitid_in_station(self):
        '''读取在工作站的小车ID
                		'''
        try:
            con = mdb.connect(ReadMysql().ip, ReadMysql().user, ReadMysql().passwd, ReadMysql().db_1, ReadMysql().port)
            cur = con.cursor()
            cur.execute("SELECT driveunitID FROM walle_core.driveunits WHERE mileage != 0 and waypointID like '%4456%'")
            driverunitid = cur.fetchall()
            cur.close()
            con.close()
            return driverunitid
        except:
            print(u"数据库连接失败")

    #获取jobid信息
    def get_jobId(self,ordernumber):
        '''获取jobid信息。例
                					|ordernumber
                		'''
        try:
            con = mdb.connect(ReadMysql().ip, ReadMysql().user, ReadMysql().passwd, ReadMysql().db_1, ReadMysql().port)
            cur = con.cursor()
            cur.execute("SELECT jobID FROM walle_core.picking_jobs j LEFT JOIN walle_erp.picking_orders o ON j.orderID = o.orderID WHERE o.orderNumber =  %s;",(ordernumber))
            jobId = cur.fetchone()
            cur.close()
            con.close()
            return jobId
        except:
            print(u"获取jobid数据库连接失败")



    #获取小车复位信息
    def reset_driverunit(self,ordernumber):
        '''获取小车复位信息。例
                					|ordernumber
                		'''
        stationid = "101"
        try:
            con = mdb.connect(ReadMysql().ip, ReadMysql().user, ReadMysql().passwd, ReadMysql().db_1, ReadMysql().port)
            cur = con.cursor()
            cur.execute("SELECT bucketID FROM walle_core.picking_jobs j LEFT JOIN walle_erp.picking_orders o ON j.orderID = o.orderID WHERE o.orderNumber =  %s;", (ordernumber))
            buketid=cur.fetchone()
            cur.execute("SELECT bucketFaceNum FROM walle_core.picking_jobs j LEFT JOIN walle_erp.picking_orders o ON j.orderID = o.orderID WHERE o.orderNumber =  %s;",(ordernumber))
            bucketFaceNum=cur.fetchone()
            cur.execute("SELECT bucketWaypointID FROM walle_core.picking_jobs   WHERE jobID IN (SELECT jobID FROM walle_core.picking_jobs j LEFT JOIN walle_erp.picking_orders o ON j.orderID = o.orderID WHERE o.orderNumber = %s);",(ordernumber))
            WaypointID=cur.fetchone()
            print(ReadMysql().reset_jobID,(ReadMysql().get_driverunitid())[0][0], buketid[0],stationid,bucketFaceNum[0],WaypointID[0])
            # 插入jobs和resetjob表resetjob
            cur.execute("INSERT INTO `walle_core`.`jobs` (`jobID`, `type`, `state`, `priority`, `timestamp`, `driveunitID`, `createdApp`, `createdDate`, `lastUpdatedApp`, `lastUpdatedDate`) VALUES (%s, 'Reset', 'RESET_INIT', NULL, NULL, %s, NULL, '2018-05-21 18:09:25.391' , NULL, '2018-05-21 18:09:25.391' );",(ReadMysql().reset_jobID,(ReadMysql().get_driverunitid())[0][0]))
            cur.execute("INSERT INTO walle_core.reset_jobs VALUES (%s,%s,%s,%s,'4456499',%s);", (ReadMysql().reset_jobID, buketid[0],stationid,bucketFaceNum[0],WaypointID[0]))
            con.commit()
            cur.close()
            con.close()
        except:
            print(u"数据库连接失败")

