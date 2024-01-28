/**
 * Created by fc on 2017/5/30.
 */

//封装js
function ajax(){
    var ajaxData = {
        type:arguments[0].type || "GET",
        url:arguments[0].url || "",
        async:arguments[0].async || "true",
        data:arguments[0].data || null,
        dataType:arguments[0].dataType || "text",
        contentType:arguments[0].contentType || "application/x-www-form-urlencoded",
        beforeSend:arguments[0].beforeSend || function(){},
        success:arguments[0].success || function(){},
        error:arguments[0].error || function(){}
    };
    ajaxData.beforeSend();
    var xhr = createxmlHttpRequest();
    xhr.responseType=ajaxData.dataType;
    xhr.open(ajaxData.type,ajaxData.url,ajaxData.async);
    xhr.setRequestHeader("Content-Type",ajaxData.contentType);
    xhr.send(convertData(ajaxData.data));
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4) {
            if(xhr.status == 200){
                ajaxData.success(xhr.response)
            }else{
                ajaxData.error()
            }
        }
    }
}

function createxmlHttpRequest() {
    if (window.ActiveXObject) {
        return new ActiveXObject("Microsoft.XMLHTTP");
    } else if (window.XMLHttpRequest) {
        return new XMLHttpRequest();
    }
}

function convertData(data){
    if( typeof data === 'object' ){
        var convertResult = "" ;
        for(var c in data){
            convertResult+= c + "=" + data[c] + "&";
        }
        convertResult=convertResult.substring(0,convertResult.length-1);
        return convertResult;
    }else{
        return data;
    }
}
function  tip(t) {
    document.getElementById("contact-tip").innerText = t;
    document.getElementById("contact-tip").style.webkitTransform = "scale(1)";
    document.getElementById("contact-tip").style.transform = "scale(1)";
    setTimeout(function () {
        document.getElementById("contact-tip").style.webkitTransform = "scale(0)";
        document.getElementById("contact-tip").style.transform = "scale(0)";
    },2000);
}


var checkbg = "#A7A7A7";
//内容页用户设置
function nr_setbg(intype){

    var huyandiv = document.getElementById("huyandiv");
    var light = document.getElementById("lightdiv");
    if(intype == "huyan"){
        if(huyandiv.style.backgroundColor == ""){
            set("light","huyan");
            document.cookie="light=huyan;path=/";
        }
        else{
            set("light","no");
            document.cookie="light=no;path=/";
        }
    }
    if(intype == "light"){

        if(light.innerText == "关灯"){
            set("light","yes");
            document.cookie="light=yes;path=/";
        }
        else{
            set("light","no");
            document.cookie="light=no;path=/";
        }
    }
    if(intype == "big"){
        set("font","big");
        document.cookie="font=big;path=/";
    }
    if(intype == "middle"){
        set("font","middle");
        document.cookie="font=middle;path=/";
    }
    if(intype == "small"){
        set("font","small");
        document.cookie="font=small;path=/";
    }
}

//内容页读取设置
function getset(){
    var strCookie=document.cookie;
    var arrCookie=strCookie.split("; ");
    var light;
    var font;

    for(var i=0;i<arrCookie.length;i++){
        var arr=arrCookie[i].split("=");
        if("light"==arr[0]){
            light=arr[1];
            break;
        }
    }
    for(var i=0;i<arrCookie.length;i++){
        var arr=arrCookie[i].split("=");
        if("font"==arr[0]){
            font=arr[1];
            break;
        }
    }

    //light
    if(light == "yes"){
        set("light","yes");
    }
    else if(light == "no"){
        set("light","no");
    }
    else if(light == "huyan"){
        set("light","huyan");
    }
    //font
    if(font == "big"){
        set("font","big");
    }
    else if(font == "middle"){
        set("font","middle");
    }
    else if(font == "small"){
        set("font","small");
    }
    else{
        set("","");
    }
}

//内容页应用设置
function set(intype,p){
    var BookBody = document.getElementById("BookBody");//页面body
    var huyandiv = document.getElementById("huyandiv");//护眼div
    var lightdiv = document.getElementById("lightdiv");//灯光div
    var fontfont = document.getElementById("fontfont");//字体div
    var fontbig = document.getElementById("fontbig");//大字体div
    var fontmiddle = document.getElementById("fontmiddle");//中字体div
    var fontsmall = document.getElementById("fontsmall");//小字体div
    var txt =  document.getElementById("text");//内容div
    var footer =  document.getElementById("footer");
    var BookTitle =  document.getElementById("nr_title");//文章标题
    var page1 = document.getElementById("nr_page1");//上目录链接
    var page2 = document.getElementById("nr_page2");//上目录链接
    var set = document.getElementById("nr_set");
    //var pt_prev =  document.getElementById("shujia");
    //灯光
    if(intype == "light"){
        if(p == "yes"){
            //关灯
            lightdiv.innerText = "开灯";

            BookBody.style.backgroundColor = "#5A5A5A";
            footer.style.color = "#ccc";
            footer.style.backgroundColor = "#5A5A5A";
            huyandiv.style.backgroundColor = "";
            BookTitle.style.color = "#ccc";
            txt.style.color = "#ccc";
            set.style.color = "#ccc";
            for(var i=0;i<3;i++){
                page1.querySelectorAll("div a")[i].style.color = "#ccc";
                page2.querySelectorAll("div a")[i].style.color = "#ccc";
            }
            //pt_prev.style.cssText = "background-color:#222;color:#fff;border:1px solid #fff";
        }
        else if(p == "no"){
            //开灯
            lightdiv.innerText = "关灯";
            BookBody.style.backgroundColor = "#fff";
            footer.style.color = "#333";
            footer.style.backgroundColor = "#fff";
            txt.style.color = "#333";
            BookTitle.style.color = "#333";
            huyandiv.style.backgroundColor = "";
            set.style.color = "#333";
            for(var i=0;i<3;i++){
                page1.querySelectorAll("div a")[i].style.color = "#333";
                page2.querySelectorAll("div a")[i].style.color = "#333";
            }
            //pt_prev.style.cssText = "";
        }
        else if(p == "huyan"){
            //护眼
            lightdiv.innerText = "关灯";
            huyandiv.style.backgroundColor = checkbg;
            BookBody.style.backgroundColor = "#FBF6EC";
            BookTitle.style.color = "#333";
            footer.style.backgroundColor = "#FBF6EC";
            txt.style.color = "#333";
            set.style.color = "#333";
            for(var i=0;i<3;i++){
                page1.querySelectorAll("div a")[i].style.color = "#333";
                page2.querySelectorAll("div a")[i].style.color = "#333";
            }
            //pt_prev.style.cssText = "background-color:#0E7A18;color:#000;border:1px solid #13A422";
        }
    }
    //字体
    if(intype == "font"){
        //alert(p);
        fontbig.style.backgroundColor = "";
        fontmiddle.style.backgroundColor = "";
        fontsmall.style.backgroundColor = "";
        if(p == "big"){
            fontbig.style.backgroundColor = checkbg;
            txt.style.fontSize = "28px";
        }
        if(p == "middle"){
            fontmiddle.style.backgroundColor = checkbg;
            txt.style.fontSize = "24px";
        }
        if(p == "small"){
            fontsmall.style.backgroundColor = checkbg;
            txt.style.fontSize = "18px";
        }
    }
}


