




function swapOutSource(url, p, v) {
    if (url.indexOf(p + "=") > 0) {
        //  url = url.replace(new RegExp(p + "=", 'g'), p + "=" + v);
        url = changeURI(url, p, v);
    } else if (url.indexOf("?") > 0) {
        url = url + "&" + p + "=" + v;
    } else {
        url = url + "?" + p + "=" + v;
    }

    return url;
}

function changeURI(url, key, value) {
    key = escape(key); value = escape(value);
    var kvp = url.split('&');
    var i = kvp.length; var x; while (i--) {
        x = kvp[i].split('=');
        if (x[0] == key) {
            x[1] = value;
            kvp[i] = x.join('=');
            break;
        }
    }
    if (i < 0) {
        kvp[kvp.length] = [key, value].join('=');
    } else {
        //this will reload the page, it's likely better to store this until finished
        url = kvp.join('&');
    }

    return url;
}
function getURLParameters(paramName) {
    var sURL = window.document.URL.toString();
    if (sURL.indexOf("?") > 0) {
        var arrParams = sURL.split("?");
        var arrURLParams = arrParams[1].split("&");
        var arrParamNames = new Array(arrURLParams.length);
        var arrParamValues = new Array(arrURLParams.length);
        var i = 0;
        for (i = 0; i < arrURLParams.length; i++) {
            var sParam = arrURLParams[i].split("=");
            arrParamNames[i] = sParam[0];
            if (sParam[1] != "")
                arrParamValues[i] = unescape(sParam[1]);
            else
                arrParamValues[i] = "No Value";
        }

        for (i = 0; i < arrURLParams.length; i++) {
            if (arrParamNames[i] == paramName) {
                //alert("Param:"+arrParamValues[i]);
                return arrParamValues[i];
            }
        }
        return "No Parameters Found";
    }

}

function myConfirm(dialogText, okFunc, cancelFunc, dialogTitle) {
    myConfirm2(dialogText, okFunc, cancelFunc, dialogTitle, "Yes", "No")
}
function myConfirm2(dialogText, okFunc, cancelFunc, dialogTitle, myok, mycancel) {
    var d = $('<div style="padding: 10px; max-width: 500px; word-wrap: break-word;">' + dialogText + '</div>').dialog({
        draggable: false,
        modal: true,
        resizable: false,
        width: 'auto',
        title: dialogTitle || 'Confirm',
        minHeight: 75,
        buttons: {
            OK: function () {
                if (typeof (okFunc) == 'function') { setTimeout(okFunc, 50); }
                $(this).dialog('destroy');
            },
            Cancel: function () {
                if (typeof (cancelFunc) == 'function') { setTimeout(cancelFunc, 50); }
                $(this).dialog('destroy');
            }
        }
    });
    //('.ui-dialog-buttonpane button:contains(Cancel)')
    //  $('button:contains(Cancel)', $(d)).html(); 
    //  $('button:contains(Cancel)', $(d)).html($('button:contains(Cancel)', $(d)).replaceAll('Cancel', mycancel));
    $('.ui-dialog-buttonpane button:contains(Cancel)').html($('.ui-dialog-buttonpane button:contains(Cancel)').html().replaceAll('Cancel', mycancel));

    $('.ui-dialog-buttonpane button:contains(OK)').html($('.ui-dialog-buttonpane button:contains(OK)').html().replaceAll('OK', myok));


}


//V2 static
String.format = function () {
    if (arguments.length == 0)
        return null;

    var str = arguments[0];
    for (var i = 1; i < arguments.length; i++) {
        var re = new RegExp('\\{' + (i - 1) + '\\}', 'gm');
        str = str.replace(re, arguments[i]);
    }
    return str;
}
String.prototype.format = function () {
    var args = arguments;
    return this.replace(/\{(\d+)\}/g,
        function (m, i) {
            return args[i];
        });
}
function myMessage(dialogText, dialogTitle) {
    $('<div style="padding: 10px; max-width: 500px; word-wrap: break-word;">' + dialogText + '</div>').dialog({
        draggable: false,
        modal: true,
        resizable: false,
        width: 'auto',
        title: dialogTitle || 'Message',
        minHeight: 75,
        buttons: {
            OK: function () {
                $(this).dialog('destroy');
            }
        }
    });
}

String.prototype.startsWith = function (prefix) {
    return this.indexOf(prefix) === 0;
}
String.prototype.endsWith = function (suffix) {
    return this.match(suffix + "$") == suffix;
}

