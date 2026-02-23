;(function(){
    var centerObj= new Object();
    centerObj.w=1024;
    centerObj.h=682;
    centerObj.maxBox=new HGAME.canvas({
        w:centerObj.w,
        h:centerObj.h
    });
    centerObj.start="none";
    centerObj.animate=new HGAME.animate();
    centerObj.loedSource=new HGAME.source();
    centerObj.cj=0;
    centerObj.canvas=document.createElement("canvas");
    centerObj.model=new HGAME.model();
    window.myTest=centerObj.model;
    centerObj.ele=document.getElementById("demo");
    centerObj.goldInfo={
        w:60,
        h:60,
        targetRect:{
            x:170,
            y:604,
            w:160,
            h:60
        }
    };
    centerObj.imgInfoInterface={};
    centerObj.rectInfoInterface={};
    centerObj.jnInfo={};
    centerObj.bufObj={};
    centerObj.createRect=false;
    centerObj.fishRectTime=200;
    centerObj.cxsjRect=45;
    centerObj.fishRectTimeBuf=200;
    centerObj.cxsjRectBuf=45;
    centerObj.nowFishRect=0;
    centerObj.bufObj.jn={
        x:0,
        y:0
    };
    centerObj.jnInfo.wpObj={
        time:0,
        img:METHOD.createImg( "img/Interface/jn1.png"),
        txt:{
            txt:"万网齐发",
            x:10,
            y:55
        },
        x:300,
        y:580,
        w:60,
        h:60,
        action:function(){
            if(this.time>0){
                var txt =centerObj.maxBox.txt;
                txt.font="normal normal 12px/16px arial";
                txt.fillStyle="#ffffff";
                txt.textBaseline="top";
                txt.textAlign="left";
                var wds = txt.measureText("x"+this.txt.txt).width;
                txt.drawImage(this.img,this.txt.x,this.txt.y,20,20);
                txt.fillText(this.txt.txt+this.time,this.txt.x+20,this.txt.y+4);
                if(Math.random()>0.6){
                    var bullteB=new HGAME.bulletB({
                        noDeathImg:centerObj.p.bulletImgArr[centerObj.p.nowImg],
                        deathImg:centerObj.p.gridImgArr[centerObj.p.nowImg],
                        belong:centerObj.p,
                        angle:0,
                        x:Math.random()*1024,
                        y:centerObj.h+10,
                        hurtInfo:centerObj.p.nowImg
                    });
                    centerObj.bulletArr.push(bullteB);
                    centerObj.maxBox.add(bullteB);
                }


            }
        },
        clickFun:function(){
            if(this.num-1>=0&&this.time<=0){
                this.time=25;
                this.num--;
                localStorage.jNwp=this.num;
            }

        },
        sAction:function(){
            if(this.time>0){
                this.time--;
            }else{
                this.time=0;
            }
        }
    };

    METHOD.defineEx(centerObj.jnInfo.wpObj,'num',(typeof localStorage.jNwp)!="undefined"?localStorage.jNwp:3,function(){
        localStorage.jNwp=this.num;
    });
    METHOD.defineEx(centerObj,"wpNum",centerObj.jnInfo.wpObj.num,function(){
        centerObj.jnInfo.wpObj.num=this.wpNum;
    });
    centerObj.animate02=new HGAME.animate({time:90});
    centerObj.addNumTime=30;
    centerObj.animate02.action=function(){
        var i = 0,q=0;
        for(i = 0;i<centerObj.fishArr.length;i++){
            if(typeof centerObj.fishArr[i]=="undefined")continue;
            if(!centerObj.fishArr[i].method02){continue}
            for(q=0;q<centerObj.fishArr[i].method02.length;q++){
                if(centerObj.fishArr[i].method02[q].centerObj){
                    centerObj.fishArr[i][centerObj.fishArr[i].method02[q].name]&&centerObj.fishArr[i][centerObj.fishArr[i].method02[q].name](centerObj);
                }else{
                    centerObj.fishArr[i][centerObj.fishArr[i].method02[q].name]&&centerObj.fishArr[i][centerObj.fishArr[i].method02[q].name]();
                }
                if(typeof centerObj.fishArr[i]=="undefined")break;
            }
        }

        for(i=0;i<centerObj.bulletArr.length;i++){
            centerObj.bulletArr[i].changeImageInfo();
        }
    };
    centerObj.animate03=new HGAME.animate({time:60});
    centerObj.animate03.action=function(){
        for(var i=0;i<centerObj.goldArr.length;i++){
            centerObj.goldArr[i].changeImgInfo();
            centerObj.goldArr[i].changeXYInfo(centerObj);
        }
    };
    centerObj.animate.aSecondAction=function(){
        for(var o in     centerObj.jnInfo){
            centerObj.jnInfo[o].sAction.call(centerObj.jnInfo[o]);
        }
        if(centerObj.num<=50){
            if( centerObj.addNumTime<=0){
                centerObj.num=parseInt(centerObj.num)+5;
                centerObj.addNumTime=30;
            }else{
                centerObj.addNumTime=centerObj.addNumTime-1;
            }
        }else{
            centerObj.addNumTime=0;
        }
        if(centerObj.createRect==false){
            if(centerObj.fishRectTime-1<0){
                var info = METHOD.getRandomItem(cjData[centerObj.cj][3]);
                if(typeof info=="undefined"){
                    centerObj.createRect=false;
                    centerObj.fishRectTime=centerObj.fishRectTimeBuf;
                    return 0;
                }else{
                    centerObj.nowFishRect=info.num;
                }
                centerObj.fishRectTime=0;
                centerObj.createRect=true;
                centerObj.cxsjRect=info.time;
                for(var i = 0;i<centerObj.createFishArr.length;i++){
                    //createTime
                    //createTimeBuf
                    if(centerObj.createFishArr[i].fishType=="rect"+info.num){
                        console.log(centerObj.createFishArr[i].createTimeBufBuf);
                        centerObj.createFishArr[i].createAllTime=  centerObj.createFishArr[i].createAllTimeBuf;
                        centerObj.createFishArr[i].createTime= centerObj.createFishArr[i].createTimeBufBuf;
                    }

                }
            }else{
                centerObj.fishRectTime--;
            }
        }else{
            if(centerObj.cxsjRect-1<0){
                centerObj.fishRectTime=0;
                centerObj.createRect=false;
                centerObj.fishRectTime=centerObj.fishRectTimeBuf;
            }else{
                centerObj.cxsjRect--;
            }
        }

    };
    centerObj.animate.action=function(){
        var i = 0;
        var q = 0;
        centerObj.maxBox.render();
        centerObj.actionAfter();
        for(var o in centerObj.jnInfo){
            centerObj.jnInfo[o].action.call(centerObj.jnInfo[o]);
        }
        centerObj.p.changeImgInfo();
        /*fishT.changeImgInfo();
        fishT.changeAngle();
        fishT.moveForward();
        fishT.isScreenOut(centerObj);
        fishT.deathAfter(centerObj);*/
        for(;i<centerObj.bulletArr.length;i++){
            if(centerObj.bulletArr[i].type!=2){
                centerObj.bulletArr[i].moveForward();
            }

            centerObj.bulletArr[i].isScreenOut(centerObj);
            centerObj.bulletArr[i].colFish(centerObj);
            centerObj.bulletArr[i]&&centerObj.bulletArr[i].deathChangeAfter(centerObj);
        }
        for(i = 0;i<centerObj.fishArr.length;i++){
            if(typeof centerObj.fishArr[i]=="undefined")continue;
            if(centerObj.fishArr[i].fishType=="ySmall"){

                if(centerObj.createRect==true){
                    centerObj.fishArr[i].isChangeAngle=false;
                }else{
                    centerObj.fishArr[i].isChangeAngle=true;
                }
            }

            if(!centerObj.fishArr[i].method){continue}

            for(q=0;q<centerObj.fishArr[i].method.length;q++){

                if(centerObj.fishArr[i].method[q].centerObj){
                    centerObj.fishArr[i][centerObj.fishArr[i].method[q].name]&&centerObj.fishArr[i][centerObj.fishArr[i].method[q].name](centerObj);
                }else{
                    centerObj.fishArr[i][centerObj.fishArr[i].method[q].name]&&centerObj.fishArr[i][centerObj.fishArr[i].method[q].name]();
                }
                if(typeof centerObj.fishArr[i]=="undefined")return;
            }
        }
        for(i = 0;i<centerObj.createFishArr.length;i++){
            if(centerObj.createRect==true){
                if( centerObj.createFishArr[i].fishType=="rect"+centerObj.nowFishRect){
                    centerObj.createFishArr[i].createFish(centerObj);
                }
            }else{
                if( centerObj.createFishArr[i].fishType=="ySmall"){
                    centerObj.createFishArr[i].createFish(centerObj);
                }
            }

        }

    };
    centerObj.imgNum=new Image();
    centerObj.imgNum2=new Image();
    centerObj.imgGlod=new Image();
    centerObj.imgGlod2=new Image();
    centerObj.rectInfoInterface.back={
        x:10,
        y:15,
        w:40,
        h:35,
        clickFun:function(){
            selctUI(centerObj.maxBox.txt);
        }
    };

    centerObj.actionAfter=function(){
        var str = ""+centerObj.num;
        var x = 148;
        var y = 657;
        var w = 36;
        var h = 49;
        var txt = centerObj.maxBox.txt;
        txt.beginPath();
        function a(){
            str="0"+str;
            if(str.length<6){
                a();
            }
        }
        if(str.length<6){
            a();
        }
        var Iint=0;
        for(var i = 0;i<str.length;i++){
            Iint= parseFloat(str[i]);
            txt.drawImage(centerObj.imgNum,w*Iint,0,w,h,x+i*w/1.5,y,w/2.5,h/2.5);
           //
        }
        txt.drawImage(centerObj.addRect.img,centerObj.addRect.x,centerObj.addRect.y);

        txt.drawImage(centerObj.noAddRect.img,centerObj.noAddRect.x,centerObj.noAddRect.y);
        for(var d in centerObj.rectInfoInterface){
            txt.drawImage(centerObj.imgInfoInterface[d],centerObj.rectInfoInterface[d].x,centerObj.rectInfoInterface[d].y,
                centerObj.rectInfoInterface[d].w,centerObj.rectInfoInterface[d].h);
        }
        for(d in centerObj.jnInfo){
                txt.drawImage(centerObj.jnInfo[d].img,centerObj.jnInfo[d].x,centerObj.jnInfo[d].y,
                centerObj.jnInfo[d].w,centerObj.jnInfo[d].h);
                txt.font="normal normal 20px/24px arial";
                txt.fillStyle="#ffffff";
                txt.textBaseline="top";
                txt.textAlign="left";
                var wds = txt.measureText("x"+centerObj.jnInfo[d].num).width;
                txt.fillText("x"+centerObj.jnInfo[d].num,centerObj.jnInfo[d].x+centerObj.jnInfo[d].w-wds-5,centerObj.jnInfo[d].y+centerObj.jnInfo[d].h-24);
        }
        txt.closePath();
        str="";

        if(centerObj.addNumTime<=9){
            str="0"+centerObj.addNumTime
        }else{
            str=""+centerObj.addNumTime
        }
        for(var  o = 0;o<str.length;o++){
            txt.beginPath();
            txt.drawImage(centerObj.imgNum2,0,240-24*parseInt(str[o])-24,20,24,300+20*o,658,20,24);
            txt.closePath();
        }
        txt.fillText("返回",55,22);
        txt.fillText("灰灰世界",930,22);
        txt.textBaseline="middle";
        txt.textAlign="center";
        if(centerObj.createRect==false){
            str="鱼群到来"+centerObj.fishRectTime;
        }else{
            str="鱼群来啦"+centerObj.cxsjRect;
        }
        txt.fillText(str,centerObj.w/2,22);
        
        powerInfoFun(txt);
    };
    centerObj.bufObj.power={
        img100:METHOD.createImg("img/Interface/energy-bar.png"),
        powerRect:{
            w:270,
            h:270,x:417,y:500
        },
        noDeathArr:[
            METHOD.createImg("img/pwoerPd/JadePerch_IN_Particles_01-hd.png"),
            METHOD.createImg("img/pwoerPd/JadePerch_IN_Particles_02-hd.png"),
            METHOD.createImg("img/pwoerPd/JadePerch_IN_Particles_03-hd.png"),
            METHOD.createImg("img/pwoerPd/JadePerch_IN_Particles_04-hd.png"),
            METHOD.createImg("img/pwoerPd/JadePerch_IN_Particles_05-hd.png"),
            METHOD.createImg("img/pwoerPd/JadePerch_IN_Particles_06-hd.png"),
            METHOD.createImg("img/pwoerPd/JadePerch_IN_Particles_07-hd.png"),
            METHOD.createImg("img/pwoerPd/JadePerch_IN_Particles_08-hd.png")
        ],
        deathArr:[
            METHOD.createImg("img/pwoerPd/JadePerch_Particles_01-hd.png"),
            METHOD.createImg("img/pwoerPd/JadePerch_Particles_02-hd.png"),
            METHOD.createImg("img/pwoerPd/JadePerch_Particles_03-hd.png"),
            METHOD.createImg("img/pwoerPd/JadePerch_Particles_04-hd.png"),
            METHOD.createImg("img/pwoerPd/JadePerch_Particles_05-hd.png")
        ],
        x:674,
        y:655,
        w:213,
        h:19,

        nowImg:0
    };
    METHOD.defineEx(centerObj.bufObj.power,"ingInfo",typeof localStorage.ingInfo!="undefined"?localStorage.ingInfo:0.5,function(){
        localStorage.ingInfo=this.ingInfo;
    });

    function powerInfoFun(txt){
      //  debugger;
        txt.drawImage(centerObj.bufObj.power.img100,centerObj.bufObj.power.x,centerObj.bufObj.power.y,centerObj.bufObj.power.w*centerObj.bufObj.power.ingInfo,centerObj.bufObj.power.h);
        if(centerObj.bufObj.power.ingInfo>=1){
            if(centerObj.bufObj.power.nowImg+1<=centerObj.bufObj.power.noDeathArr.length-1){
                centerObj.bufObj.power.nowImg=centerObj.bufObj.power.nowImg+1
            }else{
                centerObj.bufObj.power.nowImg=0;
            }
            //debugger;
            txt.drawImage(centerObj.bufObj.power.noDeathArr[centerObj.bufObj.power.nowImg],
                centerObj.bufObj.power.powerRect.x,centerObj.bufObj.power.powerRect.y,centerObj.bufObj.power.powerRect.w,centerObj.bufObj.power.powerRect.h);

        }

    };
    function getAnimateArr(imgInfo,ty){

        imgInfo=imgInfo||"1x8";
        var arr = new Array();
        var arr02 = new Array();
        function fun(num,w,h){
            var i = 0;
            if(num==0){
                for(;i<h/2;i++){
                    arr.push({w:0,h:i});
                    arr02.push({w:0,h:h/2+i});
                }
            }else if(num==1){
                for(i=0;i< h;i++){
                    arr.push({w:0,h:i});
                }
            }else if(num==2){
                var a=h/3;
                for(i=0;i< h;i++){
                    if(i>a*2-1){
                        arr02.push({w:0,h:i});
                    }else{
                        arr.push({w:0,h:i});
                    }
                }
            }else if(num==3&&h==10){
                for(i=0;i< h;i++){
                    if(i>5){
                        arr02.push({w:0,h:i});
                    }else{
                        arr.push({w:0,h:i});
                    }
                }
            }else if(num==4&&h==15){
                for(i=0;i< h;i++){
                    if(i>13){
                        arr02.push({w:0,h:i});
                    }else{
                        arr.push({w:0,h:i});
                    }
                }
            }else if(num==5&&h==33){
                for(i=0;i< h;i++){
                    if(i>29){
                        arr02.push({w:0,h:i});
                    }else{
                        arr.push({w:0,h:i});
                    }
                }
            }
        }
        switch (imgInfo){
            case "1x8":{
                switch (ty){
                    case "0":{
                        fun(0,1,8);
                        break;
                    }
                }
                break;
            }
            case "1x12":{
                switch (ty){
                    case "0":{
                        fun(0,1,12);
                        break;
                    }
                    case "2":{
                        fun(2,1,12);
                    }
                }
                break;
            }
            case '1x10':{
                switch (ty) {
                    case "0":{
                        fun(0,1,10);
                        break;
                    }
                    case "1":{
                        fun(1,1,10);
                        break;
                    }
                    case "3":{
                        fun(3,1,10);
                        break;
                    }
                }
                break;
            }
            case "1x15":{
                switch (ty){
                    case "4":{
                        fun(4,1,15);
                    }
                        break;
                }
                break;
            }
            case "1x33":{
                switch (ty){
                    case "5":{
                        fun(5,1,33);
                    }
                }
                break;
            }
            case "1x5":{
                switch (ty){
                    case "1":{
                        fun(1,1,5);
                        break;
                    }
                }
                break;
            }
        }
        if(ty=='0'||ty=="2"||ty=="3"||ty=="4"||ty=="5"){
            return {
                a:arr,
                b:arr02
            }
        }else if(ty=="1"){
            return arr;
        }

    }
    centerObj.goldInfo.imgInfoArr=getAnimateArr("1x10","1");
    function getCreateInfo(O){
        var yInfo=getAnimateArr(O.imgInfoAg, O.imgInfoAg02);
        O.swimArr=yInfo.a;
        O.deathArray=yInfo.b;
    }
    centerObj.loedSource.loadCall=function(a,b){
        var txt = centerObj.maxBox.txt;
        txt.beginPath();
        txt.clearRect(0,0,centerObj.w,centerObj.h);
        txt.font="normal normal 20px/24px arial";
        txt.textBaseline="middle";
        txt.textAlign="center";
        txt.fillStyle="#000000";
        txt.fillRect(0,0,centerObj.w,centerObj.h);
        txt.fillStyle="#ffffff";
        txt.fillText("加载资源:"+a+"/"+b,centerObj.w/2,centerObj.h/2);
        txt.closePath();
    };
    centerObj.cjShowArr=[
        {
            img:METHOD.createImg("img/Interface/e.jpg"),
            w:240,
            h:164,
            index:0,
            needNum:0,
            say:"这里有时候会出现灯笼鱼"
        },
        {
            img:METHOD.createImg("img/Interface/game_bg_2_hd.jpg"),
            w:240,
            h:164,
            index:1,
            needNum:5000,
            say:"这里有时候会出现电鳗鱼"
        },
        {
            img:METHOD.createImg("img/Interface/bg1.jpg"),
            w:240,
            h:164,
            index:2,
            needNum:10000,
            say:"这里有时候会出现大乌龟"
        },
        {
            img:METHOD.createImg("img/Interface/startbg.jpg"),
            w:240,
            h:164,
            index:3,
            needNum:20000,
            say:"这里有时候会出现鲨鱼"
        },
        {
            img:METHOD.createImg("img/Interface/b.jpg"),
            w:240,
            h:164,
            index:4,
            needNum:40000,
            say:"这里有时候会出现黄金大鲨鱼"
        },
        {
            img:METHOD.createImg("img/Interface/c.jpg"),
            w:240,
            h:164,
            index:5,
            needNum:80000,
               say:"这里有时候会出现大珍珠"
        },
        {
            img:METHOD.createImg("img/Interface/d.jpg"),
            w:240,
            h:164,
            index:6,
            needNum:100000,
            say:"这里会出现传说中的美人鱼"
        }
    ];
    var imgStartbg = METHOD.createImg( "img/Interface/startbg.jpg");
    function emptyFun(){
        centerObj.fishArr= new Array();
        centerObj.bulletArr=new Array();
        centerObj.createFishArr=new Array();
        centerObj.goldArr=new Array();
        centerObj.animate.stop();
        centerObj.animate02.stop();
        centerObj.animate03.stop();
        centerObj.maxBox.empty();
    }
    function initCj(num){


        centerObj.num=localStorage.num?localStorage.num:1000;
        centerObj.cj=num;
        if(!cjData[centerObj.cj])return console.log("error:loaded error !!");
        centerObj.start="loadeding";
        emptyFun();
        centerObj.maxBox.add(centerObj.pt);
        centerObj.maxBox.add(centerObj.p);

        centerObj.loedSource.loadedSource(cjData[centerObj.cj][0],function(){
            //  var yInfo=getAnimateArr("1x8","0");
            var i = 0;
            for(;i<cjData[centerObj.cj][1].length;i++){
                getCreateInfo( cjData[centerObj.cj][1][i]);
                var a = new HGAME.fishStruct(cjData[centerObj.cj][1][i]);
                centerObj.createFishArr.push(a);
            }
            var bg = new HGAME.Object2D({
                img:METHOD.createImg(cjData[centerObj.cj][2]),
                w:centerObj.w,
                h:centerObj.h,
                x:0,
                y:0
            });
            centerObj.maxBox.add(bg);
            centerObj.animate.run();
            centerObj.animate02.run();
            centerObj.animate03.run();
            centerObj.start="begin";
        });
    };

    function selctUI(txt,text){
        emptyFun();
        text=text||"";
        var  Y=80;
        centerObj.start="selecting";
        txt.beginPath();
        txt.clearRect(0,0,centerObj.w,centerObj.h);
        txt.drawImage(imgStartbg,0,0);
        txt.textBaseline="top";
        txt.textAlign="left";
        txt.fillStyle="#ffffff";
        txt.font="normal normal 20px/24px arial";
        txt.fillText("选择场景:"+text,10,Y);
        txt.fillStyle="#ffff00";
        txt.font="normal normal 16px/20px arial";
        txt.fillText("您的分数:"+centerObj.num,10,Y-25);
        Y=Y+24+10+20;
        var x =8;
        var y=Y;
        var int =0;
        for(var i = 0;i< centerObj.cjShowArr.length;i++){
            var img=centerObj.cjShowArr[i].img;

            txt.drawImage(img,0,0,img.width,img.height,x,y,centerObj.cjShowArr[i].w,centerObj.cjShowArr[i].h);
            txt.fillStyle="rgba(0,0,0,0.8)";
            txt.fillRect(x,y+centerObj.cjShowArr[i].h-80,centerObj.cjShowArr[i].w,80);
            txt.font="normal normal 16px/20px arial";
            txt.fillStyle="#ffffff";
            txt.fillText(centerObj.cjShowArr[i].say,x+10,y+centerObj.cjShowArr[i].h+20-80);
            txt.fillStyle="#ffff00";
            txt.fillText("需求分数:"+centerObj.cjShowArr[i].needNum,x+10,y+centerObj.cjShowArr[i].h+10-40);
            centerObj.cjShowArr[i].x=x;
            centerObj.cjShowArr[i].y=y;
            x=x+centerObj.cjShowArr[i].w+16;
            if(int==3){
                int=0;
                x=8;
                y=y+centerObj.cjShowArr[i].h+100;
            }else{
                int++;
            }


        }
        txt.closePath();
    }
    function startUI(txt){
        emptyFun();
        centerObj.start="loading";
        var startRect =centerObj.startRect;
        txt.beginPath();
        txt.clearRect(0,0,centerObj.w,centerObj.h);
        txt.drawImage(imgStartbg,0,0);
        txt.drawImage(METHOD.createImg( "img/Interface/login.png"),centerObj.w/2-387/2,centerObj.h/2-287/2-80);
        txt.fillStyle="#0994ff";
        txt.shadowBlur=20;
        txt.shadowColor="#098eff";
        txt.fillRect(startRect.x,startRect.y,startRect.w,startRect.h);
        txt.shadowBlur=0;
        txt.textBaseline="middle";
        txt.font="normal normal 20px/24px arial";
        txt.textAlign="center";
        txt.fillStyle="#ffffff";

        txt.fillText("开始游戏",startRect.x+startRect.w/2,startRect.y+startRect.h/2);
        txt.closePath();
    }
    centerObj.startRect=  {
        x:centerObj.w/2-200/2,y:centerObj.h/2-60/2+100,
        w:200,
        h:60
    };

    centerObj.loedSource.loadedSource([
        "img/Interface/cannon_minus.png",
        "img/Interface/startbg.jpg",
        "img/pwoerPd/JadePerch_IN_Particles_01-hd.png",
        "img/pwoerPd/JadePerch_IN_Particles_02-hd.png",
        "img/pwoerPd/JadePerch_IN_Particles_03-hd.png",
        "img/pwoerPd/JadePerch_IN_Particles_04-hd.png",
        "img/pwoerPd/JadePerch_IN_Particles_05-hd.png",
        "img/pwoerPd/JadePerch_IN_Particles_06-hd.png",
        "img/pwoerPd/JadePerch_IN_Particles_07-hd.png",
        "img/pwoerPd/JadePerch_IN_Particles_08-hd.png",
        "img/pwoerPd/JadePerch_Particles_01-hd.png",
        "img/pwoerPd/JadePerch_Particles_02-hd.png",
        "img/pwoerPd/JadePerch_Particles_03-hd.png",
        "img/pwoerPd/JadePerch_Particles_04-hd.png",
        "img/pwoerPd/JadePerch_Particles_05-hd.png",
        "img/Interface/bg1.jpg",
        "img/Interface/b.jpg",
        "img/Interface/energy-bar.png",
        "img/Interface/back.png",
        "img/Interface/jn1.png",
        "img/Interface/c.jpg",
        "img/Interface/d.jpg",
        "img/Interface/e.jpg",
        "img/Interface/game_bg_2_hd.jpg",
        "img/Interface/cannon_minus_down.png",
        "img/Interface/cannon_plus.png",
        "img/Interface/login.png",
        "img/Interface/cannon_plus_down.png",
        "img/glod/coinText.png",//黄色的数字
        "img/glod/number_black.png",//白色的数字
        "img/glod/coinAni1.png",//白色的金币
        "img/glod/coinAni2.png",//黄色的金币
        "img/Interface/bottom-bar.png",
        "img/bullet/cannon1.png",
        "img/bullet/cannon2.png",
        "img/bullet/cannon3.png",
        "img/bullet/cannon4.png",
        "img/bullet/cannon5.png",
        "img/bullet/cannon6.png",
        "img/bullet/cannon7.png",
        "img/bullet/bullet1.png",
        "img/bullet/bullet2.png",
        "img/bullet/bullet3.png",
        "img/bullet/bullet4.png",
        "img/bullet/bullet5.png",
        "img/bullet/bullet6.png",
        "img/bullet/bullet7.png",
        "img/bullet/web1s.png",
        "img/bullet/web2s.png",
        "img/bullet/web3s.png",
        "img/bullet/web4s.png",
        "img/bullet/web5.png",
        "img/bullet/web6s.png",
        "img/bullet/web7s.png"
    ],function(){
        centerObj.imgNum.src= "img/glod/coinText.png";
        centerObj.imgNum2.src= "img/glod/number_black.png";
        centerObj.imgGlod.src= "img/glod/coinAni1.png";
        centerObj.imgGlod2.src= "img/glod/coinAni2.png";
        centerObj.imgInfoInterface.back=METHOD.createImg("img/Interface/back.png");

        startUI(centerObj.maxBox.txt);
        centerObj.pt = new HGAME.Object2D({
            img:METHOD.createImg("img/Interface/bottom-bar.png"),
            w:765,
            h:72,
            x:(centerObj.w-765)/2,
            y:(centerObj.h-72),
            lastDraw:true
        });
        var arr  = getAnimateArr("1x5","1");
        centerObj.p=new HGAME.bulletA({
            lastDraw:true,
            imgArr:[
                METHOD.createImg("img/bullet/cannon1.png"),
                METHOD.createImg("img/bullet/cannon2.png"),
                METHOD.createImg("img/bullet/cannon3.png"),
                METHOD.createImg("img/bullet/cannon4.png"),
                METHOD.createImg("img/bullet/cannon5.png"),
                METHOD.createImg("img/bullet/cannon6.png"),
                METHOD.createImg("img/bullet/cannon7.png")
            ],
            bulletImgArr:[
                METHOD.createImg("img/bullet/bullet1.png"),
                METHOD.createImg("img/bullet/bullet2.png"),
                METHOD.createImg("img/bullet/bullet3.png"),
                METHOD.createImg("img/bullet/bullet4.png"),
                METHOD.createImg("img/bullet/bullet5.png"),
                METHOD.createImg("img/bullet/bullet6.png"),
                METHOD.createImg("img/bullet/bullet7.png")
            ],
            gridImgArr:[
                METHOD.createImg("img/bullet/web1s.png"),
                METHOD.createImg("img/bullet/web2s.png"),
                METHOD.createImg("img/bullet/web3s.png"),
                METHOD.createImg("img/bullet/web4s.png"),
                METHOD.createImg("img/bullet/web5.png"),
                METHOD.createImg("img/bullet/web6s.png"),
                METHOD.createImg("img/bullet/web7s.png")
            ],
            changeImgArr:arr,
            pt:centerObj.pt,
            imgInfoTxt:"1x5"

        });

        METHOD.defineEx(centerObj,"num",localStorage.num?localStorage.num:1000,function(){
            localStorage.num=centerObj.num;
        });


        centerObj.addRect={
            w:44,
            h:31,
            y:646,
            x:622,
            downImg:METHOD.createImg(  "img/Interface/cannon_plus_down.png"),
            noDownImg:METHOD.createImg( "img/Interface/cannon_plus.png"),
            img:METHOD.createImg( "img/Interface/cannon_plus.png")
        };
        centerObj.noAddRect={
            w:44,
            h:31,
            y:646,
            x:442,
            noDownImg:METHOD.createImg( "img/Interface/cannon_minus.png"),
            downImg:METHOD.createImg("img/Interface/cannon_minus_down.png"),

            img:METHOD.createImg( "img/Interface/cannon_minus.png")
        };


    });
    centerObj.ele.appendChild(centerObj.canvas);
    centerObj.animate04=new HGAME.animate();
    var cTxt=centerObj.canvas.getContext("2d");
    centerObj.canvas.width=500;
    centerObj.canvas.height=500;
    function clickDomFun(p){
        if(window.screen.width<=700){
            if(typeof document.body.webkitRequestFullscreen!="undefined"){
                document.body.webkitRequestFullscreen();
            }else if(typeof document.body.mozRequestFullscreen!="undefined"){
                document.body.mozRequestFullscreen();
            }else if(typeof document.body.oRequestFullscreen!="undefined"){
                document.body.oRequestFullscreen()
            }else if(typeof document.body.requestFullscreen!="undefined"){
                document.body.requestFullscreen();
            }
        }
        if(centerObj.start=="loading"){
            if(METHOD.inRect(p,centerObj.startRect)){
                selctUI(centerObj.maxBox.txt);
            }
        }else if(centerObj.start=="selecting"){
            for(var i = 0;i< centerObj.cjShowArr.length;i++){
                if(METHOD.inRect(p,centerObj.cjShowArr[i])){
                    if(centerObj.cjShowArr[i].needNum<=centerObj.num){
                        initCj(centerObj.cjShowArr[i].index);
                    }else {
                        selctUI(centerObj.maxBox.txt,"需要的分数不够啊!");
                    }

                    return;
                }
            }
        }


        if(centerObj.start!="begin")return;
        for(var o in     centerObj.rectInfoInterface){
            if(METHOD.inRect(p,centerObj.rectInfoInterface[o])){
                centerObj.rectInfoInterface[o].clickFun.call(centerObj.rectInfoInterface[o]);
                return;
            }
        }
        for( o in     centerObj.jnInfo){
            if(METHOD.inRect(p,centerObj.jnInfo[o])){
                centerObj.jnInfo[o].clickFun.call(centerObj.jnInfo[o]);
                return;
            }
        }
        if(METHOD.inRect(p,centerObj.addRect)){
            centerObj.p.changeImg("add");
            return
        }
        if(METHOD.inRect(p,centerObj.noAddRect)){
            centerObj.p.changeImg("noAdd");
            return
        }

        if(centerObj.bufObj.power.ingInfo>=1){
            centerObj.p.createBullte(centerObj,"1");
            centerObj.bufObj.power.ingInfo=0;
        }else{

            if(centerObj.num-(centerObj.p.nowImg+1)<=0){
                return;
            }
            centerObj.p.createBullte(centerObj);
            centerObj.num-=(centerObj.p.nowImg+1);
            centerObj.bufObj.power.ingInfo=parseFloat(centerObj.bufObj.power.ingInfo)+parseFloat((centerObj.p.nowImg+1)/1200);
            if(centerObj.bufObj.power.ingInfo>1){
                centerObj.bufObj.power.ingInfo=1;
            }
        }
    }
    function moveDomFun(p){
        if(centerObj.start!="begin")return;
     var p2={
            x:centerObj.p.x+centerObj.p.w/2,
            y:centerObj.p.y
        };
        if(!METHOD.inRect(p,{x:142,y:625,w:768,h:100})&&!METHOD.inRect(p,{x:456,y:594,w:210,h:150})){
            var angle= METHOD.pointAngleInfo(p,p2);
            centerObj.p.angle=270+angle;
        }
    }
    function downDomFun(p){
        if(centerObj.start!="begin")return;
        if(METHOD.inRect(p,centerObj.addRect)){

            centerObj.addRect.img= centerObj.addRect.downImg;
        }
        if(METHOD.inRect(p,centerObj.noAddRect)){
            centerObj.noAddRect.img= centerObj.noAddRect.downImg;
        }
    }
    function upDomFun(p){
        if(centerObj.start!="begin")return;
        centerObj.noAddRect.img= centerObj.noAddRect.noDownImg;
        centerObj.addRect.img= centerObj.addRect.noDownImg;
    }
    if(window.screen.width<1000){
        var time = null;
        centerObj.canvas.addEventListener("touchstart",function(e){
            time=new Date()
            var p = {
                x:e.changedTouches[0].clientX-centerObj.canvas.x,
                y: e.changedTouches[0].clientY-centerObj.canvas.y
            };
            if(p.x<0|| e.y<0){
                return
            }
            p.x= p.x*centerObj.w/centerObj.canvas.w;
            p.y= p.y*centerObj.h/centerObj.canvas.h;
            downDomFun(p);
        },true);
        centerObj.canvas.addEventListener("touchend",function(e){

            var p = {
                x: e.changedTouches[0].clientX-centerObj.canvas.x,
                y: e.changedTouches[0].clientY-centerObj.canvas.y
            };
            if(p.x<0|| e.y<0){
                return
            }
            p.x= p.x*centerObj.w/centerObj.canvas.w;
            p.y= p.y*centerObj.h/centerObj.canvas.h;
            upDomFun(p);
            if(new Date-time<130){
                moveDomFun(p)
                clickDomFun(p);
            }
        },true);

    }else{
        centerObj.canvas.addEventListener("click",function(e){
            var p = {
                x: e.offsetX-centerObj.canvas.x,
                y: e.offsetY-centerObj.canvas.y
            };
            if(p.x<0|| e.y<0){
                return
            }
            p.x= p.x*centerObj.w/centerObj.canvas.w;
            p.y= p.y*centerObj.h/centerObj.canvas.h;
            clickDomFun(p);

        },true);
        centerObj.canvas.addEventListener("mousemove",function(e){
            var p = {
                x: e.offsetX-centerObj.canvas.x,
                y: e.offsetY-centerObj.canvas.y
            };
            if(p.x<0|| e.y<0){
                return
            }
            p.x= p.x*centerObj.w/centerObj.canvas.w;
            p.y= p.y*centerObj.h/centerObj.canvas.h;
            moveDomFun(p);
        },true);
        centerObj.canvas.addEventListener("mousedown",function(e){
            var p = {
                x: e.offsetX-centerObj.canvas.x,
                y: e.offsetY-centerObj.canvas.y
            };
            if(p.x<0|| e.y<0){
                return
            }
            p.x= p.x*centerObj.w/centerObj.canvas.w;
            p.y= p.y*centerObj.h/centerObj.canvas.h;
            downDomFun(p);
        },true);
        centerObj.canvas.addEventListener("mouseup",function(e){
            var p = {
                x: e.offsetX-centerObj.canvas.x,
                y: e.offsetY-centerObj.canvas.y
            };
            if(p.x<0|| e.y<0){
                return
            }
            p.x= p.x*centerObj.w/centerObj.canvas.w;
            p.y= p.y*centerObj.h/centerObj.canvas.h;
            upDomFun(p);
        },true);
    }



    centerObj.canvas.w=0;
    centerObj.canvas.h=0;
    centerObj.canvas.x = 0;
    centerObj.canvas.y=0;
    centerObj.animate04.action=function(){
    
        if(document.documentElement.clientWidth<1000){
            centerObj.canvas.width=document.documentElement.clientWidth;
            centerObj.canvas.height=document.documentElement.clientHeight;
        }else{
            centerObj.canvas.width=centerObj.w;
            centerObj.canvas.height=centerObj.h;
        }
        var w=centerObj.canvas.width;
        var h=w/centerObj.w*centerObj.h;
        var x = 0,
            y=(centerObj.canvas.height-h)/2;
        if(h>centerObj.canvas.height){
            h=centerObj.canvas.height;
            w=h/centerObj.h*centerObj.w;
            y=0;
            x=(centerObj.canvas.width-w)/2;
        }
        centerObj.canvas.w=w;
        centerObj.canvas.h=h;
        centerObj.canvas.x = x;
        centerObj.canvas.y=y;
        cTxt.beginPath();
        cTxt.clearRect(0,0,centerObj.canvas.width,centerObj.canvas.height);
        cTxt.fillStyle="#000000";
        cTxt.fillRect(0,0,centerObj.canvas.width,centerObj.canvas.height);
        if(window.screen.width<1000){
            if(window.orientation==90||window.orientation==-90){

            }else{
                var txt=centerObj.canvas.getContext("2d");
                txt.fillStyle="#ffffff"
                txt.textBaseline="middle";
                txt.textAlign="center";
                txt.font="normal normal 24px/28px arial"
                txt.fillText("请让浏览器处于横屏模式",centerObj.canvas.width/2,centerObj.canvas.height/2);
                return;
            }
        }
       
        cTxt.drawImage(centerObj.maxBox.dom,0,0,centerObj.w,centerObj.h,x,y,w,h);
        cTxt.closePath();
    };
    centerObj.animate04.run();
})();