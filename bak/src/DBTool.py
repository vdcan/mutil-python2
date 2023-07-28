#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright (c) 2010-2013 Roger Light <roger@atchoo.org>
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Distribution License v1.0
# which accompanies this distribution.
#
# The Eclipse Distribution License is available at
#   http://www.eclipse.org/org/documents/edl-v10.php.
#
# Contributors:
#    Roger Light - initial implementation
# Copyright (c) 2010,2011 Roger Light <roger@atchoo.org>
# All rights reserved.

# This shows a simple example of an MQTT subscriber.
 
import redis
import json  
import pyodbc as po
import pandas as pd
import my_config; 
import mysql.connector


 
# Connection variables
server = my_config.config["mssql_host"]
database = my_config.config["mssql_db"]
username = my_config.config["mssql_user"]
password = my_config.config["mssql_pwd"]

REDIS = redis.Redis(host= my_config.config["redis_host"], port=my_config.config["redis_port"]) 
def CPT(proc, key): 
    try:
        # Connection string
        cnxn = po.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
                server+';DATABASE='+database+';UID='+username+';PWD=' + password)
        cur = cnxn.cursor()
    
        # Prepare the stored procedure execution script and parameter values
        #storedProc = "Exec [Sales].[Mtb_GetCustomers] @SearchText = ?, @MaximumRowsToReturn = ?"
        storedProc = "Exec "+proc;
        #params = ("And", 10)
        params = ( )
        df_list = []
    
        # Execute Stored Procedure With Parameters
        #rows = cur.execute( storedProc, params ).fetchall()
        cur.execute( storedProc, params );
        #print(storedProc)
        ka= key.split(",");
        i =0;
        while True:    
            df_list = []
            rows = cur.fetchall()
            # process all result sets in the same place
            #columns = [column[0] for column in cur.description]
            #df_list.append(pd.DataFrame.from_records(rows, columns=columns))
            #df = pd.DataFrame.from_records(rows,columns=columns)
            #print(1, df.head())
            insertObject = []
            columnNames = [column[0] for column in cur.description]
            #columnNames.append("test")
            #print(columnNames);
            #print(rows);
            for record in rows:
                insertObject.append( dict( zip( columnNames , record ) ) )
            SaveDataToRedis(ka[i],insertObject)
            i = i +1;
            if not cur.nextset():
                break 
        
        cur.close() 
        del cur
        
        # Close the database connection
        cnxn.close()
        #v = str(dict( insertObject));
        #v = v.replace("'","\"")
        #REDIS.set(key, v);   
        #print(str(insertObject))
    except Exception as e:
        print("Errorr31: %s" % e)

def CPT2(proc, key): 
    try:
        # Connection string
        cnxn = po.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
                server+';DATABASE='+database+';UID='+username+';PWD=' + password)
        cur = cnxn.cursor()
    
        # Prepare the stored procedure execution script and parameter values
        #storedProc = "Exec [Sales].[Mtb_GetCustomers] @SearchText = ?, @MaximumRowsToReturn = ?"
        storedProc = "Exec "+proc;
        #params = ("And", 10)
        params = ( )
        df_list = []
    
        # Execute Stored Procedure With Parameters
        #rows = cur.execute( storedProc, params ).fetchall()
        cur.execute( storedProc, params );
        #print(storedProc)
        ka= key.split(",");
        i =0;
        while True:    
            df_list = []
            rows = cur.fetchall() 
            #insertObject = []
            columnNames = [column[0] for column in cur.description]
            #columnNames.append("test")
            #print(columnNames);
            #print(rows);
            for record in rows:
                #insertObject.append( dict( zip( columnNames , record ) ) )
                SaveDataToRedisRange(ka[i], dict( zip( columnNames , record ) ))
            #SaveDataToRedis(ka[i],insertObject)
            i = i +1;
            if not cur.nextset():
                break 
        
        cur.close() 
        del cur
        
        # Close the database connection
        cnxn.close() 
    except Exception as e:
        print("Errorr31: %s" % e)
def SaveDataToRedisRange(key, insertObject):
    #print(key);
    v = str( insertObject );
    v = v.replace("'","\"")
    v=v.replace("Decimal(\"", "");
    v=v.replace("\")", "");

    v=v.replace("datetime.datetime(", "\"");
    v=v.replace("),", "\",");
    #print(v)
    REDIS.lpush(key, v);   
def SaveDataToRedis(key, insertObject):
    #print(key);
    v = str( insertObject );
    v = v.replace("'","\"")
    v=v.replace("Decimal(\"", "");
    v=v.replace("\")", "");

    v=v.replace("datetime.datetime(", "\"");
    v=v.replace("),", "\",");
    #print(v)
    REDIS.set(key, v);   