function SetValue(id, value) {

    var element = $('#' + id);

    if (element.attr("type") == "checkbox") {
        $('#' + id).attr('checked', value);
    } else {
        $('#' + id).val(value);
    }
}
function GetValue(id) {
    var element = $('#' + id);
    if (element.is("input")) {
        // code here
        if (element.attr("type") == "checkbox") {
            return element.is(':checked')
        } else if (element.attr("type") == "radio") {
            return element.is(':checked')
        } else {

            return element.val();
        }
    } else if (element.is("select")) {
        // code here
        return element.val();
    } else {
        return element.val();
    }
    return "no value";
}
var soundEmbed = null;
//======================================================================
function soundPlay(which) {
    if (!soundEmbed) {
        soundEmbed = document.createElement("embed");
        soundEmbed.setAttribute("src", which);
        soundEmbed.setAttribute("hidden", true);
        soundEmbed.setAttribute("autostart", true);
    }
    else {
        document.body.removeChild(soundEmbed);
        soundEmbed.removed = true;
        soundEmbed = null;
        soundEmbed = document.createElement("embed");
        soundEmbed.setAttribute("src", which);
        soundEmbed.setAttribute("hidden", true);
        soundEmbed.setAttribute("autostart", true);
    }
    soundEmbed.removed = false;
    document.body.appendChild(soundEmbed);
}


