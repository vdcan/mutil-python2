function initPage() {
    for (var i = 0; i < gGroupText.length; i++) {
        $(".u_" + gGroupText[i]["sa_code_full"]).html(gGroupText[i]["sa_unit"]);
        $(".t_" + gGroupText[i]["sa_code_full"]).html(gGroupText[i]["sa_text"]);
        $(".v_" + gGroupText[i]["sa_code_full"]).html("0");
 // console.log(gGroupText[i]);
    }


    $(".btn-primary").click(function (me) {
        ButtonClicked(me);
    });

}




function mySub() { 
	subscribeByType("p", gAncestor)
	/*var d = gNCodes.split(', ')
	for(var i =0; i < d.length; i ++)
    subscribeByType("", gAncestor+'/'+d[i]) 
    */

}
function fixData(o){ try {
                o = o.replaceAll(",}","}")
                o = o.replaceAll("},]","}]")
                 o = JSON.parse(o);
            } catch (e) {
                console.log(e);
            }
  return o;
}
function mqtt_status(  o) {
	var data = fixData(o);
	   console.log("mqtt_status",  data) 
	   
	   Object.entries(data).forEach(entry => {
 const [key, value] = entry;
        console.log(key, value);
        var k = key+"";
 // var k = key; 
var v = value["d"];
v = v.substring(1, v.length -1)
var va = v.split(", ");
var tmpV = va[0];
console.log(va);
var flag = 1;
for(var i =0;i <va.length; i ++){
if(tmpV !=va[i]){
    flag =0; 
} 
}
v = v.replaceAll(", ",""); 
k = k.toUpperCase();
 console.log( ".S_" +k , v);
 if(flag ==1 &&tmpV!="0")
 $(".S_" +k).css("fill","#eeeeee");
 else
    $(".S_" +k).css("fill","#"+v);;
   // console.log( $(".s_" +k).css("fill"));
 // console.log(k, value); s_n3_1_RGB1
});
//$(".s_n3_1_RGB1"  ).css("fill", "yellow")  
     /*   for (var i = 0; i < o.d.length; i ++) {
   $(".s_n3_1_RGB1"  ).css("fill")          console.log(o.d[i]);
            $(".v_"+o.d[i]["sa_c"]).html(o.d[i]["v"]);
        }*/
}


function mqtt_data(  o) {
	var data = fixData(o);
	    console.log(  data) 
	    var nc = data.nc;
	    for (var i = 0; i < data.data.length; i++) {
	    	var d=  data.data[i];
	    	var ni = d.ni;
	    for (var j = 0; j < d.d.length; j++) {
         //   console.log(d.d[j]);
         //   console.log(".v_" +nc+"_"+ni+"_"+d.d[j]["t"]+"_"+d.d[j]["i"], d.d[j]["v"]);
            var c = ".V_" +nc+ ni+ d.d[j]["t"]+ d.d[j]["i"];
            c = c.toUpperCase();
            $(c).html(d.d[j]["v"]);
	    } 
        } 
}

function ButtonClicked(me) {
    //  console.log(me);
    var a = me.target.attributes["cmdid"];
   // console.log(gCmd,a.value);
    if(gCmd[a.value]!=null){
    //	publish("s/"+gCmd[a.value],"cmd")
    	message_out("s/"+gCmd[a.value],"cmd")
    }
    //message_out("p/cmd/",a.value)
   // console.log(a.value);
  //  console.log($(me).attr("id"));
}
 