def CST(table_name, conn= None, k = ""): 
    try:
        # Connection string
        print(k);
        if(conn==None):
            cnxn = po.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
                server+';DATABASE='+database+';UID='+username+';PWD=' + password)
        else:
            cnxn = conn;
        cur = cnxn.cursor()
        if(k ==""):
            key =  table_name;
        else    :
            key = k;
        #key=table_name     
        # Prepare the stored procedure execution script and parameter values
        #storedProc = "Exec [Sales].[Mtb_GetCustomers] @SearchText = ?, @MaximumRowsToReturn = ?"
        storedProc = "SELECT * FROM "+ table_name;
        #print(storedProc);
        #params = ("And", 10)
        params = ( )
        df_list = []
        #print(storedProc)
    
        # Execute Stored Procedure With Parameters
        #rows = cur.execute( storedProc, params ).fetchall()
        rc = cur.execute( storedProc );
        #print(rc.rowcount );
        while 1 > 0:    
            df_list = []
            rows = cur.fetchall()
            #print(rows)
            insertObject = []
            columnNames = [column[0] for column in cur.description]
            #print(columnNames);
            for record in rows: 
                v = str(dict( zip( columnNames ,  record) ));
                v = v.replace("'","\"")
                v=v.replace("Decimal(\"", "");
                v=v.replace("\")", "");
                
                v=v.replace("datetime.datetime(", "\"");
                v=v.replace("),", "\",");
                #print(v);
                REDIS.lpush(key, v);  
            
            #print(record);
            #print(v);
            #exit();
            if not cur.nextset():
                break 
        
        cur.close() 
        del cur
        
        # Close the database connection
        if(conn == None):
            cnxn.close()
        
        #print(str(insertObject))
    except Exception as e:
        print("Error1: %s" % e)


#CST("v_node_node_client_id") 

def CST2(table_name, conn= None, k = ""): 
    try:
        # Connection string
        if(conn==None):
            cnxn = po.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
                server+';DATABASE='+database+';UID='+username+';PWD=' + password)
        else:
            cnxn = conn;
        cur = cnxn.cursor()
        if(k ==""):
            key =  table_name;
        else    :
            key = k;
        # Prepare the stored procedure execution script and parameter values
        #storedProc = "Exec [Sales].[Mtb_GetCustomers] @SearchText = ?, @MaximumRowsToReturn = ?"
        storedProc = "SELECT * FROM "+ table_name;
        #params = ("And", 10)
        params = ( )
        df_list = []
        print(storedProc)
        counter =0;
    
        # Execute Stored Procedure With Parameters
        #rows = cur.execute( storedProc, params ).fetchall()
        cur.execute( storedProc );
        result=""
        while True:    
            df_list = []
            rows = cur.fetchall()
            insertObject = []
            columnNames = [column[0] for column in cur.description]
            #print(columnNames);
            rowStr="";
            for record in rows:
                v = str(dict( zip( columnNames , record ) ));
                v = v.replace("'","\"")
                rowStr = rowStr+v+",";
                #REDIS.lpush(key,v );  
            if(counter == 0):
                result="\"Table\":["
            else:
                result=result+",\"Table" + str(counter) + "\":[";
            result=result+rowStr+"]";
            if not cur.nextset():
                break 
            counter = counter +1;
        cur.close() 
        del cur
        
        # Close the database connection
        if(conn == None):
            cnxn.close()
        result = result.replace("},]", "}]");
        REDIS.lpush(key,result );  
        #print(str(insertObject))
    except Exception as e:
        print("Error3: %s" % e)



def CSTBC(table_name, column): 
    try:
        # Connection string
        cnxn = po.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
                server+';DATABASE='+database+';UID='+username+';PWD=' + password)
        cur = cnxn.cursor()
        #cs = columns.split(',')
        #key = "test_"+table_name;
        # Prepare the stored procedure execution script and parameter values
        #storedProc = "Exec [Sales].[Mtb_GetCustomers] @SearchText = ?, @MaximumRowsToReturn = ?"
        storedProc = "SELECT distinct "+column+" FROM "+ table_name +" group by "+column;
        #params = ("And", 10)
        params = ( )
        df_list = []
        print(storedProc)
    
        # Execute Stored Procedure With Parameters
        #rows = cur.execute( storedProc, params ).fetchall()
        cur.execute( storedProc );


        df_list = []
        rows = cur.fetchall()
        # process all result sets in the same place 
        insertObject = []
        columnNames = [column[0] for column in cur.description]  

        # Process each record individually
        for rec in rows:
            #print(rec[0])
            CST(table_name +' where '+column+' =\''+str(rec[0])+'\'', cnxn, table_name+":"+str(rec[0]))
            #exit()

        #print(columnNames);
        #for record in columnNames:
        #    REDIS.lpush(key, str(dict( zip( columnNames , record ) )));   
         
        cur.close() 
        del cur
        
        # Close the database connection
        cnxn.close()
        
        #print(str(insertObject))
    except Exception as e:
        print("Error2: %s" % e)

#CPT('usp_protocol_detail_list','test1');    
#CST("ddl");   
#CSTBC("v_alarm_method", "alarm_code")

#CSTBC("v_node_node_client_id","node_client_id");
def mysql_redis(table):


    mydb = mysql.connector.connect(
    host= my_config.config["mysql_host"],
    user= my_config.config["mysql_user"],
    password= my_config.config["mysql_pwd"],
    database= my_config.config["db"]
    )

    print(mydb) 

    cur = mydb.cursor()

    cur.execute("SELECT * FROM "+table)

    rows = cur.fetchall()


    insertObject = []
    columnNames = [column[0] for column in cur.description]  
    #print(columnNames);
    # Process each record individually
    for rec in rows:
        #print(rec)
        v = str(dict( zip( columnNames , rec ) ));
        v = v.replace("'","\"")
        v = v.replace(": None,",": \"\",")
        v = v.replace(": datetime",": \" datetime")
        v = v.replace("),",")\",")
        REDIS.lpush(table, v);  
        #CST(table_name, cnxn, table_name+":"+str(rec[0]))

    #print(columnNames);
    #for record in columnNames:
    #    REDIS.lpush(key, str(dict( zip( columnNames , record ) )));   

    cur.close() 
    del cur

    # Close the database connection
    mydb.close()