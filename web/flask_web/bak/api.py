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
import time;

from flask import request
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/dataprocess/web/web/static/files'
ALLOWED_EXTENSIONS = {'tar', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

#app = Flask(__name__)
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

data= [{"ASSOCIATIONPATTERN_ID0": 111,
        "A_DN0": "AR=AP Terminal Port to ONT",
        "FROM_TYPE0": "p",
        "LOGICALRESOURCE_UNIQUEID0": "null",
        "NETWORK_UNIQUEID0": "",
        "N_DN0": "null",
        "PHYSICALRESOURCE_UNIQUEID0": 52068650,
        "RESOURCE_UNIQUEID0": 52068650,
        "R_DN0": "ME=PHNXAZNE 3335 E SHERIDAN ST/TP=001",
        "R_NAME0": "Terminal Port",
        "R_PREFIX0": "TP",
        "TO_LOGICALRESOURCE_UNIQUEID0": "null",
        "TO_NETWORK_UNIQUEID0": "null",
        "TO_PHYSICALRESOURCE_UNIQUEID0": 62047745,
        "TO_PLACE_UNIQUEID0": "null",
        "TO_P_DN0": "null",
        "TO_RESOURCE_UNIQUEID0": 62047745,
        "TO_R_DN0": "ME=62047715",
        "TO_R_NAME0": "Optical Node Terminal",
        "TO_R_PREFIX0": "ME",
        "TO_TYPE0": "p"
 }
 ]


connection = cx_Oracle.connect(user="ooldrtest4", password="a268261a456b8a18ed68f9ed8",
                               dsn="racorad43-scan.test.intranet:1521/svc_o2test1")                               
 
query="""

select v_resource.ASSOCIATIONPATTERN_ID,v_resource.* from v_resource
where    PHYSICALRESOURCE_UNIQUEID=52068650
""" 

query_resource="""

select v_resource.ASSOCIATIONPATTERN_ID,v_resource.* from v_resource 
""" 
query_place="""

select 
n1.*
from hv_address addr
join externalsystemplacesi esp on esp.externalid = addr.address_alias_id 
INNER JOIN v_resource n1 on n1.TO_PLACE_UNIQUEID= esp.uniqueid 
"""
query_entity="""
 select ENTITYID, dn.dnkey, nvl( dn.PARENTDN,'') PARENTDN, dn.DISTINGUISHEDNAME, nvl(  dn.ROOTDN_ENTITYID, '') ROOTDN_ENTITYID, et.DISTINGUISHEDNAME etype, et.CATEGORY  from
DISTINGUISHEDNAME dn 
join  entitytype et on dn.ENTITYTYPE_UNIQUEID= et.UNIQUEID
where ENTITYID=
  """
query_entity_address="""
select  dn.ENTITYID ,  dn.dnkey, nvl( dn.PARENTDN,'') PARENTDN, dn.DISTINGUISHEDNAME, nvl(  dn.ROOTDN_ENTITYID, '') ROOTDN_ENTITYID, et.DISTINGUISHEDNAME etype, et.CATEGORY   
from hv_address addr
join externalsystemplacesi esp on esp.externalid = addr.address_alias_id  
join DISTINGUISHEDNAME dn on dn.ENTITYID=esp.uniqueid 
 join  entitytype et on dn.ENTITYTYPE_UNIQUEID= et.UNIQUEID
where  addr.address_alias_id =
"""


query_resource_v3="""

select   A_ID,A_DN,FROM_TYPE,TO_TYPE,FROM_UNIQUEID,TO_UNIQUEID,FROM_DN,FROM_ENKEY,FROM_ETID,FROM_ETYPE,TO_DN,TO_ENKEY,TO_ETID,TO_ETYPE from v_resource3 
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

@app.route('/querye')
def queryResourceEntity():  
  entity_id = request.args.get('eid', default = 'null', type = str) 
  if(entity_id =="null"  ):
    return nullQuery();
  sql = query_entity + entity_id;
  songsJSON= queryJson(sql)
  
  logical_resource_id = 'null'
  physical_resource_id = 'null' 


  sql = query_resource;
  flag = 0
  for e in songsJSON:
    print(e);
    if(str(e["CATEGORY"])=="PHYSICAL_RESOURCE"): 
      sql = sql+" where ( TO_PHYSICALRESOURCE_UNIQUEID ='" +entity_id+"'    )  "; 
      sql = sql+ " union "+query_resource+ " where (   PHYSICALRESOURCE_UNIQUEID ='" +entity_id+"'  )"; 
      flag = 1
    if(str(e["CATEGORY"])=="LOGICAL_RESOURCE"):
      sql = sql+" where ( TO_LOGICALRESOURCE_UNIQUEID ='" +entity_id+"'    )  "; 
      sql = sql+ " union "+query_resource+ " where (   LOGICALRESOURCE_UNIQUEID ='" +entity_id+"'  )"; 
      flag = 1
    if(str(e["CATEGORY"])=="LOCATION"):
      sql = sql+" where ( TO_PLACE_UNIQUEID ='" +entity_id+"'    )  "; 
      #sql = sql+ " union "+query_resource+ " where (   TO_PLACE_UNIQUEID ='" +entity_id+"'  )"; 
      flag = 1 
    if(str(e["CATEGORY"])=="NETWORKSI"):
      sql = sql+" where ( NETWORK_UNIQUEID ='" +entity_id+"'    )  ";  
      sql = sql+ " union "+query_resource+ " where (   TO_NETWORK_UNIQUEID ='" +entity_id+"'  )"; 
      flag = 1 
  entityInfo = json.dumps(songsJSON, indent=4, sort_keys=True, default=str)  
  entityInfo= str( entityInfo) 
  #print(songsJSON);
  #return  '{"message":'+songsJSON+'}' 
   
  if(flag ==0):
    return nullQuery();
    
  songsJSON= queryJson(sql);
  
  songsJSON = json.dumps(songsJSON, indent=4, sort_keys=True, default=str)
  message= str( songsJSON) 
  #if(from_to=="t" or from_to=="f"):
  #  sql = query_resource;
  #  sql = sql+" where ( TO_PHYSICALRESOURCE_UNIQUEID ='" +physical_resource_id+"'   or '"+physical_resource_id+"' ='null' ) and  (TO_LOGICALRESOURCE_UNIQUEID ='" +logical_resource_id+"'  or '"+logical_resource_id+"' ='null'   )"; 
  #  sql = sql+ " union "+query_resource+ " where (   PHYSICALRESOURCE_UNIQUEID ='" +physical_resource_id+"' or '"+physical_resource_id+"' ='null' ) and  ( LOGICALRESOURCE_UNIQUEID ='" +logical_resource_id+"' or '"+logical_resource_id+"' ='null'   )"; 
  #  return query(sql);
  r =   '{"message":'+songsJSON+', "entityInfo":'+entityInfo+'}' 

  r= r.replace(': null',': "null"').replace(': None',': "None"');
  #print (r);
  return r;

@app.route('/queryp')
def queryPleace():  
  alias_id = request.args.get('aid', default = 'null', type = str) 
  if(alias_id =="null"  ):
    return nullQuery();
  sql = query_entity_address +"'" +alias_id+"'";
  songsJSON= queryJson(sql)
  
  logical_resource_id = 'null'
  physical_resource_id = 'null' 


  sql = query_resource;
  flag = 0
  for e in songsJSON:
    print(e);
    if(str(e["CATEGORY"])=="LOCATION"):
      sql = query_place;
      sql = sql+" where addr.address_alias_id ='" +alias_id+"'";
      #sql = sql+ " union "+query_resource+ " where (   TO_PLACE_UNIQUEID ='" +entity_id+"'  )"; 
      flag = 1  
  entityInfo = json.dumps(songsJSON, indent=4, sort_keys=True, default=str)  
  entityInfo= str( entityInfo) 
  #print(songsJSON);
  #return  '{"message":'+songsJSON+'}' 
   
  if(flag ==0):
    return nullQuery();
    
  songsJSON= queryJson(sql);
  
  songsJSON = json.dumps(songsJSON, indent=4, sort_keys=True, default=str)
  message= str( songsJSON) 
  #if(from_to=="t" or from_to=="f"):
  #  sql = query_resource;
  #  sql = sql+" where ( TO_PHYSICALRESOURCE_UNIQUEID ='" +physical_resource_id+"'   or '"+physical_resource_id+"' ='null' ) and  (TO_LOGICALRESOURCE_UNIQUEID ='" +logical_resource_id+"'  or '"+logical_resource_id+"' ='null'   )"; 
  #  sql = sql+ " union "+query_resource+ " where (   PHYSICALRESOURCE_UNIQUEID ='" +physical_resource_id+"' or '"+physical_resource_id+"' ='null' ) and  ( LOGICALRESOURCE_UNIQUEID ='" +logical_resource_id+"' or '"+logical_resource_id+"' ='null'   )"; 
  #  return query(sql);
  r =   '{"message":'+songsJSON+', "entityInfo":'+entityInfo+'}' 

  r= r.replace(': null',': "null"').replace(': None',': "None"');
  #print (r);
  return r;
def queryPlaceOld():  
  alias_id = request.args.get('aid', default = 'null', type = str)
  from_to = request.args.get('ft', default = 'null', type = str)
  place_id = request.args.get('pid', default = 'null', type = str)

  if(alias_id!="null"):
    sql = query_place;
    sql = sql+" where addr.address_alias_id ='" +alias_id+"'";
    return query(sql);
  if(from_to=="f"):
    sql = query_resource;
    sql = sql+" where (FROM_PLACE_UNIQUEID ='" +place_id+"'   )";
    return query(sql);
  if(from_to=="t"):
    sql = query_resource;
    sql = sql+" where (TO_PLACE_UNIQUEID ='" +place_id+"'   )";
    return query(sql);
  
  return nullQuery();

@app.route('/queryr')
def queryResource():  
  from_to = request.args.get('ft', default = 'null', type = str)
  logical_resource_id = request.args.get('lrid', default = 'null', type = str)
  physical_resource_id = request.args.get('prid', default = 'null', type = str)
  if(logical_resource_id =="null" and physical_resource_id =="null"):
    return nullQuery();

  if(from_to=="t" or from_to=="f"):
    sql = query_resource;
    sql = sql+" where ( TO_PHYSICALRESOURCE_UNIQUEID ='" +physical_resource_id+"'   or '"+physical_resource_id+"' ='null' ) and  (TO_LOGICALRESOURCE_UNIQUEID ='" +logical_resource_id+"'  or '"+logical_resource_id+"' ='null'   )"; 
    sql = sql+ " union "+query_resource+ " where (   PHYSICALRESOURCE_UNIQUEID ='" +physical_resource_id+"' or '"+physical_resource_id+"' ='null' ) and  ( LOGICALRESOURCE_UNIQUEID ='" +logical_resource_id+"' or '"+logical_resource_id+"' ='null'   )"; 
    return query(sql);
  if(from_to=="fw"):
    sql = query_resource;
    sql = sql+" where (TO_PHYSICALRESOURCE_UNIQUEID ='" +physical_resource_id+"' or '"+physical_resource_id+"' ='null' ) and  (TO_LOGICALRESOURCE_UNIQUEID ='" +logical_resource_id+"' or '"+logical_resource_id+"' ='null' )";
    return query(sql);
  return nullQuery();

@app.route('/queryn')
def queryNetwork():  
  from_to = request.args.get('ft', default = 'null', type = str)
  network_id = request.args.get('nid', default = 'null', type = str)
  
  if(from_to=="t"):
    sql = query_resource;
    sql = sql+" where (NETWORK_UNIQUEID ='" +network_id+"' )  ";
    return query(sql);
  if(from_to=="f"):
    sql = query_resource;
    sql = sql+" where (TO_NETWORK_UNIQUEID ='" +network_id+"' )  ";
    return query(sql);

@app.route('/dbquery')
def nullQuery():  
  return  '{"message":[]}' 
  
# Define route "/api".
@app.route('/api')
def api():
  # return in JSON format. (For API)
  return jsonify({"message":data})
  #return jsonify({"message":"Hello from Flask!"})



query_resource2="""

select  * from v_resource2 
""" 
query_place2="""

select esp.uniqueid my_id,
n1.*
from hv_address addr
join externalsystemplacesi esp on esp.externalid = addr.address_alias_id 
INNER JOIN v_resource2 n1 on n1.TO_UNIQUEID= esp.uniqueid and n1.to_type ='Place' 
where addr.address_alias_id = 
""" 




query_resource2_o="""

select   A_ID,A_DN,FROM_TYPE,TO_TYPE,FROM_UNIQUEID,TO_UNIQUEID,FROM_DN,FROM_ENKEY,FROM_ETID,FROM_ETYPE,TO_DN,TO_ENKEY,TO_ETID,TO_ETYPE from v_resource2 
""" 
query_place2="""

select esp.uniqueid my_id,
n1.*
from hv_address addr
join externalsystemplacesi esp on esp.externalid = addr.address_alias_id 
INNER JOIN v_resource3 n1 on n1.to_PLACE_UNIQUEID= esp.uniqueid  
where addr.address_alias_id = 
""" 

query_place_root="""
 SELECT 0 A_ID,
       'ROOT' A_DN,
       'PhysicalResource' FROM_TYPE,
       'PhysicalResource' TO_TYPE,
       n.entityid FROM_UNIQUEID,
       pn.entityid TO_UNIQUEID,
       n.distinguishedname FROM_DN,
       n.dnkey FROM_ENKEY,
       n.ENTITYTYPE_UNIQUEID   FROM_ETID,
       et.PREFIX FROM_ETYPE,
       pn.distinguishedname TO_DN,
       pn.dnkey TO_ENKEY,
       pn.ENTITYTYPE_UNIQUEID TO_ETID,
       etp.PREFIX  TO_ETYPE  
FROM distinguishedname n
join ENTITYTYPE et on et.UNIQUEID = n.ENTITYTYPE_UNIQUEID
join distinguishedname pn on pn.entityid = n.ROOTDN_ENTITYID
join ENTITYTYPE etp on etp.UNIQUEID = pn.ENTITYTYPE_UNIQUEID
WHERE n.entityid = 
"""
@app.route('/nquerye')
def queryResourceEntity2():  
  entity_id = request.args.get('eid', default = 'null', type = str) 
  if(entity_id =="null"  ):
    return nullQuery();
  sql = query_resource2;
  sql = sql+" where ( TO_UNIQUEID ='" +entity_id+"'    )  "; 
  sql = sql+ " union "+query_resource2+ " where (   from_uniqueid ='" +entity_id+"'  )"; 
   
    
  songsJSON= queryJson(sql);
  
  songsJSON = json.dumps(songsJSON, indent=4, sort_keys=True, default=str)
  message= str( songsJSON) 
  #if(from_to=="t" or from_to=="f"):
  #  sql = query_resource;
  #  sql = sql+" where ( TO_PHYSICALRESOURCE_UNIQUEID ='" +physical_resource_id+"'   or '"+physical_resource_id+"' ='null' ) and  (TO_LOGICALRESOURCE_UNIQUEID ='" +logical_resource_id+"'  or '"+logical_resource_id+"' ='null'   )"; 
  #  sql = sql+ " union "+query_resource+ " where (   PHYSICALRESOURCE_UNIQUEID ='" +physical_resource_id+"' or '"+physical_resource_id+"' ='null' ) and  ( LOGICALRESOURCE_UNIQUEID ='" +logical_resource_id+"' or '"+logical_resource_id+"' ='null'   )"; 
  #  return query(sql);
  r =   '{"message":'+songsJSON +', "my_id":'+entity_id+'}' 

  r= r.replace(': null',': "null"').replace(': None',': "None"');
  #print (r);
  return r;


@app.route('/nqueryp')
def queryPleace2():  
  alias_id = request.args.get('aid', default = 'null', type = str) 
  if(alias_id =="null"  ):
    return nullQuery();
  sql = query_place2 +"'" +alias_id+"'";
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




@app.route('/n2querye')
def queryResourceEntityv2():  
  entity_id = request.args.get('eid', default = 'null', type = str) 
  rt = request.args.get('rt', default = '0', type = str) 
  if(entity_id =="null"  ):
    return nullQuery();
  if(entity_id.isnumeric()):
    sql = query_entity + entity_id;
  else:    
    sql = query_entity + "0 or dn.DISTINGUISHEDNAME='" +entity_id+"'";
  songsJSON= queryJson(sql)
  
  logical_resource_id = 'null'
  physical_resource_id = 'null' 


  sql = query_resource_v3;
  flag = 0
  ENTITYID =""
  for e in songsJSON:
    print(e);
    ENTITYID = str(e["ENTITYID"])
    if(str(e["CATEGORY"])=="PHYSICAL_RESOURCE"): 
      sql = sql+" where ( TO_PHYSICALRESOURCE_UNIQUEID ='" +ENTITYID+"'    )  "; 
      sql = sql+ " union "+query_resource_v3+ " where (   PHYSICALRESOURCE_UNIQUEID ='" +ENTITYID+"'  )"; 
      if(rt=="1"):
        sql = sql+ " union "+query_place_root+ " '" +ENTITYID+"'   "; 
      flag = 1
    if(str(e["CATEGORY"])=="LOGICAL_RESOURCE"):
      sql = sql+" where ( TO_LOGICALRESOURCE_UNIQUEID ='" +ENTITYID+"'    )  "; 
      sql = sql+ " union "+query_resource_v3+ " where (   LOGICALRESOURCE_UNIQUEID ='" +ENTITYID+"'  )"; 
      flag = 1
    if(str(e["CATEGORY"])=="LOCATION"):
      sql = sql+" where ( TO_PLACE_UNIQUEID ='" +ENTITYID+"'    )  "; 
      #sql = sql+ " union "+query_resource+ " where (   TO_PLACE_UNIQUEID ='" +entity_id+"'  )"; 
      flag = 1 
    if(str(e["CATEGORY"])=="NETWORKSI"):
      sql = sql+" where ( NETWORK_UNIQUEID ='" +ENTITYID+"'    )  ";  
      sql = sql+ " union "+query_resource_v3+ " where (   TO_NETWORK_UNIQUEID ='" +ENTITYID+"'  )"; 
      flag = 1 
  entityInfo = json.dumps(songsJSON, indent=4, sort_keys=True, default=str)  
  entityInfo= str( entityInfo) 
  #print(songsJSON);
  #return  '{"message":'+entityInfo+'}' 
   
  if(flag ==0):
    return nullQuery();
  
  print(sql);  
  songsJSON= queryJson(sql);
  
  songsJSON = json.dumps(songsJSON, indent=4, sort_keys=True, default=str)
  message= str( songsJSON) 
  r =   '{"message":'+songsJSON+', "entityInfo":'+entityInfo+', "my_id":"'+ENTITYID+'"}' 

  r= r.replace(': null',': "null"').replace(': None',': "None"');
  #print(r); 
  return r;

def allowed_file(filename):
  return True;
  return '.' in filename and \
          filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
gFileList=[];
@app.route('/listfile', methods=['GET' ])
def list_file():
  global gFileList;
  r = str(gFileList); 
  now = time.time()
  files = os.listdir(UPLOAD_FOLDER); 
  for f in files:
    fp = os.path.join(UPLOAD_FOLDER, f);
    if os.stat(fp).st_mtime < now - 300 * 1000:
      os.remove(fp);
  gFileList=[]

  return r; 
@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        #print(request.files)
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        print(file.filename );
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            gFileList.append(filename);
            #return redirect(url_for('download_file', name=filename))
    return '{"r":"ok"}'
    
    '''
    <!doctype html><title>Upload new File</title><h1>Upload new File</h1><form method=post enctype=multipart/form-data><input type=file name=file><input type=submit value=Upload></form>
    ''' 