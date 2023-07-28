
function GetID(r, type){
	if(gForEquipment != undefined && gForEquipment==1)
	return  r.type_code+"_"+ r.equipment_id+"_"+r.node_index+"_"+r.device_index +"_"+type;
	else
	return  r.type_code+"_"+r.node_index+"_"+r.device_index +"_"+type;
}

function GetID2(r, type){

	if(gForEquipment != undefined && gForEquipment==1)
	return r.tc +"_"+ r.eid+"_"+r.ni+"_"+r.di +"_"+type;
	else
	
	return r.tc +"_"+ r.ni+"_"+r.di +"_"+type;
}
/*******************************************************************************
 * Copyright (c) 2015 IBM Corp.
 *
 * All rights reserved. This program and the accompanying materials
 * are made available under the terms of the Eclipse Public License v1.0
 * and Eclipse Distribution License v1.0 which accompany this distribution.
 *
 * The Eclipse Public License is available at
 *    http://www.eclipse.org/legal/epl-v10.html
 * and the Eclipse Distribution License is available at
 *   http://www.eclipse.org/org/documents/edl-v10.php.
 *
 * Contributors:
 *    James Sutton - Initial Contribution
 *******************************************************************************/

/*
Eclipse Paho MQTT-JS Utility
This utility can be used to test the Eclipse Paho MQTT Javascript client.
*/

// Create a client instance
var client = null;
var connected = false;


logMessage("INFO", "Starting Eclipse Paho JavaScript Utility.");

// Things to do as soon as the page loads
//document.getElementById("clientIdInput").value = "js-utility-" + makeid();

// called when the client connects
function onConnect(context) {
  // Once a connection has been made, make a subscription and send a message.
  var connectionString = context.invocationContext.host + ":" + context.invocationContext.port + context.invocationContext.path;
  logMessage("INFO", "Connection Success ", "[URI: ", connectionString, ", ID: ", context.invocationContext.clientId, "]");
  /*var statusSpan = document.getElementById("connectionStatus");
  statusSpan.innerHTML = "Connected to: " + connectionString + " as " + context.invocationContext.clientId;
  connected = true;
  setFormEnabledState(true);*/
}


function onConnected(reconnect, uri) {
  // Once a connection has been made, make a subscription and send a message.
  logMessage("INFO", "Client Has now connected: [Reconnected: ", reconnect, ", URI: ", uri, "]");
    //subscribe("s/#", 0)
    if (typeof mySub != "undefined")
        setTimeout(mySub, 200);
  connected = true;


} 
function onFail(context) {
  logMessage("ERROR", "Failed to connect. [Error Message: ", context.errorMessage, "]");
//  var statusSpan = document.getElementById("connectionStatus");
//  statusSpan.innerHTML = "Failed to connect: " + context.errorMessage;
  connected = false;
  //setFormEnabledState(false);
}

// called when the client loses its connection
function onConnectionLost(responseObject) {
  if (responseObject.errorCode !== 0) {
    logMessage("INFO", "Connection Lost. [Error Message: ", responseObject.errorMessage, "]");
  }
  connected = false;
}
/*
function mqtt_wk_alarm(equ_info,o) {
    console.log("F_wk_alarm");
    console.log(o);
}
function mqtt_wk_data(equ_info,o) {
    console.log("F_wk_data");
    console.log(o);
}*/
// called when a message arrives
 

function onMessageArrived(message) {
    //console.log(message.destinationName, message.payloadString);
    var na = message.destinationName.split('/');
    if (na.length > 0) {

    var equ_info = {};
        name = na[na.length -1]
        if (eval("typeof mqtt_" + name + " === 'function'")) {
            var o = message.payloadString

          /*  try {
                o = o.replaceAll("'","\"")
                 o = JSON.parse(o);
            } catch (e) {
                console.log(e);
            }
             */
            eval("mqtt_" + name + "( o)");
        } else {
            console.log("can't find  mqtt_" + name);
        }
    }
    return;
/*if(	message.destinationName.indexOf("/databoard/")>=0){
	 var o = JSON.parse(message.payloadString);
	console.log(o);
		$("."+GetID2(o, "D")).html(o.un) 
		$("."+GetID2(o, "S")).html(o.s) 
		$("."+GetID2(o, "V")).html(o.v)  
		if(SetSVGValue!= undefined)
		SetSVGValue(GetID2(o, "V"), o.v);
	//console.log(o);
}*/
	
  //logMessage("INFO", "Message Recieved: [Topic: ", message.destinationName, ", Payload: ", message.payloadString, ", QoS: ", message.qos, ", Retained: ", message.retained, ", Duplicate: ", message.duplicate, "]");
 /* var messageTime = new Date().toISOString();
  // Insert into History Table
  var table = document.getElementById("incomingMessageTable").getElementsByTagName("tbody")[0];
  var row = table.insertRow(0);
  row.insertCell(0).innerHTML = message.destinationName;
  row.insertCell(1).innerHTML = safeTagsRegex(message.payloadString);
  row.insertCell(2).innerHTML = messageTime;
  row.insertCell(3).innerHTML = message.qos;


  if (!document.getElementById(message.destinationName)) {
    var lastMessageTable = document.getElementById("lastMessageTable").getElementsByTagName("tbody")[0];
    var newlastMessageRow = lastMessageTable.insertRow(0);
    newlastMessageRow.id = message.destinationName;
    newlastMessageRow.insertCell(0).innerHTML = message.destinationName;
    newlastMessageRow.insertCell(1).innerHTML = safeTagsRegex(message.payloadString);
    newlastMessageRow.insertCell(2).innerHTML = messageTime;
    newlastMessageRow.insertCell(3).innerHTML = message.qos;

  } else {
    // Update Last Message Table
    var lastMessageRow = document.getElementById(message.destinationName);
    lastMessageRow.id = message.destinationName;
    lastMessageRow.cells[0].innerHTML = message.destinationName;
    lastMessageRow.cells[1].innerHTML = safeTagsRegex(message.payloadString);
    lastMessageRow.cells[2].innerHTML = messageTime;
    lastMessageRow.cells[3].innerHTML = message.qos;
  }*/

}

