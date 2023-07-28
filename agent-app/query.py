import time
from ctypes import *

import taos    

config={
"logPath":"/yourapp.log",
"redis":" jssqlredis",
"redis_host":"jssqlredis",
"redis_port":6379, 
"taos_host":"e7c3cdeeee88",
"taos_user":"root",

"taos_pwd":"taosdata",
}

#import classes;
#import DataInit;

#print(my_config.config)

conn = taos.connect(host=config["taos_host"],user=config["taos_user"], password=config["taos_pwd"])
 

def fetch_all_demo():
    result: taos.TaosResult = conn.query("select  * from appiot.sensor_data order by add_on  desc limit 0, 10")
    rows = result.fetch_all_into_dict()
    print("row count:", result.row_count)
    print("===============all data===================")
    for entry in rows: 
        entry['add_on'] = int(entry['add_on'].timestamp())
    print(rows)
  
if __name__ == "__main__":
    fetch_all_demo( )