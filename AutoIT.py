#coding=utf-8

import win32com.client

class AutoIT(object):
    def __init__(self):
        self.autoit = win32com.client.Dispatch("AutoItX3.Control")

    def getText(self,stationtitle,control):
        autoit = win32com.client.Dispatch("AutoItX3.Control")
        autoit.WinActive(stationtitle, "")
        autoit.ControlClick(stationtitle,"",control)
        a=autoit.ControlGetText(stationtitle, "", control)
        print "asdads"
        print a
        return a
a=AutoIT()
print  a.getText("瓦力智能系统-102","Static5")
