# This file is part of https://github.com/jainamoswal/Flask-Example.
# Usage covered in <IDC lICENSE>
# Jainam Oswal. <jainam.me> 


# Import Libraries 
from app import app
from flask import jsonify
import cx_Oracle
import json
import numpy as np 
import pandas as pd

from flask import request
 

connection = cx_Oracle.connect(user="ooldrtest4", password="a268261a456b8a18ed68f9ed8",
                               dsn="racorad43-scan.test.intranet:1521/svc_o2test1")                               
  

query_resource="""

select  * from v_resource2 
""" 
query_place="""

select 
n1.*
from hv_address addr
join externalsystemplacesi esp on esp.externalid = addr.address_alias_id 
INNER JOIN v_resource2 n1 on n1.TO_UNIQUEID= esp.uniqueid and n1.to_type ='Place' 
where addr.address_alias_id = 
""" 

def replaceNone(data_dict,v,rv):
    for key in data_dict.keys():
        if data_dict[key] == v:
            data_dict[key] = rv
        elif type(data_dict[key]) is dict:
            replaceNone(data_dict[key],v,rv)


def query(sql):
  print(sql);
  cursor = connection.cursor()
  cursor.execute(sql)
  rows = [x for x in cursor]
  cols = [x[0] for x in cursor.description]
  df= pd.DataFrame( {"cols": cols})
  #print(df.cols);
  #df.cols = df.cols+ df.groupby("cols").cumcount().astype(str);
  df.cols = df.cols+ removeZero(df.groupby("cols").cumcount()) ;
  #print(df); 
  songs = []
  for row in rows:
    song = {}
    for prop, val in zip(df.cols, row):
      song[prop] = val
    songs.append(song)
  # Create a string representation of your array of songs.
  songsJSON = json.dumps(songs, indent=4, sort_keys=True, default=str)

  songsJSON= str( songsJSON).replace(' null',' "null"');
  #print(songsJSON);
  return  '{"message":'+songsJSON+'}' 


def queryJson(sql):
  print("queryJson:", sql);
  cursor = connection.cursor()
  cursor.execute(sql)
  rows = [x for x in cursor]
  cols = [x[0] for x in cursor.description]
  df= pd.DataFrame( {"cols": cols})
  #print(df.cols);
  #df.cols = df.cols+ df.groupby("cols").cumcount().astype(str);
  df.cols = df.cols+ removeZero(df.groupby("cols").cumcount()) ;
  #print(df); 
  songs = []
  for row in rows:
    song = {}
    for prop, val in zip(df.cols, row):
      song[prop] = val
    songs.append(song)
  # Create a string representation of your array of songs. 
  return songs; 


def removeZero(count):
  #print (count)
  for i in range(len(count)):

    if( count[i]==0 ):
      count[i] ="";
    else:
      count[i]= str(count[i])
  return count

def queryEntity(entityID):
  
  print (entityID);

@app.route('/nquerye')
def queryResourceEntity():  
  entity_id = request.args.get('eid', default = 'null', type = str) 
  if(entity_id =="null"  ):
    return nullQuery();
  
  sql = sql+" where ( TO_UNIQUEID ='" +entity_id+"'    )  "; 
  sql = sql+ " union "+query_resource+ " where (   from_UNIQUEID ='" +entity_id+"'  )"; 
   
    
  songsJSON= queryJson(sql);
  
  songsJSON = json.dumps(songsJSON, indent=4, sort_keys=True, default=str)
  message= str( songsJSON) 
  #if(from_to=="t" or from_to=="f"):
  #  sql = query_resource;
  #  sql = sql+" where ( TO_PHYSICALRESOURCE_UNIQUEID ='" +physical_resource_id+"'   or '"+physical_resource_id+"' ='null' ) and  (TO_LOGICALRESOURCE_UNIQUEID ='" +logical_resource_id+"'  or '"+logical_resource_id+"' ='null'   )"; 
  #  sql = sql+ " union "+query_resource+ " where (   PHYSICALRESOURCE_UNIQUEID ='" +physical_resource_id+"' or '"+physical_resource_id+"' ='null' ) and  ( LOGICALRESOURCE_UNIQUEID ='" +logical_resource_id+"' or '"+logical_resource_id+"' ='null'   )"; 
  #  return query(sql);
  r =   '{"message":'+songsJSON +'}' 

  r= r.replace(': null',': "null"').replace(': None',': "None"');
  #print (r);
  return r;


@app.route('/nqueryp')
def queryPleace():  
  alias_id = request.args.get('aid', default = 'null', type = str) 
  if(alias_id =="null"  ):
    return nullQuery();
  sql = query_entity_address +"'" +alias_id+"'";
  songsJSON= queryJson(sql)
   
  songsJSON = json.dumps(songsJSON, indent=4, sort_keys=True, default=str)
  message= str( songsJSON) 
  #if(from_to=="t" or from_to=="f"):
  #  sql = query_resource;
  #  sql = sql+" where ( TO_PHYSICALRESOURCE_UNIQUEID ='" +physical_resource_id+"'   or '"+physical_resource_id+"' ='null' ) and  (TO_LOGICALRESOURCE_UNIQUEID ='" +logical_resource_id+"'  or '"+logical_resource_id+"' ='null'   )"; 
  #  sql = sql+ " union "+query_resource+ " where (   PHYSICALRESOURCE_UNIQUEID ='" +physical_resource_id+"' or '"+physical_resource_id+"' ='null' ) and  ( LOGICALRESOURCE_UNIQUEID ='" +logical_resource_id+"' or '"+logical_resource_id+"' ='null'   )"; 
  #  return query(sql);
  r =   '{"message":'+songsJSON +'}' 

  r= r.replace(': null',': "null"').replace(': None',': "None"');
  #print (r);
  return r;


@app.route('/ndbquery')
def nullQuery():  
  return  '{"message":[]}' 
  
# Define route "/api".
@app.route('/napi')
def api():
  # return in JSON format. (For API)
  return jsonify({"message":data})
  #return jsonify({"message":"Hello from Flask!"})



