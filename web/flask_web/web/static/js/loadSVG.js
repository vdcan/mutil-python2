
$(function(){
	
	$(".hideme2").each(function() {
		$(this).get(0).tagName=="IMG";
		var u = $(this).attr("src");
		var uid = $(this).parent().attr("id");
    loadSVGasXML(u, uid);
});
}) ;
function loadSVGasXML(SVGFile, uid) {
   // var SVGFile="fan.svg";

    var loadXML = new XMLHttpRequest();
    function handler(){
        var svgDiv = document.getElementById(uid);
        if(loadXML.readyState == 4 && loadXML.status == 200) {            
            var xmlString=loadXML.responseText;
            svgDiv.innerHTML=xmlString;
            $("a").click(function() {
               alert('hi');
            });            
            fitSVGinDiv();        
        }
    }
    if (loadXML != null) {
        loadXML.open("GET", SVGFile+"?_t=1"+timestamp(), true);
        loadXML.onreadystatechange = handler;
        loadXML.send();
    }
}
function timestamp  () {
    var d = new Date();
    var result = d.getYear() + '' + d.getMonth() + '' + d.getDay() + '' + d.getMinutes() + '' + d.getSeconds() + '' + d.getMilliseconds();
    return result;
}
function fitSVGinDiv(){
    var divWH=60;
    var mySVG=document.getElementsByTagName("svg")[0];
    var bb=mySVG.getBBox();
    var bbw=bb.width;
    var bbh=bb.height;
    //--use greater of bbw vs bbh--
    if(bbw>=bbh)
        var factor=bbw/divWH;
    else
        var factor=bbh/divWH;
    var vbWH=divWH*factor;
    var vbX=(bbw-vbWH)/2;
    var vbY=(bbh-vbWH)/2;
   // mySVG.setAttribute("viewBox",vbX+" "+vbY+" "+vbWH+" "+vbWH);
    mySVG.setAttribute("width","100%");
   // mySVG.setAttribute("height","100%");
}
function runCmd(cmd){
	console.log(cmd,gCmd );
	if(gCmd[cmd]!=null){
	console.log(cmd,gCmd[cmd]);
		
	message_out(gCmd[cmd],"cmd")
}
}