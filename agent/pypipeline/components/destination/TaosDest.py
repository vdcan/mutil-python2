from pypipeline.core.Destination import Destination 
 
import taos
import my_config
from pypipeline.core.Message import Message
 
import taos

import math
import copy
from datetime import datetime, timedelta
conn = {} 
def insertData(template, data):
    file1 = open("templates/" +template , "r")
    Lines = file1.readlines()
    file1.close(); 
    c1 = conn.cursor()
    # Strips the newline character
    for line in Lines: 
        for d in data:
            #print(d)
            sqlcmd =line.strip().format(**d)
            print(sqlcmd)
            c1.execute(sqlcmd)
 

class SaveSensorData(Destination):
    def __init__(self, plumber, params):
        super().__init__(plumber, params)
        self.template = params["template"]
        global conn;
        conn = taos.connect(host=my_config.config["taos_host"],
                    user=my_config.config["taos_user"], password=my_config.config["taos_pwd"])

    def process(self, exchange):
        #print("\nLog: " + self.channel + "\n" + str(exchange) + "\n")
        #exchange.in_msg.body
        #print(self.template , exchange.out_msg.body)
        m = Message();
        if(len(exchange.out_msg.body) >0):
            insertData(self.template , exchange.out_msg.body);
            m.body = "inserted";
        else:
            m.body = "array empyt";
        exchange.out_msg = m;
        #pSaveSensorDataToTaos(u, s, g,    sensor, sensor_type, r, gateway)
        #sendMqttMessage(self.topic , exchange.in_msg.body) 