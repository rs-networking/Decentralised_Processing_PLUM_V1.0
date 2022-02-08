#------------------------------------------
#--- Author: Chanthujan Chandrakumar
#--- Date: 08th Feb 2022
#--- Version: 1.0
#--- Python Ver: 2.7
#------------------------------------------


import socket as s
import time
from datetime import datetime
from array import *
import json 
from msg_format import alert_Message




def tcp_Sender(nodeList, host, PORT, AlertType , AlertData):
    for IP in nodeList:
        try:
            message = alert_Message(AlertType, host , AlertData)
            sock = s.socket(s.AF_INET, s.SOCK_STREAM) 
            sock.connect((str(IP) , PORT))
            sock.sendall(str(message))  
        except Exception:   
            print("Unable to send to " + str(IP))
            pass    