/*	This work is licensed under Creative Commons GNU LGPL License.

License: http://creativecommons.org/licenses/LGPL/2.1/
Version: 0.9
Author:  Stefan Goessner/2006
Web:     http://goessner.net/ 
*/
function xml2json(xml, tab) {
    var X = {
        toObj: function (xml) {
            var o = {};
            if (xml.nodeType == 1) {   // element node ..
                if (xml.attributes.length)   // element with attributes  ..
                    for (var i = 0; i < xml.attributes.length; i++)
                        o["@" + xml.attributes[i].nodeName] = (xml.attributes[i].nodeValue || "").toString();
                if (xml.firstChild) { // element has child nodes ..
                    var textChild = 0, cdataChild = 0, hasElementChild = false;
                    for (var n = xml.firstChild; n; n = n.nextSibling) {
                        if (n.nodeType == 1) hasElementChild = true;
                        else if (n.nodeType == 3 && n.nodeValue.match(/[^ \f\n\r\t\v]/)) textChild++; // non-whitespace text
                        else if (n.nodeType == 4) cdataChild++; // cdata section node
                    }
                    if (hasElementChild) {
                        if (textChild < 2 && cdataChild < 2) { // structured element with evtl. a single text or/and cdata node ..
                            X.removeWhite(xml);
                            for (var n = xml.firstChild; n; n = n.nextSibling) {
                                if (n.nodeType == 3)  // text node
                                    o["#text"] = X.escape(n.nodeValue);
                                else if (n.nodeType == 4)  // cdata node
                                    o["#cdata"] = X.escape(n.nodeValue);
                                else if (o[n.nodeName]) {  // multiple occurence of element ..
                                    if (o[n.nodeName] instanceof Array)
                                        o[n.nodeName][o[n.nodeName].length] = X.toObj(n);
                                    else
                                        o[n.nodeName] = [o[n.nodeName], X.toObj(n)];
                                }
                                else  // first occurence of element..
                                    o[n.nodeName] = X.toObj(n);
                            }
                        }
                        else { // mixed content
                            if (!xml.attributes.length)
                                o = X.escape(X.innerXml(xml));
                            else
                                o["#text"] = X.escape(X.innerXml(xml));
                        }
                    }
                    else if (textChild) { // pure text
                        if (!xml.attributes.length)
                            o = X.escape(X.innerXml(xml));
                        else
                            o["#text"] = X.escape(X.innerXml(xml));
                    }
                    else if (cdataChild) { // cdata
                        if (cdataChild > 1)
                            o = X.escape(X.innerXml(xml));
                        else
                            for (var n = xml.firstChild; n; n = n.nextSibling)
                                o["#cdata"] = X.escape(n.nodeValue);
                    }
                }
                if (!xml.attributes.length && !xml.firstChild) o = null;
            }
            else if (xml.nodeType == 9) { // document.node
                o = X.toObj(xml.documentElement);
            }
            else
                alert("unhandled node type: " + xml.nodeType);
            return o;
        },
        toJson: function (o, name, ind) {
            var json = name ? ("\"" + name + "\"") : "";
            if (o instanceof Array) {
                for (var i = 0, n = o.length; i < n; i++)
                    o[i] = X.toJson(o[i], "", ind + "\t");
                json += (name ? ":[" : "[") + (o.length > 1 ? ("\n" + ind + "\t" + o.join(",\n" + ind + "\t") + "\n" + ind) : o.join("")) + "]";
            }
            else if (o == null)
                json += (name && ":") + "null";
            else if (typeof (o) == "object") {
                var arr = [];
                for (var m in o)
                    arr[arr.length] = X.toJson(o[m], m, ind + "\t");
                json += (name ? ":{" : "{") + (arr.length > 1 ? ("\n" + ind + "\t" + arr.join(",\n" + ind + "\t") + "\n" + ind) : arr.join("")) + "}";
            }
            else if (typeof (o) == "string")
                json += (name && ":") + "\"" + o.toString() + "\"";
            else
                json += (name && ":") + o.toString();
            return json;
        },
        innerXml: function (node) {
            var s = ""
            if ("innerHTML" in node)
                s = node.innerHTML;
            else {
                var asXml = function (n) {
                    var s = "";
                    if (n.nodeType == 1) {
                        s += "<" + n.nodeName;
                        for (var i = 0; i < n.attributes.length; i++)
                            s += " " + n.attributes[i].nodeName + "=\"" + (n.attributes[i].nodeValue || "").toString() + "\"";
                        if (n.firstChild) {
                            s += ">";
                            for (var c = n.firstChild; c; c = c.nextSibling)
                                s += asXml(c);
                            s += "</" + n.nodeName + ">";
                        }
                        else
                            s += "/>";
                    }
                    else if (n.nodeType == 3)
                        s += n.nodeValue;
                    else if (n.nodeType == 4)
                        s += "<![CDATA[" + n.nodeValue + "]]>";
                    return s;
                };
                for (var c = node.firstChild; c; c = c.nextSibling)
                    s += asXml(c);
            }
            return s;
        },
        escape: function (txt) {
            return txt.replace(/[\\]/g, "\\\\")
                   .replace(/[\"]/g, '\\"')
                   .replace(/[\n]/g, '\\n')
                   .replace(/[\r]/g, '\\r');
        },
        removeWhite: function (e) {
            e.normalize();
            for (var n = e.firstChild; n;) {
                if (n.nodeType == 3) {  // text node
                    if (!n.nodeValue.match(/[^ \f\n\r\t\v]/)) { // pure whitespace text node
                        var nxt = n.nextSibling;
                        e.removeChild(n);
                        n = nxt;
                    }
                    else
                        n = n.nextSibling;
                }
                else if (n.nodeType == 1) {  // element node
                    X.removeWhite(n);
                    n = n.nextSibling;
                }
                else                      // any other node
                    n = n.nextSibling;
            }
            return e;
        }
    };
    if (xml.nodeType == 9) // document node
        xml = xml.documentElement;
    var json = X.toJson(X.toObj(X.removeWhite(xml)), xml.nodeName, "\t");
    return "{\n" + tab + (tab ? json.replace(/\t/g, tab) : json.replace(/\t|\n/g, "")) + "\n}";
}
/*	This work is licensed under Creative Commons GNU LGPL License.

License: http://creativecommons.org/licenses/LGPL/2.1/
Version: 0.9
Author:  Stefan Goessner/2006
Web:     http://goessner.net/ 
*/
function json2xml(o, tab) {
    var toXml = function (v, name, ind) {
        var xml = "";
        if (v instanceof Array) {
            for (var i = 0, n = v.length; i < n; i++)
                xml += ind + toXml(v[i], name, ind + "\t") + "\n";
        }
        else if (typeof (v) == "object") {
            var hasChild = false;
            xml += ind + "<" + name;
            for (var m in v) {
                if (m.charAt(0) == "@")
                    xml += " " + m.substr(1) + "=\"" + v[m].toString() + "\"";
                else
                    hasChild = true;
            }
            xml += hasChild ? ">" : "/>";
            if (hasChild) {
                for (var m in v) {
                    if (m == "#text")
                        xml += v[m];
                    else if (m == "#cdata")
                        xml += "<![CDATA[" + v[m] + "]]>";
                    else if (m.charAt(0) != "@")
                        xml += toXml(v[m], m, ind + "\t");
                }
                xml += (xml.charAt(xml.length - 1) == "\n" ? ind : "") + "</" + name + ">";
            }
        }
        else {
            if (typeof (v) != "function")

                xml += ind + "<" + name + ">" + v.toString() + "</" + name + ">";
        }
        return xml;
    }, xml = "";
    for (var m in o)
        xml += toXml(o[m], "A", "");
    //  xml += toXml(o[m], m, "");
    return tab ? xml.replace(/\t/g, tab) : xml.replace(/\t|\n/g, "");
}


String.prototype.replaceAll = function (findWith, replaceWith) {
    regex = new RegExp(findWith, 'g');
    return this.replace(regex, replaceWith);
}

function GetTimezone() {
    var offset = new Date().getTimezoneOffset();
    offset = offset / 60;
    return offset + 1;
}

function getCaret(el) {
    if (el.selectionStart) {
        return el.selectionStart;
    } else if (document.selection) {
        el.focus();

        var r = document.selection.createRange();
        if (r == null) {
            return 0;
        }

        var re = el.createTextRange(),
        rc = re.duplicate();
        re.moveToBookmark(r.getBookmark());
        rc.setEndPoint('EndToStart', re);

        var add_newlines = 0;
        for (var i = 0; i < rc.text.length; i++) {
            if (rc.text.substr(i, 2) == '\r\n') {
                add_newlines += 2;
                i++;
            }
        }

        //return rc.text.length + add_newlines;

        //We need to substract the no. of lines
        return rc.text.length - add_newlines;
    }
    return 0;
}




function IsInArray(arr, val) {

    var testStr = ',' + arr.join(",") + ",";

    return testStr.indexOf("," + val + ",") != -1;

}





function insertAtCursor(myField, myValue) {
    var cursorPos = $('#' + myField).prop('selectionStart');
    var v = $('#' + myField).val();
    var textBefore = v.substring(0, cursorPos);
    var textAfter = v.substring(cursorPos, v.length);

    $('#' + myField).val(textBefore + myValue + textAfter);
}

function LoadDDL(name , callBack) {

   var url = km.model.urls["ddler"] + "&ddl=" + ddl;


}