#coding=utf-8
import time
import requests
import datetime
import ReadMysql

class SendOrder(object):
	# def __init__(self,ip,wmsport,username,password):
	# 	self.ip = ip
	# 	self.port= wmsport
	# 	self.username= username
	# 	self.password= password
	# 	self.wms_login_url = "http://" + self.ip + ":" + str(self.port) + "/walle-wms/login"
	# 	self.wms_keeporder_url = "http://" + self.ip + ":" + str(self.port) + "/walle-wms/order/newOrder"
	# 	self.wms_submitOrders_url =  "http://" + self.ip + ":" + str(self.port) + "/walle-wms/order/submitOrders"
	# 	self.orderno=datetime.datetime.now().strftime('%m%d%H%M%S%f')
	# 	self.shipDeadline=time.strftime("%Y-%m-%d"+"T"+"%H:%M:%S"+ ".280+0800")
	# 	self.orderDate=time.strftime("%Y-%m-%d"+"T"+"%H:%M:%S"+ ".234Z")

	def send_order_OneOder_OneSku(self,ip,wmsport,username,password,skuID,skuNumber,name,quantity,eans):
		'''通过wms下单。例
					| skuID          | skuNumber               | name   | quantity   | eans   |
		'''



		wms_login_url = "http://" + ip + ":" + str(wmsport) + "/walle-wms/login"
		wms_keeporder_url = "http://" + ip + ":" + str(wmsport) + "/walle-wms/order/newOrder"
		wms_submitOrders_url = "http://" + ip + ":" + str(wmsport) + "/walle-wms/order/submitOrders"
		orderno = datetime.datetime.now().strftime('%m%d%H%M%S%f')
		shipDeadline = time.strftime("%Y-%m-%d" + "T" + "%H:%M:%S" + ".280+0800")
		orderDate = time.strftime("%Y-%m-%d" + "T" + "%H:%M:%S" + ".234Z")

		session=requests.Session()
		print wms_login_url
		json_data={"account":username,"password":password}
		login=session.post(wms_login_url,json=json_data)
		print u"登录接口返回结果为：" + login.text
		print u"登录接口返回cookie为:"
		print login.cookies

		data_keeporder={
	"orderID": None,
	"orderNumber": orderno,
	"customerID": "100",
	"orderDate": orderDate,
	"shipDate": None,
		"shipFromName": None,
	"shipFromPhone": None,
	"shipFromAddress": None,
	"shipFromZipcode": None,
	"shipToName": None,
	"shipToPhone": None,
	"shipToAddress": None,
	"shipToZipcode": None,
	"logisticsCompany": None,
	"expressPaymentWay": None,
	"orderDetails": [{
		"skuID": skuID,
		"skuNumber":skuNumber,
		"name": name,
		"quantity": quantity,
		"orderID": None,
		"fulfillQuantity": 0,
		"pickingQuantity": 1999998,
		"storageQuantity": 0,
		"externalID": None,
		"price": None,
		"eans": eans
	}],
	"toDelOrderDetails": [],
	"shipFromAddressID": "",
	"price": None,
	"isTaobaoOrder": False,
	"externalState": None,
	"ShipToStoreName": None,
	"orderType": None,
	"shipDeadline": shipDeadline,
	"splittable": True
}

		b=session.post(wms_keeporder_url,json=data_keeporder)
		print u"下单接口返回结果为："+b.text
		print u"订单号为：" + orderno
		print datetime.datetime.now()
		return orderno

	def clean_countcheck(self,ip, dbuser, dbpasswd, dbport, dbdatabase,wmsport,username,password):
		try:
			rm=ReadMysql.ReadMysql()
			countCheck_order=rm.get_countCheck_order(ip, dbuser, dbpasswd, dbport, dbdatabase)
			wms_countcheck_delete_url= "http://" + ip + ":" + str(wmsport) +"/walle-wms/countcheck/delete"
			wms_login_url = "http://" + ip + ":" + str(wmsport) + "/walle-wms/login"
			session = requests.Session()
			json_data = {"account": username, "password": password}
			json_data1= countCheck_order
			login = session.post(wms_login_url, json=json_data)
			print u"登录接口返回结果为：" + login.text
			print u"登录接口返回cookie为:"
			print login.cookies
			b = session.post(wms_countcheck_delete_url, json=json_data1)
			print u"接口返回结果为：" + b.text
		except Exception as results:
			print(results)



# 	def send_order_OneOrder_TwoSku(self,skuID,skuNumber,name,quantity,eans):
# 		'''通过wms下单。例
# 					| skuID          | skuNumber               | name   | quantity   | eans   |
# 		'''
# 		session=requests.Session()
# 		print self.wms_login_url
# 		json_data={"account":self.username,"password":self.password}
# 		login=session.post(self.wms_login_url,json=json_data)
# 		print u"登录接口返回结果为：" + login.text
# 		print u"登录接口返回cookie为:"
# 		print login.cookies
#
# 		data_keeporder={
# 	"orderID": None,
# 	"orderNumber": self.orderno,
# 	"customerID": "100",
# 	"orderDate": self.orderDate,
# 	"shipDate": None,
# 	"shipFromName": None,
# 	"shipFromPhone": None,
# 	"shipFromAddress": None,
# 	"shipFromZipcode": None,
# 	"shipToName": None,
# 	"shipToPhone": None,
# 	"shipToAddress": None,
# 	"shipToZipcode": None,
# 	"logisticsCompany": None,
# 	"expressPaymentWay": None,
# 	"orderDetails": [{
# 		"skuID": skuID,
# 		"skuNumber": skuNumber,
# 		"name": name,
# 		"quantity":quantity,
# 		"orderID": None,
# 		"fulfillQuantity": 0,
# 		"pickingQuantity": 1999906,
# 		"storageQuantity": 0,
# 		"externalID": None,
# 		"price": None,
# 		"eans": ["6922629722580"]
# 	}, {
# 		"skuID": "000000993119_6159350",
# 		"skuNumber": "000000993119",
# 		"name": "男款个性休闲舒适裤子黑色",
# 		"quantity": 6,
# 		"orderID": None,
# 		"fulfillQuantity": 0,
# 		"pickingQuantity": 10000,
# 		"storageQuantity": 0,
# 		"externalID": None,
# 		"price": None,
# 		"eans": eans
# 	}],
# 	"toDelOrderDetails": [],
# 	"shipFromAddressID": "",
# 	"price": None,
# 	"isTaobaoOrder": "false",
# 	"externalState": None,
# 	"ShipToStoreName": None,
# 	"orderType": None,
# 	"shipDeadline": self.shipDeadline,
# 	"splittable": True
# }
#
# 		b=session.post(self.wms_keeporder_url,json=data_keeporder)
# 		print u"下单接口返回结果为："+b.text
# 		print u"订单号为：" + self.orderno
# 		print datetime.datetime.now()
# 		return self.orderno

# if __name__ == '__main__':
# 	#"000000993119_6159350", "000000993119", "男款个性休闲舒适裤子黑色", "3", "[000000993119]"
# 	a=SendOrder()
# 	a.clean_countcheck("192.168.21.14","root","","6014","walle_erp",6054,"admin","1")