#coding=utf-8
import pymysql as mdb
import time



class ReadMysql(object):


    #获取order状态
    def get_order_status(self,ip, dbuser, dbpasswd, dbport,dbdatabase, orderNumber=""):
        '''获取order状态。例
                					|ordernumber
                		'''

        try:
            con = mdb.connect(ip, dbuser,dbpasswd, dbdatabase, int(dbport))
            cur = con.cursor()
            cur.execute("SELECT state FROM walle_erp.orders WHERE orderNumber= %s;",(orderNumber))
            order_state=cur.fetchone()
            print(order_state[0])
            cur.close()
            con.close()
            return order_state[0]
        except Exception as e:
            print e



    #获取工作站状态
    def get_station_state(self,ip, dbuser, dbpasswd, dbport, dbdatabase,stationname):
        '''获取工作站状态。例
                					|stationnumber
                		'''

        stationid = stationname.split('-')[-1]
        try:
            con = mdb.connect(ip, dbuser, dbpasswd,dbdatabase, int(dbport))
            cur = con.cursor()
            cur.execute("SELECT state FROM walle_core.stations WHERE stationID=%s;", (stationid))
            station_state = cur.fetchone()
            print(station_state[0])
            cur.close()
            con.close()
            return station_state[0]
        except TypeError:
            print(u"请查看传值是否为空或类型错误")
        except Exception as results:
            print(results)


    #获取一个可用的箱号
    def get_box(self,ip, dbuser, dbpasswd, dbport, dbdatabase):
        '''获取一个可用箱号。例
            :return box_list
                		'''
        try:
            con = mdb.connect(ip, dbuser, dbpasswd, dbdatabase, int(dbport))
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
        except Exception as results:
            print(u"读取箱号失败")
            print results



    #获取picking_packages状态绑定箱号信息
    def get_results(self,ip, dbuser, dbpasswd, dbport, dbdatabase,orderNumber=""):
        '''获取picking_packages状态绑定箱号信息。例
                					|ordernumber
                		'''

        try:
            con = mdb.connect(ip, dbuser, dbpasswd, dbdatabase, int(dbport))
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
        except Exception as results:
            print(u"查询数据库失败")
            print(results)





    # 拿结果表的后两条
    def get_results_Two(self,ip, dbuser, dbpasswd, dbport, dbdatabase):
        '''获取最后两条结果
                		'''


        try:
            con = mdb.connect(ip,dbuser,dbpasswd, dbdatabase, int(dbport))
            cur = con.cursor()
            cur.execute("select orderID,quantity,relatedNumber,createdDate FROM walle_core.picking_packages GROUP BY  createdDate DESC limit 2;")
            results = cur.fetchall()
            print(results)
            cur.close()
            con.close()
            return results
        except Exception as results:
            print(u"查询数据库失败")
            print(results)


    #造一条测试数据，把商品数量调为10000
    def create_test_data(self,ip, dbuser, dbpasswd, dbport, dbdatabase):
        '''造一条商品数据并把数量调为一万
        返回skunumber
                		'''


        try:
            con = mdb.connect(ip, dbuser, dbpasswd, dbdatabase, int(dbport))
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
        except Exception as results:
            print(u"数据库连接失败")
            print(results)



     #造一条测试数据，把商品数量调为10000,写入ini，skuno_2
    def create_test_data_2(self,ip, dbuser, dbpasswd, dbport, dbdatabase):
        '''一条商品数据，把商品数量调整为一万，为skuno2
                		'''

        try:
            con = mdb.connect(ip, dbuser, dbpasswd, dbdatabase, int(dbport))
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
        except Exception as results:
            print(u"数据库连接失败")
            print(results)

#创建商品3
    def create_test_data_3(self,ip, dbuser, dbpasswd, dbport, dbdatabase):
        """
        创造一条商品数据，返回为skuno
        :param ip:
        :param dbuser:
        :param dbpasswd:
        :param dbport:
        :param dbdatabase:
        :return:
        """

        try:
            con = mdb.connect(ip, dbuser, dbpasswd, dbdatabase, int(dbport))
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
        except Exception as results:
            print(u"数据库连接失败")
            print results






