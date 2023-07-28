from pypipeline.core.Destination import Destination 
 
import taos


config={
"logPath":"/yourapp.log",
"redis":" jssqlredis",
"redis_host":"jssqlredis",
"redis_port":6379,
"sqlserver_loader":"E:\\workdir\\MQTTJSql\\JSBaseTDSSO_test\\bin\\Debug\\JSBaseTDSSO_test.exe",

"taos_host":"e7c3cdeeee88",
"taos_user":"root",

"taos_pwd":"taosdata",
}

conn = {}


def pSaveSensorDataToTaos(u, s, g,    sensor, sensor_type, r, gateway):
    sensor_value ="";
    for x in r["d"]:
        v = "%s:%s" %( x["d"], x["v"])
        if(sensor_value ==""):
            sensor_value =  v; 
        else:
            sensor_value = sensor_value +","+v; 
    SaveSensorDataToTaos(u, s, g,  r["dt"],  sensor, sensor_type, sensor_value, gateway, r["c"])

def SaveSensorDataToTaos(u, s, g,  dt,  sensor, sensor_type, sensor_value, gateway, amount):
    #print(nlid, node_code, client_id, sts, data);
    #InitTaos()
    #print(u, s, g,  dt,  sensor, sensor_type, sensor_value, gateway, amount);
    c1 = conn.cursor()
    c1.execute('use appiot;\r\n') 
    #s= "CREATE TABLE  IF NOT EXISTS SensorData%s  USING SensorData TAGS ('%s');\r\n" %( nlid, nlid )

    s2 = "CREATE TABLE  IF NOT EXISTS sensor_data2_"+u +"_" +s +"_" +g+\
        "  USING sensor_data2 TAGS (  '"+u+"','"+s+"','"+g+"');\r\n"  # %( nlid, nlid )
    #print(s2);
    c1.execute(s2)
    sqlcmd = ['insert into sensor_data2_%s_%s_%s  values' % (u, s,  g)]
    #print(sqlcmd);
    sqlcmd.append('(now, \'%s\', %s, \'%s\', \'%s\', \'%s\', \'%s\');' %
                  (dt, amount, sensor, sensor_type, sensor_value, gateway))
    print(' '.join(sqlcmd));
    c1.execute(' '.join(sqlcmd)) 
 
 
# If you want to use a specific client id, use
# mqttc = mqtt.Client("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.

 

class SaveSensorData(Destination):
    def __init__(self, plumber, params):
        super().__init__(plumber, params)
        self.topic = params["topic"]
        global conn;
        conn = taos.connect(host=config["taos_host"],
                    user=config["taos_user"], password=config["taos_pwd"])

    def process(self, exchange):
        #print("\nLog: " + self.channel + "\n" + str(exchange) + "\n")
        #exchange.in_msg.body
        #pSaveSensorDataToTaos(u, s, g,    sensor, sensor_type, r, gateway)
        #sendMqttMessage(self.topic , exchange.in_msg.body) 