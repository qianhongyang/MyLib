#coding=utf-8
import time
import json
import xlrd
import requests
import datetime

class SendOrder():
	def __init__(self):
		self.filepath = "D:\\conf.xls"
		xls_file = xlrd.open_workbook(filename=self.filepath)
		self.table=xls_file.sheet_by_index(0)
		self.ip=self.table.cell_value(2,1)
		self.port=self.table.cell_value(2,2)
		self.username=self.table.cell_value(2,5)
		self.password=self.table.cell_value(2,6)
		self.wms_login_url = "http://" + self.ip + ":" + self.port + "/walle-wms/login"
		self.wms_keeporder_url = "http://" + self.ip + ":" + self.port + "/walle-wms/order/newOrder"
		self.wms_submitOrders_url =  "http://" + self.ip + ":" + self.port + "/walle-wms/order/submitOrders"
		self.orderno=datetime.datetime.now().strftime('%m%d%H%M%S%f')
		self.shipDeadline=time.strftime("%Y-%m-%d"+"T"+"%H:%M:%S"+ ".280+0800")
		self.orderDate=time.strftime("%Y-%m-%d"+"T"+"%H:%M:%S"+ ".234Z")

	def send_order(self,skuID,skuNumber,name,quantity,eans):
		'''通过wms下单。例
					| skuID          | skuNumber               | name   | quantity   | eans   |
		'''
		session=requests.Session()
		print self.wms_login_url
		json_data={"account":self.username,"password":self.password}
		login=session.post(self.wms_login_url,json=json_data)
		print u"登录接口返回结果为：" + login.text
		print u"登录接口返回cookie为:"
		print login.cookies

		data_keeporder={
	"orderID": None,
	"orderNumber": self.orderno,
	"customerID": "100",
	"orderDate": self.orderDate,
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
	"shipDeadline": self.shipDeadline,
	"splittable": True
}

		b=session.post(self.wms_keeporder_url,json=data_keeporder)
		print u"下单接口返回结果为："+b.text
		print u"订单号为：" + self.orderno
		print datetime.datetime.now()
		return self.orderno