#创建商品4
    def create_test_data_4(self,ip, dbuser, dbpasswd, dbport, dbdatabase):
        """
        创建商品，并返回一个商品skunumber
        :param ip:
        :param dbuser:
        :param dbpasswd:
        :param dbport:
        :param dbdatabase:
        :return:
        """


        try:
            con = mdb.connect(ip, dbuser, dbpasswd, dbdatabase, int(dbport))
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
        except Exception as results:
            print(u"数据库连接失败")
            print(results)


    #更改ordertype
    def change_ordertype(self,ip, dbuser, dbpasswd, dbport, dbdatabase,ordertype,orderNumber):
        """
        改变订单状态
        :param ip:
        :param dbuser:
        :param dbpasswd:
        :param dbport:
        :param dbdatabase:
        :param ordertype:
        :param orderNumber:
        :return:
        """


        try:
            con = mdb.connect(ip, dbuser, dbpasswd, dbdatabase, int(dbport))
            cur = con.cursor()

            cur.execute("UPDATE walle_erp.orders SET orderType=%s WHERE orderNumber=%s;",(ordertype,orderNumber))
            con.commit()
            cur.close()
            con.close()
            print("Change ordertype success!")
        except Exception as results:
            print(u"数据库连接失败")
            print results

    # 提交订单
    def change_orderstate(self,ip, dbuser, dbpasswd, dbport, dbdatabase,orderNumber):
        """
        提交订单
        :param ip:
        :param dbuser:
        :param dbpasswd:
        :param dbport:
        :param dbdatabase:
        :param orderNumber:
        :return:
        """

        try:
            con = mdb.connect(ip, dbuser, dbpasswd, dbdatabase, int(dbport))
            cur = con.cursor()
            cur.execute("UPDATE walle_erp.orders SET state='PENDING_PROCESS' WHERE orderNumber=%s;", (orderNumber))
            con.commit()
            cur.close()
            con.close()
            print("Change orderstate success!")
        except Exception as results:
            print(u"数据库连接失败")
            print results

    #初始化工作站拣货任务
    def init_station_picking(self,ip, dbuser, dbpasswd, dbport, dbdatabase,ordernumber):
        """
        数据库初始化工作站拣货任务
        :param ip:
        :param dbuser:
        :param dbpasswd:
        :param dbport:
        :param dbdatabase:
        :param ordernumber:
        :return:
        """

        try:
            con = mdb.connect(ip, dbuser, dbpasswd, dbdatabase, int(dbport))
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
        except Exception as results:
            print(u"初始化工作站拣货任务,数据库连接失败")
            print results

    # 初始化工作站补货任务
    def init_station_replenishment(self,ip, dbuser, dbpasswd, dbport, dbdatabase):
        """
        数据库初始化工作站补货任务
        :param ip:
        :param dbuser:
        :param dbpasswd:
        :param dbport:
        :param dbdatabase:
        :return:
        """

        try:
            con = mdb.connect(ip, dbuser, dbpasswd, dbdatabase, int(dbport))
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
    def get_station_windows_ip(self,ip, dbuser, dbpasswd, dbport, dbdatabase,stationname):
        """
        根据工作站名称读取工作站启动机器的ip
        :param ip:
        :param dbuser:
        :param dbpasswd:
        :param dbport:
        :param dbdatabase:
        :param stationname:
        :return:
        """
        stationname = stationname
        stationid = stationname.split('-')[-1]

        try:
            con = mdb.connect(ip, dbuser, dbpasswd, dbdatabase, int(dbport))
            cur = con.cursor()

            cur.execute("SELECT sessionID from walle_core.stations where stationID = %s",(stationid))
            stationip=cur.fetchone()
            con.commit()
            cur.close()
            con.close()
            return stationip[0]
        except Exception as  results:
            print(u"数据库连接失败")
            print results


    #读取做过任务的小车ID
    def get_driverunitid(self,ip, dbuser, dbpasswd, dbport, dbdatabase):
        '''读取做过任务的小车ID
                		'''

        try:
            con =mdb.connect(ip, dbuser, dbpasswd, dbdatabase, int(dbport))
            cur = con.cursor()

            cur.execute("SELECT driveunitID FROM walle_core.driveunits WHERE mileage != 0;")
            driverunitid=cur.fetchall()
            cur.close()
            con.close()
            return  driverunitid
        except Exception as results:
            print(u"数据库连接失败")
            print results

    # 读取在工作站的小车ID
    def get_driverunitid_in_station(self,ip, dbuser, dbpasswd, dbport, dbdatabase):
        """
        获取在工作站的小车id
        :param ip:
        :param dbuser:
        :param dbpasswd:
        :param dbport:
        :param dbdatabase:
        :return: driverunitid
        """
        try:
            con = mdb.connect(ip, dbuser, dbpasswd, dbdatabase, int(dbport))
            cur = con.cursor()
            cur.execute("SELECT driveunitID FROM walle_core.driveunits WHERE mileage != 0 and waypointID like '%4456%' or waypointID like '%4390%'")
            driverunitid = cur.fetchall()
            cur.close()
            con.close()
            return driverunitid
        except Exception as results:
            print(u"数据库连接失败")
            print results

    #获取jobid信息
    def get_jobId(self,ip, dbuser, dbpasswd, dbport, dbdatabase,ordernumber):
        """
        根据订单号获取job号
        :param ip:
        :param dbuser:
        :param dbpasswd:
        :param dbport:
        :param dbdatabase:
        :param ordernumber:
        :return:
        """

        try:
            con = mdb.connect(ip, dbuser, dbpasswd, dbdatabase, int(dbport))
            cur = con.cursor()
            cur.execute("SELECT jobID FROM walle_core.picking_jobs j LEFT JOIN walle_erp.picking_orders o ON j.orderID = o.orderID WHERE o.orderNumber =  %s;",(ordernumber))
            jobId = cur.fetchone()
            cur.close()
            con.close()
            return jobId
        except Exception as e:
            print(u"获取jobid数据库连接失败")
            print e


    #获取小车复位信息
    def reset_driverunit(self,ip, dbuser, dbpasswd, dbport, dbdatabase,ordernumber,stationname,reset_jobID):
        """
        复位在工作站的小车
        :param ip:
        :param dbuser:
        :param dbpasswd:
        :param dbport:
        :param dbdatabase:
        :param ordernumber:
        :param stationname:
        :param reset_jobID:
        :return:
        """


        nowtime = time.strftime("%Y-%m-%d %H:%M:%S")


        stationid = stationname.split('-')[-1]
        rm=ReadMysql()
        try:
            con = mdb.connect(ip, dbuser, dbpasswd, dbdatabase, int(dbport))
            cur = con.cursor()
            cur.execute("SELECT bucketID FROM walle_core.picking_jobs j LEFT JOIN walle_erp.picking_orders o ON j.orderID = o.orderID WHERE o.orderNumber =  %s;", (ordernumber))
            buketid=cur.fetchone()
            cur.execute("SELECT bucketFaceNum FROM walle_core.picking_jobs j LEFT JOIN walle_erp.picking_orders o ON j.orderID = o.orderID WHERE o.orderNumber =  %s;",(ordernumber))
            bucketFaceNum=cur.fetchone()
            cur.execute("SELECT bucketWaypointID FROM walle_core.picking_jobs   WHERE jobID IN (SELECT jobID FROM walle_core.picking_jobs j LEFT JOIN walle_erp.picking_orders o ON j.orderID = o.orderID WHERE o.orderNumber = %s);",(ordernumber))
            WaypointID=cur.fetchone()
            print(reset_jobID,(rm.get_driverunitid(ip, dbuser, dbpasswd, dbport, dbdatabase))[0][0], buketid[0],stationid,bucketFaceNum[0],WaypointID[0])
            # 插入jobs和resetjob表resetjob
            cur.execute("INSERT INTO `walle_core`.`jobs` (`jobID`, `type`, `state`, `priority`, `timestamp`, `driveunitID`, `createdApp`, `createdDate`, `lastUpdatedApp`, `lastUpdatedDate`) VALUES (%s, 'Reset', 'RESET_INIT', NULL, NULL, %s, NULL, '2018-05-21 18:09:25.391' , NULL, '2018-05-21 18:09:25.391' );",(reset_jobID,(rm.get_driverunitid(ip, dbuser, dbpasswd, dbport, dbdatabase))[0][0]))
            cur.execute("INSERT INTO walle_core.reset_jobs VALUES (%s,%s,%s,%s,'4456499',%s);", (reset_jobID, buketid[0],stationid,bucketFaceNum[0],WaypointID[0]))
            con.commit()
            cur.close()
            con.close()
        except Exception as results:
            print results


    #获取货架
    def get_bucketNumber(self,ip, dbuser, dbpasswd, dbport, dbdatabase,skunumber):
        """
        根据商品号获取商品货架位置
        :param ip:
        :param dbuser:
        :param dbpasswd:
        :param dbport:
        :param dbdatabase:
        :param skunumber:
        :return:
        """


        try:
            con = mdb.connect(ip, dbuser, dbpasswd, dbdatabase, int(dbport))
            cur = con.cursor()
            cur.execute("SELECT bucketSlotID  from walle_core.bucket_slot_skus WHERE skuID in  ( SELECT skuID from walle_erp.skus WHERE skuNumber = %s);",(skunumber))
            buckernu=cur.fetchone()[0]
            print buckernu
            b=buckernu.split("-")
            cur.close()
            con.close()
            return b[0]
        except Exception as e:
            print e

            # 拿结果表的后三条

    def get_results_three(self,ip, dbuser, dbpasswd, dbport, dbdatabase):
        """
        拿最后三条数据
        :param ip:
        :param dbuser:
        :param dbpasswd:
        :param dbport:
        :param dbdatabase:
        :return:
        """

        con = mdb.connect(ip, dbuser, dbpasswd, dbdatabase, int(dbport))
        cur = con.cursor()
        cur.execute(
            "select orderID,quantity,relatedNumber FROM walle_core.picking_packages GROUP BY  createdDate DESC limit 3;")
        results = cur.fetchall()
        cur.close()
        con.close()
        return results

    #查找盘点订单号
    def get_countCheck_order(self,ip, dbuser, dbpasswd, dbport, dbdatabase):
        """
        查找盘点订单号
        :param ip:
        :param dbuser:
        :param dbpasswd:
        :param dbport:
        :param dbdatabase:
        :return: 列表
        """
        try:
            con = mdb.connect(ip, dbuser, dbpasswd, dbdatabase, int(dbport))
            cur = con.cursor()
            cur.execute(
                "select count_checks.countCheckID from walle_erp.count_checks where state='DOING';")
            results = cur.fetchall()
            cur.close()
            con.close()
            li=[]
            for i in results:
                for a in i:
                    li.append(a)
            print(li)
            return li
        except Exception as result:
            print(result)

# if __name__ == '__main__':
#     a=ReadMysql()
#     a.get_countCheck_order("192.168.21.14","root","","6014","walle_erp")
