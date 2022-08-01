#------------------------------------------
#--- Author: Chanthujan Chandrakumar
#--- Date: 08th Feb 2022
#--- Version: 1.0
#--- Python Ver: 2.7
#------------------------------------------




import time
from datetime import datetime
from array import *
import json
 


def alert_Message(AlertType, host, AlertData): #this function defines the message format for the alert message
    Alertmsg = {}
    Alertmsg['AlertType'] = AlertType
    Alertmsg['Sensor_ID'] = host
    Alertmsg['Date'] = (datetime.today()).strftime("%d-%b-%Y %H:%M:%S:%f")
    Alertmsg['AlertData'] = AlertData
    Alert_json_data = json.dumps(Alertmsg)
    return str(Alert_json_data)
