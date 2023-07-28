function switchTab(e, info) {
   var i, content, links;
   content = document.getElementsByClassName("vTab");
   for (i = 0; i < content.length; i++) {
      content[i].style.display = "none"; 
   }
   content = document.getElementsByClassName("vTabActive");
   for (i = 0; i < content.length; i++) {
      content[i].style.display = "none"; 
   }
   links = document.getElementsByClassName("lTab");
   for (i = 0; i < links.length; i++) {
      links[i].className = links[i].className.replace(" active", "");
   }
   document.getElementById(info).style.display = "block";
   if(e!=null)
   e.currentTarget.className += " active";
}
function initTabs(){

    $("#template_tab").tmpl({ Table: gMenuData }).appendTo("#tab");
    $("#template_context").tmpl({ Table: gMenuData }).appendTo("#context");
   // switchTab(null, "test1");
//document.getElementById("test1").click(); 
}

setTimeout(initTabs,50);