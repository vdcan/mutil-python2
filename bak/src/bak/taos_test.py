
import datetime
import my_config;
import taos
conn =  taos.connect(host=my_config.config["taos_host"], user=my_config.config["taos_user"], password=my_config.config["taos_pwd"] )

c1 = conn.cursor()
# Create a database
c1.execute('create database if not exists db')
c1.execute('use db')
# Create a table
c1.execute('create table if not exists tb (ts timestamp, temperature int, humidity float)')
# Insert data
start_time = datetime.datetime(2019, 11, 1)
affected_rows = c1.execute('insert into tb values (\'%s\', 0, 0.0)' %start_time)
# Insert data in batch
time_interval = datetime.timedelta(seconds=60)
sqlcmd = ['insert into tb values']
for irow in range(1,11):
    start_time += time_interval
    sqlcmd.append('(\'%s\', %d, %f)' %(start_time, irow, irow*1.2))
affected_rows += c1.execute(' '.join(sqlcmd))
print("inserted %s records" % affected_rows)