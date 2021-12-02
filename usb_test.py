from re import findall
from sys import path
import time
from PyQt5 import QtCore
import wmi

class USB(QtCore.QObject):

    def __init__(self,parent=None):
        super(USB,self).__init__(parent)
        self.status=None
        self.path=None
        self.usb_ports_refresh()

    def usb_ports_refresh(self):
        c = wmi.WMI()
        self.path=None
        for disk in c.Win32_LogicalDisk():
            if disk.Description== "Removable Disk":
                self.path=disk.Name+"/newfile.txt"

    def built_str(self,n):
        init_str="\x14\x22\x16\x14"
        data=""
        for i in range(0,n):
            data+=init_str
        return(data)
    
    def change_path(self):
        self.path=None

    def Wspeed_test(self,path,data):
        d=data
        try:
            with open(path,"w") as file:
                file.write("")
                start = time.time()
                file.write(d)
                stop=time.time()
                file.close()
            self.status=("OK  Speed: "+str((round(12/(stop-start),3)))+" Mb/s")
        except Exception as e:
            if str(e)[1:8]=="Errno 2":
                self.status=("Drive Not Found")
            else:
                self.status=("Please add a USB Path")