function connectionToggle() {

  if (connected) {
    disconnect();
  } else {
    connect();
  }


}

function getLocation(href = window.location) {
    var location = document.createElement("a");
    location.href = href;
    // IE doesn't populate all link properties when setting .href with a relative URL,
    // however .href will return an absolute URL which then can be used on itself
    // to populate these additional fields.
    if (location.host == "") {
        location.href = location.href;
    }
    return location;
};
function connect() {
	 var hostname = "127.0.0.1"
	if(typeof(gMQTT_ADDRESS) == "undefined"){
		
    var a = getLocation(); 
      hostname = a.hostname;// "vr.polluxcom.com";//"192.168.0.179";// document.getElementById("hostInput").value;
	}else{
			   hostname  = gMQTT_ADDRESS;
	}
    var port = 9003;//9003;//document.getElementById("portInput").value;
  var clientId =makeid();//"testid111";// document.getElementById("clientIdInput").value;

    var path = "/";//"/mqtt";// document.getElementById("pathInput").value;
  var user ="";// document.getElementById("userInput").value;
  var pass ="";//= document.getElementById("passInput").value;
  var keepAlive =120;// Number(document.getElementById("keepAliveInput").value);
  var timeout =300;// Number(document.getElementById("timeoutInput").value);
  var tls = false;// document.getElementById("tlsInput").checked;
  var automaticReconnect =true;// document.getElementById("automaticReconnectInput").checked;
  var cleanSession =true;// document.getElementById("cleanSessionInput").checked;
  var lastWillTopic ="";// document.getElementById("lwtInput").value;
  var lastWillQos =0;// Number(document.getElementById("lwQosInput").value);
  var lastWillRetain =true;// document.getElementById("lwRetainInput").checked;
  var lastWillMessageVal ="";// document.getElementById("lwMInput").value;


    client = new Paho.MQTT.Client(hostname, Number(port), path,clientId);
  //if (path.length > 0) {
  //  client = new Paho.Client(hostname, Number(port), path, clientId);
  //} else {
  //  client = new Paho.Client(hostname, Number(port), clientId);
  //}
  logMessage("INFO", "Connecting to Server: [Host: ", hostname, ", Port: ", port, ", Path: ", client.path, ", ID: ", clientId, "]");

  // set callback handlers
  client.onConnectionLost = onConnectionLost;
  client.onMessageArrived = onMessageArrived;
  client.onConnected = onConnected;


  var options = {
    invocationContext: { host: hostname, port: port, path: client.path, clientId: clientId },
    timeout: timeout,
    keepAliveInterval: keepAlive,
    cleanSession: cleanSession,
    useSSL: tls,
    reconnect: automaticReconnect,
    onSuccess: onConnect,
    onFailure: onFail
  };



  if (user.length > 0) {
    options.userName = user;
  }

  if (pass.length > 0) {
    options.password = pass;
  }

  if (lastWillTopic.length > 0) {
    var lastWillMessage = new Paho.Message(lastWillMessageVal);
    lastWillMessage.destinationName = lastWillTopic;
    lastWillMessage.qos = lastWillQos;
    lastWillMessage.retained = lastWillRetain;
    options.willMessage = lastWillMessage;
  }

  // connect the client
  client.connect(options);
 // var statusSpan = document.getElementById("connectionStatus");
 // statusSpan.innerHTML = "Connecting...";
  logMessage("INFO", "Connecting...");
}

function disconnect() {
  logMessage("INFO", "Disconnecting from Server.");
  client.disconnect();
  /*var statusSpan = document.getElementById("connectionStatus");
  statusSpan.innerHTML = "Connection - Disconnected.";
  connected = false;
  setFormEnabledState(false);*/

}
 

