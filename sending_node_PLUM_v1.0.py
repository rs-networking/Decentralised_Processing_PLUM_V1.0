#------------------------------------------
#--- Author: Chanthujan Chandrakumar
#--- Date: 08th Feb 2022
#--- Version: 1.0
#--- Python Ver: 2.7
#------------------------------------------

import socket as s
import math as M
import numpy as np
import time
from datetime import datetime
from tcp_sender import tcp_Sender
from array import *
import json
import uuid
import threading 
import sys



################################Sensor Variables###############################
host =  raw_input("Please enter the IP address of the sender RS4D:")
thr_val = int(input("Please enter threshold for the detection:"))     
port = 8888
TCP_port  = 5005
###############################################################################


###############################Defining the node list #########################
nodeList =[]


with open("node_list.txt", "r") as file:
    newline_break = ""
    for readline in file: 
        line_strip = readline.strip()
        newline_break = line_strip +" "+ newline_break 
    
nodeList= newline_break.split()


###############################################################################


##############################MQTT Topic Declaration###########################
MQTT_Topic_EEW = "EEW/" + host +"/Alert"
###############################################################################


##############################Socket Declaration for UDP and Incoming Data ####
sock = s.socket(s.AF_INET, s.SOCK_DGRAM)
sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
sock.bind((host, port))


###############################################################################


print('Starting the Sensor ' + host + " !!!")


############################## Code Variable Declaration ###################### 
x=[]
alert_data = [] #array initiated to store one min data
time_rec = 0

###############################################################################

counter_1 = 0 

def alarm_event(in_data, threshold, window_size): # Function which alerts people
    global alert_data
    global x
    global counter_1 
    for i in in_data:
        if (i >= threshold):
            alert_data.append(i)
        else:
            alert_data = []
        if( len(alert_data) == window_size):
            print("threshold passed,  Local alert")
            alert_data = []
            counter_1 += 1                                                                                   
            text_file = open("sender_raj.txt", "a+")                                                         
            text_file.write(str(counter_1))                                                                  
            text_file.write("\n")                                                                            
            text_file.close() 
            tcp_Sender(nodeList, host, TCP_port, "Alert", "Threshold Exceeded!!!")


def sqre_func(L): #Function which returns the average of signal readings
    squared_num = [number ** 2 for number in L]
    return squared_num




def magnitude_func(L): #Function which returns the average of signal readings
    sense_data = s[2:len(s)]
    sense_int  = [int(i) for i in sense_data]
    mean       = sum(sense_int)/25
    count      = [ x - mean for x in sense_int]
    mag_list        = np.square(count) 
    return mag_list




#print ("Active senosr List:", nodeList)


while 1:  # loop forever
    data, addr = sock.recvfrom(1024)  # wait to receive data
    s = data.decode('UTF-8').strip("'{}").split(', ')  # clean and listify the data
    if (s[0] == "ENN'"):
        time_rec = s[1] 
        mag_NS        = magnitude_func(s) 
     
    elif (s[0] == "ENZ'"):
        if(s[1] == time_rec):
            mag_Z        =  magnitude_func(s)


    elif (s[0] == "ENE'"):    
        if(s[1] == time_rec):
            mag_EW        = magnitude_func(s)
            res_mag1 = np.add(mag_Z, mag_NS)
            res_mag  = np.sqrt(np.add(res_mag1, mag_EW))   
            alarm_event(res_mag,thr_val,25)
            print("Resultant vector:", res_mag)