function publish(topic, qos, message, retain = false) {
  /*var topic = document.getElementById("publishTopicInput").value;
  var qos = document.getElementById("publishQosInput").value;
  var message = document.getElementById("publishMessageInput").value;
  var retain = document.getElementById("publishRetainInput").checked;
  */
  topic =  gSET_CODE+topic
  logMessage("INFO", "Publishing Message: [Topic: ", topic, ", Payload: ", message, ", QoS: ", qos, ", Retain: ", retain, "]");
  message = new Paho.Message(message);
  message.destinationName =topic;
  message.qos = Number(qos);
  message.retained = retain;
  client.send(message);
}
var gSubscribedTopicList = [];

function unsubscribeAll() {
    let data = gSubscribedTopicList.forEach(function (data, i) {
        unsubscribe(data) 
    });
    gSubscribedTopicList = [];
}
// subscribe Alarm
function subscribeAlarm(topic, sub_flag = true) {

    var topic = "s/wk_alarm/" + topic;
    if (sub_flag)
        topic = topic + "/#";
    topic = topic.replaceAll("//", "/");
    gSubscribedTopicList.push(topic);
    subscribe(topic, 0);
}
// subscribe Alarm
function subscribeTest(topic, sub_flag = true) {

    var topic = "s/test/" + topic;
    if (sub_flag)
        topic = topic + "/#";
    topic = topic.replaceAll("//", "/");
    gSubscribedTopicList.push(topic);
    subscribe(topic, 0);
}
// subscribe Data
function subscribeData(topic, sub_flag = true) {

    var topic = "s/wk_data/" + topic;
    if (sub_flag)
        topic = topic + "/#";

    topic = topic.replaceAll("//", "/");
    gSubscribedTopicList.push(topic);
    subscribe(topic, 0);
}

// subscribe Data
function subscribeControl(topic, sub_flag = true) {

    var topic = "s/wk_control/" + topic;
    if (sub_flag)
        topic = topic + "/#";

    topic = topic.replaceAll("//", "/");
    gSubscribedTopicList.push(topic);
    subscribe(topic, 0);
}
// subscribe Data
function subscribeSensorData(topic, sub_flag = true) {
    
    var topic = "s/sensor_data/" + topic;
    if (sub_flag)
        topic = topic + "/#";
    topic = topic.replaceAll("//", "/");
    gSubscribedTopicList.push(topic);
    subscribe(topic, 0);
}
// subscribe Status
function subscribeStatus(topic, sub_flag = true) {

    var topic = "s/wk_status/" + topic;
    if (sub_flag)
        topic = topic + "/#"; 
     
    gSubscribedTopicList.push(topic);
    subscribe(topic, 0); 
}

// subscribe Status
function subscribeByType(type,topic, sub_flag = true) {
//type +
    var topic = "/p/" +     topic;
    if (topic == "") {
        if (sub_flag)
            topic = topic + "#";

    } else {
        if (sub_flag)
            topic = topic + "/#";
    }
    topic = topic.replaceAll("//", "/");
    console.log("subscribing " + topic);
    gSubscribedTopicList.push(topic);
    subscribe(topic, 0);
}
function subscribe(topic, qos) {
  //var topic = document.getElementById("subscribeTopicInput").value;
  //var qos = document.getElementById("subscribeQosInput").value;
  topic = gSET_CODE+topic
  logMessage("INFO", "Subscribing to: [Topic: ", topic, ", QoS: ", qos, "]");
  client.subscribe(topic, { qos: Number(qos) });
}

function unsubscribe(topic ) {
  //var topic = document.getElementById("subscribeTopicInput").value;
  logMessage("INFO", "Unsubscribing: [Topic: ", topic, "]");
  client.unsubscribe(topic, {
    onSuccess: unsubscribeSuccess,
    onFailure: unsubscribeFailure,
    invocationContext: { topic: topic }
  });
}


function unsubscribeSuccess(context) {
  logMessage("INFO", "Unsubscribed. [Topic: ", context.invocationContext.topic, "]");
}

function unsubscribeFailure(context) {
  logMessage("ERROR", "Failed to unsubscribe. [Topic: ", context.invocationContext.topic, ", Error: ", context.errorMessage, "]");
}

function clearHistory() {
//  var table = document.getElementById("incomingMessageTable");
  //or use :  var table = document.all.tableid;
 // for (var i = table.rows.length - 1; i > 0; i--) {
  //  table.deleteRow(i);
  //}

}


// Just in case someone sends html
function safeTagsRegex(str) {
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").
    replace(/>/g, "&gt;");
}

function makeid() {
  var text = "";
  var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    console.log("makeid")
  for (var i = 0; i < 15; i++)
    text += possible.charAt(Math.floor(Math.random() * possible.length));

  return text;
}

function logMessage(type, ...content) {
  //  console.log(content);
  var consolePre = document.getElementById("consolePre");
  var date = new Date();
  var timeString = date.toUTCString();
  var logMessage = timeString + " - " + type + " - " + content.join("");
 // consolePre.innerHTML += logMessage + "<br/>\n";

	console.log(logMessage);
  if (type === "INFO") {
    console.info(logMessage);
  } else if (type === "ERROR") {
    console.error(logMessage);
  } else {
    console.log(logMessage);
  }
}
function message_out(topic, payload) {
  topic =  gSET_CODE+'/s'+topic
    client.send(topic, payload )
}

$(function () { connect();})