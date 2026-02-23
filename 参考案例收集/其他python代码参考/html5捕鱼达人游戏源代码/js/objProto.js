/*随机创建鱼类型*/
HGAME.fishStruct=function(Obj){
    this._struct="fishStruct";
    var defaultObj = {
        createFishArray:[],//创建的鱼
        method:[],
        method02:[],
        maxNum:10,//创建鱼的最大数量
        defaultAngle:-1,//默认的面向角度
        fishType:"",
        fishInfo:{},
        imgUrl:"",
        createTimeBufBuf:0,
        fishXInfo:[-50,0],
        fishYInfo:[-50,0],
        minAngleInfo:[10,30],
        maxAngleInfo:[80,100],
        w:0,
        h:0,
        createAllTime:"none",
        createAllTimeBuf:"none",
        moveSpeed:5,
        PH:1,
        addNum:1,
        deathNum:0.4,
        createTime:-10,
        createTimeBuf:2000,
        swimArr:[],//游动动画数组
        deathArray:[],//死亡动画数组
        createFishEnd:function(fish){}
    };
    extend(defaultObj,Obj);


    this.createFish=function(centerObj){
        if(this.createAllTime!="none"&&typeof this.createAllTime=="number"){
            if(this.createAllTime<=0){
                this.createAllTime=0;
                return;
            }else{
                this.createAllTime-=centerObj.animate.time;
            }
        }
        if(this.createFishArray.length>this.maxNum)return;
        if(this.createTime<0){this.createTime=this.createTimeBuf}else{this.createTime-=centerObj.animate.time;return;}
        var img = METHOD.createImg(this.imgUrl);
        var minAng=typeof this.minAngleInfo == "string"||typeof this.minAngleInfo == "number"?this.minAngleInfo:Math.random()*(this.minAngleInfo[1]-this.minAngleInfo[0])+this.minAngleInfo[0];
        var maxAng=typeof this.maxAngleInfo == "string"||typeof this.maxAngleInfo == "number"?this.maxAngleInfo:Math.random()*(this.maxAngleInfo[1]-this.maxAngleInfo[0])+this.maxAngleInfo[0];
        var xInfo=typeof this.fishXInfo == "string"||typeof this.fishXInfo == "number"?this.fishXInfo:Math.random()*(this.fishXInfo[1]-this.fishXInfo[0])+this.fishXInfo[0];
        var yInfo=typeof this.fishYInfo == "string"||typeof this.fishYInfo == "number"?this.fishYInfo:Math.random()*(this.fishYInfo[1]-this.fishYInfo[0])+this.fishYInfo[0];
        var PH =typeof this.PH == "string"||typeof this.PH == "number"?this.PH:parseInt(Math.random()*(this.PH[1]-this.PH[0])+this.PH[0]);
        this.fishInfo={
            x:xInfo,
            y:yInfo,
            minAngle:minAng,
            maxAngle:maxAng,
            img:img,
            moveSpeed:this.moveSpeed,
            deathNum:this.deathNum,
            w:this.w,
            h:this.h,
            PH:PH,
            fishType:this.fishType,
            addNum:this.addNum,
            method:this.method,
            method02:this.method02,
            belong:this,
            angle:this.defaultAngle==-1?minAng:this.defaultAngle,
            swimArr:this.swimArr,//游动动画数组
            deathArray:this.deathArray//死亡动画数组
        };
        var fish = new HGAME.fish(this.fishInfo);
        this.createFishArray.push(fish);
        centerObj.maxBox.add(fish);
        centerObj.fishArr.push(fish);
        this.createFishEnd.call(this,fish);
    };

    extend(this,defaultObj);


};
/*鱼类型*/
HGAME.fish = function(Obj){
    HGAME.Object2D.call(this,Obj);
    this._struct="fish";
    var defaultObj = {
        swimArr:[],//游动动画数组
        deathArray:[],//死亡动画数组
        deathTime:1000,//死亡时间
        death:false,//是否死亡
        belong:null,

        moveSpeed:5,//移动速度
        maxAngle:90,//当角度大于这个值的时候减少
        minAngle:20,//当角度小于这个值的时候增加
        addAngleType:1, //1增加角度 0减少角度
        addAngleVal:2,//角度改变的值
        deathNum:0.01,
        isChangeAngle:true,//是否改变角度
        isAdd:false,//是否一直增加角度
        isNoAdd:false//是否一直减小角度
    };
    extend(defaultObj,Obj);
    this.nowImgInfo = 0;
    this.changeAngeleForMoveA=function(){
        if(this.x+this.w>700){
            this.isChangeAngle=true;
            this.addAngleVal=0.5;
        }
    };
    this.changeAngeleForMoveB=function(){
        if(this.death==true){
            return;
        }
        if(this.y+this.h>600){
           this.angle-=0.5;
        }
    };
    this.changeAngeleForMoveC=function(){
        if(this.death==true){
            return;
        }
        if(typeof this.changeAngeleForMoveCAng=="undefined"){
            this.bufAng=0;
            this.changeAngeleForMoveCAng=false;
        }
        if(!this.changeAngeleForMoveCAng){
            this.bufAng+=0.25;
        }else{
            this.bufAng-=0.25;
        }
        if(this.bufAng>100){
            this.changeAngeleForMoveCAng=true;
        }else if(this.bufAng<-100){
            this.changeAngeleForMoveCAng=false;
        }
        this.angle=this.bufAng;
    };
    this.changeImgInfo=function(){
          if(this.death==false){
                if(!this.swimArr[this.nowImgInfo]){console.log(this.img.src);return;}
                this.H_INT=this.swimArr[this.nowImgInfo].h;
                this.W_INT=this.swimArr[this.nowImgInfo].w;
                if(this.nowImgInfo>=this.swimArr.length-1){
                    this.nowImgInfo=0;
                }else{
                    this.nowImgInfo++;
                }
          }else if(this.death==true){
              if(!this.deathArray[this.nowImgInfo]){console.log(this.img.src);return;}
              this.H_INT=this.deathArray[this.nowImgInfo].h;
              this.W_INT=this.deathArray[this.nowImgInfo].w;
              if(this.nowImgInfo>=this.deathArray.length-1){
                  this.nowImgInfo=0;
              }else{
                  this.nowImgInfo++;
              }
          }
    };
    this.createGold=function(centerObj){

        if(Math.random()>0.999){
            var gold22 = new HGAME.gold({
                targetRect:centerObj.goldInfo.targetRect,
                addNum:1,
                changeAttr:"wpNum",
                img:  centerObj.jnInfo.wpObj.img,
                imgAmtInfo:[{w:0,h:0}],
                w:106,
                h:106,
                x:this.x,
                y:this.y,
                scale:0.56603,
                fx:Math.random()
            });
            centerObj.goldArr.push(gold22);
            centerObj.maxBox.add(gold22);
            return;
        }
        var addNum = parseInt(this.addNum/10);
        var addNum2 = this.addNum%10;

        var y = 0;
        for(var i = 0;i<addNum;i++){
            var gold1 = new HGAME.gold({
                targetRect:centerObj.goldInfo.targetRect,
                addNum:10,
                img:centerObj.imgGlod2,
                imgAmtInfo: centerObj.goldInfo.imgInfoArr,
                w:centerObj.goldInfo.w,
                h:centerObj.goldInfo.h,
                x:this.x+centerObj.goldInfo.w*i,
                y:this.y+y,
                fx:Math.random(),
            });
            centerObj.goldArr.push(gold1);
            centerObj.maxBox.add(gold1);
        }
        y=y+centerObj.goldInfo.h+20;
        for( i = 0;i<addNum2;i++){
            var gold2 = new HGAME.gold({
                targetRect:centerObj.goldInfo.targetRect,
                addNum:1,
                fx:Math.random(),
                img:centerObj.imgGlod,
                imgAmtInfo: centerObj.goldInfo.imgInfoArr,
                w:centerObj.goldInfo.w,
                h:centerObj.goldInfo.h,
                x:this.x+centerObj.goldInfo.w*i,
                y:this.y+y
            });
            centerObj.goldArr.push(gold2);
            centerObj.maxBox.add(gold2);
        }

    };
    this.deathAfter= function(centerObj){
        if(this.death==true){
            if(this.deathTime<=0){
                centerObj.maxBox.remove(this);

                this.belong.createFishArray.splice( this.belong.createFishArray.indexOf(this),1);
                centerObj.fishArr.splice( centerObj.fishArr.indexOf(this),1);

            }else{
                this.deathTime-=centerObj.animate.time;
            }
        }
    };
    this.isScreenOut=function(centerObj){
        var rect = {
            x:-this.w-100,
            y:-this.w-100,
            w:centerObj.maxBox.w-(-this.w-100)*2,
            h:centerObj.maxBox.h-(-this.h-100)*2
        };
        if(!METHOD.inRect({
            x:this.x,
            y:this.y
        },rect)){
            centerObj.maxBox.remove(this);
            this.belong.createFishArray.splice( this.belong.createFishArray.indexOf(this),1);
            centerObj.fishArr.splice( centerObj.fishArr.indexOf(this),1);
        }
    };
    /*改变角度相关*/
    this.changeAngle=function(){
        if(this.death)return;
        if(!this.isChangeAngle)return;
        if(this.isAdd){this.angle+=this.addAngleVal;return}
        if(this.isNoAdd){this.angle-=this.addAngleVal;return}
        if(this.addAngleType==1){
            this.angle+=this.addAngleVal;
        }else if(this.addAngleType==0){
            this.angle-=this.addAngleVal;
        }
        if(this.angle>=this.maxAngle){
            this.addAngleType=0;
        }else if(this.angle<=this.minAngle){
            this.addAngleType=1;
        }
    };
    /*向前移动*/
    this.moveForward=function(){
        if(this.death)return;
        var   p= METHOD.polarCoordinates({x:this.x,y:this.y},this.angle,this.moveSpeed);
        this.x= p.x;
        this.y= p.y;
    };
    extend(this,defaultObj);
};
/*炮架类型*/
HGAME.bulletA=function(Obj){
    HGAME.Object2D.call(this,Obj);
    this._struct="bulletA";
    var defaultObj = {
        imgArr:[],
        nowImg:0,
        bulletImgArr:[],
        changeImgArr:[],
        gridImgArr:[],
        imgInfoTxt:""
    };
    extend(defaultObj,Obj);
    this.nowImg=0;
    this.changeImg=function(type){
        if(type=="add"){
            if(this.nowImg<this.imgArr.length-1){
                this.nowImg++;
            }else {
                this.nowImg=0;
            }

        }else if(type=="noAdd"){
            if(this.nowImg>0){
                this.nowImg--;
            }else {
                this.nowImg=this.imgArr.length-1;
            }
        }
        if(typeof this.imgArr[this.nowImg]!="undefined"){
            this.img= this.imgArr[this.nowImg];
        }
    };
    this.imgInfo=0;
    this.changeImgInfo=function(){
        this.H_INT=this.changeImgArr[this.imgInfo].h;
        this.W_INT=this.changeImgArr[this.imgInfo].w;
        if(this.imgInfo>=this.changeImgArr.length-1){
            this.imgInfo=0;
        }else{
            this.imgInfo++;
        }
        this.w=this.img.width/this.imgInfoTxt.split("x")[0];
        this.h=this.img.height/this.imgInfoTxt.split("x")[1];
        this.x=this.pt.x+this.pt.w/2-this.w/2+42;
        this.y=this.pt.y-5-2*this.nowImg;
        this.rotatePointX=this.w/2;
        this.rotatePointY=this.h;
    };
    this.createBullte=function(centerObj,t){
        t=t||"";
        var point={
            x:this.x+this.rotatePointX-this.bulletImgArr[this.nowImg].width/2,
            y:this.y+this.rotatePointY-this.bulletImgArr[this.nowImg].height/2
        };
        if(t=="1"){
            point={
                x:this.x+this.rotatePointX-centerObj.bufObj.power.noDeathArr[0].width/2,
                y:this.y+this.rotatePointY-centerObj.bufObj.power.noDeathArr[0].height/2,
            }
        }
        var p2=METHOD.polarCoordinates(point,this.angle+270,this.h);
        var bullteB=null;
        if(t=="1"){
            bullteB=new HGAME.bulletB({
                noDeathImg:centerObj.bufObj.power.noDeathArr,
                deathImg:centerObj.bufObj.power.deathArr,
                belong:this,
                angle:this.angle,
                x:p2.x,
                y:p2.y,
                type:1,
                hurtInfo:20
            })
        }else{
            bullteB=new HGAME.bulletB({
            noDeathImg:this.bulletImgArr[this.nowImg],
            deathImg:this.gridImgArr[this.nowImg],
            belong:this,
            angle:this.angle,
            x:p2.x,
            y:p2.y,
            hurtInfo:this.nowImg
        });

        }

        centerObj.bulletArr.push(bullteB);
        centerObj.maxBox.add(bullteB);
    };
    if(this.imgArr.length>0){
        if(typeof this.imgArr[this.nowImg]!="undefined"){
            this.img= this.imgArr[this.nowImg];
        }else{
            this.img= this.imgArr[0];
        }
        this.w=this.img.width/this.imgInfoTxt.split("x")[0];
        this.h=this.img.height/this.imgInfoTxt.split("x")[1];
        this.x=this.pt.x+this.pt.w/2-this.w/2+42;
        this.y=this.pt.y-5-2*this.nowImg;
        this.rotatePointX=this.w/2;
        this.rotatePointY=this.h;
    }
    extend(this,defaultObj);
};
/*炮弹类型*/
HGAME.bulletB=function(Obj){
    HGAME.Object2D.call(this,Obj);
    this._struct='bulletB';
    var defaultObj = {
        noDeathImg:null,
        deathImg:null,
        deathType:0,//0子弹状态 1网状态
        deathTime:1200,
        belong:null,
        hurtTime:-10,
        hurtVal:1,
        hurtTimeBuf:500,
        moveSpeed:8,
        hurtInfo:0,type:0
    };
    extend(defaultObj,Obj);
    /*向前移动*/
    this.moveForward=function(){
        //debugger;
        if(this.deathType!=0)return;
        //debugger;
        var   p= METHOD.polarCoordinates({x:this.x,y:this.y},this.angle+270,this.moveSpeed);
        this.x= p.x;
        this.y= p.y;
    };
    this.nowImg=0;
    this.changeImageInfo=function(){
        if(this.noDeathImg.length&&this.deathImg.length){
            if(this.nowImg+1<=this.nowImgArr.length-1){
                this.nowImg=this.nowImg+1
            }else{
                this.nowImg=0;
            }
            this.img=this.nowImgArr[this.nowImg];
        }

    };
    this.colObj=new HGAME.collision();
    this.colFish=function(centerObj){
        var i =0;
        var bool = false;
        for(;i<centerObj.fishArr.length;i++){
            if(this.colObj.rotateTest(this,centerObj.fishArr[i])&&centerObj.fishArr[i].death!=true){
                bool=true;
                if(this.deathType==0){
                    if(this.type==0){
                        this.changeDeathType(1);
                    }
                }
                if(this.type==1&&!centerObj.fishArr[i].createPower){
                    centerObj.fishArr[i].createPower=true;
                    var bullteB=new HGAME.bulletB({
                        noDeathImg:this.noDeathImg,
                        deathImg:this.deathImg,
                        belong:centerObj.p,
                        angle:this.angle,
                        x:centerObj.fishArr[i].x-this.deathImg[0].width/2,
                        y:centerObj.fishArr[i].y-this.deathImg[0].height/2,
                        hurtInfo:this.hurtInfo,
                        deathTime:25000,
                        hurtTimeBuf:100,
                        type:2
                    });
                    bullteB.changeDeathType(1);
                    centerObj.bulletArr.push(bullteB);
                    centerObj.maxBox.add(bullteB);
                }
                if(this.hurtTime<=0){
                    var num  = Math.random()-0.05*this.hurtInfo;

                    if(num<centerObj.fishArr[i].deathNum){
                        if(centerObj.fishArr[i].PH-1<=0){

                            centerObj.fishArr[i].PH=0;
                            centerObj.fishArr[i].death=true;
                            centerObj.fishArr[i].nowImgInfo=0;
                            centerObj.fishArr[i].createGold(centerObj);

                        }else{
                            centerObj.fishArr[i].PH-=this.hurtVal;
                        }

                    }
                }
            }
        }
        if(bool){
            this.hurtTime=this.hurtTimeBuf;
        }
    };
    /**/
    this.nowImgArr=this.noDeathImg;
    this.changeDeathType=function(num,info){
        var w = this.w;
        var h = this.h;
        this.deathType=num;
        if(this.deathType==0){
            if(this.noDeathImg.length){
                this.nowImg=0;
                this.img=this.noDeathImg[0];
                this.nowImgArr=this.noDeathImg;
            }else{
                this.img = this.noDeathImg;
            }


        }else if(this.deathType==1){
            if(this.deathImg.length){
                this.nowImg=0;
                this.img=this.deathImg[0];
                this.nowImgArr=this.deathImg;
            }else{
                this.img = this.deathImg;
            }
        }
        this.w=this.img.width;
        this.h=this.img.height;
        if(num==1){
            this.angle=0;
            this.x = this.x-this.w/2+w/2;
            this.y = this.y-this.h/2+h/2
        }
    };
    this.isScreenOut=function(centerObj){
        var rect = {
            x:-this.w-30,
            y:-this.w-30,
            w:centerObj.maxBox.w-(-this.w-30)*2,
            h:centerObj.maxBox.h-(-this.h-30)*2
        };
        if(!METHOD.inRect({
                x:this.x,
                y:this.y
            },rect)){
            this.changeDeathType(1);
        }
    };
    this.deathChangeAfter=function(centerObj){
        if(this.deathType==1){
            if(this.hurtTime>0){
                this.hurtTime-=centerObj.animate.time;
            }
            if(this.deathTime<=0){
                centerObj.maxBox.remove(this);
                centerObj.bulletArr.splice( centerObj.bulletArr.indexOf(this),1);
            }else{
                this.deathTime-=centerObj.animate.time;
            }
        }
    };
    this.changeDeathType(0);
    extend(this,defaultObj);
};
/*金币类型*/
HGAME.gold=function(Obj){
    HGAME.Object2D.call(this,Obj);
    this._struct='gold';
    var defaultObj = {
        targetRect:null,
        addNum:1,
        img:null,
        imgAmtInfo:[],
        fx:0.3,
        lastDraw:true,
        addt:0.01,
        changeAttr:'num'
    };
    this.imgInfo=0;
    this.changeImgInfo=function(){
        this.H_INT=this.imgAmtInfo[this.imgInfo].h;
        this.W_INT=this.imgAmtInfo[this.imgInfo].w;
        if(this.imgInfo>=this.imgAmtInfo.length-1){
            this.imgInfo=0;
        }else{
            this.imgInfo++;
        }
    };
    this.changeXYInfo=function(centerObj){
        var x=METHOD.bezierCurve({
            t:this.t,
            P0:this.bufX,
            P1:this.cPoint.x,
            P2:this.targetRect.x
        });
        var y =METHOD.bezierCurve({
            t:this.t,
            P0:this.bufY,
            P1:this.cPoint.y,
            P2:this.targetRect.y
        });
        this.x=x;
        this.y=y;
        if(this.scale>=0.5){
            this.scale-=0.005;
        }
        if(this.t<=1){
            this.t+=this.addt;
        }else{

            centerObj.goldArr.splice(centerObj.goldArr.indexOf(this),1);
            centerObj.maxBox.remove(this);
            centerObj[this.changeAttr]=parseInt(centerObj[this.changeAttr])+parseInt(this.addNum);
        }
    };
    extend(defaultObj,Obj);
    extend(this,defaultObj);
    this.cPoint = {x:0,y:0};
    var addInfo=90;
    if(this.fx>=0.5){
        addInfo=90
    }else {
        addInfo=-90
    }
    var ang=METHOD.pointAngleInfo(this.targetRect,this);
    var ang02=(ang+addInfo)%360;
    if(ang02<0){
        ang02=ang02+360;
    }
    this.cPoint=METHOD.polarCoordinates({
        x:(Math.max(this.targetRect.x,this.x)-Math.min(this.targetRect.x,this.x))/2+Math.min(this.targetRect.x,this.x),
        y:(Math.max(this.targetRect.y,this.y)-Math.min(this.targetRect.y,this.y))/2+Math.min(this.targetRect.y,this.y)
    },ang02,100);
    var jl=(this.targetRect.x-this.x)*(this.targetRect.x-this.x)+(this.targetRect.y-this.y)*(this.targetRect.y-this.y);
    jl=Math.sqrt(jl);
    this.bufX=this.x;
    this.bufY=this.y;
    this.t=0;
    this.addt=1/(jl/20);
};
/*对话框类*/
HGAME.model=function(Obj){
    HGAME.canvas.call(this);
    extend(this,Obj);
    var THIS = this;
    this.title=new HGAME.canvas();
    this.content=new HGAME.canvas();
    this.btn=new HGAME.canvas();
    this.btn2=new HGAME.canvas();
    this.buffer="normal normal {size}/{line} arial";
    this.initContent=function(Obj){
        Obj=Obj||{};
        var defaultObj={
            txt:["test title"],//title显示文字
            fontSize:"16",//title的字体大小
            lineHeight:"20",//title的行高
            color:"#999999",//title的文字颜色
            bgColor:"#ffffff",//title 背景颜色
            verticalAlign:"middle",
            textAlign:"center" //center 剧中 left剧左 right 剧右
        };
        var txt = this.content.txt;
        var h =Obj.h?Obj.h:150;
        var w = Obj.w?Obj.w:this.w;
        extend(defaultObj,Obj);
        this.content.w=w;
        this.content.h=h;
        txt.clearRect(0,0,w,h);
        txt.beginPath();
        /*绘制背景*/
        txt.fillStyle=defaultObj.bgColor;
        txt.fillRect(0,0,w,h);
        /*绘制文字*/
        var startY = (h - defaultObj.txt.length*defaultObj.lineHeight)/2;
        for(var i = 0;i<defaultObj.txt.length;i++){
            var text = defaultObj.txt[i];
            txt.fillStyle=defaultObj.color;
            txt.font=this.buffer.replace("{size}",defaultObj.fontSize+"px").replace("{line}",defaultObj.lineHeight+"px");
            txt.textBaseline="top";
            var x=0;
            var y = defaultObj.lineHeight*i +startY;
            if(defaultObj.textAlign=="left"){
                txt.textAlign="left";
                x=0;
            }else if(defaultObj.textAlign=="center"){
                txt.textAlign="center";
                x=w/2;
            }else if(defaultObj.textAlign=="right"){
                txt.textAlign="right";
                x=w;
            }
            txt.fillText(text,x,y);
        }
        txt.closePath();
    };
    this.initComment=function(Obj,cvsObj){
        Obj=Obj||{};
        var defaultObj = {
            txt:"test title",//title显示文字
            fontSize:"16",//title的字体大小
            lineHeight:"20",//title的行高
            color:"#cccccc",//title的文字颜色
            bgColor:"#ffffff",//title 背景颜色
            textAlign:"center" //center 剧中 left剧左 right 剧右
        };
        /*txt文字 font*/
        var txt = cvsObj.txt;
        var h =Obj.h?Obj.h:45;
        var w = Obj.w?Obj.w:this.w;
        extend(defaultObj,Obj);
        cvsObj.w=w;
        cvsObj.h=h;
        txt.clearRect(0,0,w,h);
        txt.beginPath();
        /*绘制背景*/
        txt.fillStyle=defaultObj.bgColor;
        txt.fillRect(0,0,w,h);
        /*绘制文字*/
        txt.fillStyle=defaultObj.color;
        txt.font=this.buffer.replace("{size}",defaultObj.fontSize+"px").replace("{line}",defaultObj.lineHeight+"px");
        txt.textBaseline="middle";
        var x=0;
        var y = h/2;
        if(defaultObj.textAlign=="left"){
            txt.textAlign="left";
            x=0;
        }else if(defaultObj.textAlign=="center"){
            txt.textAlign="center";
            x=w/2;
        }else if(defaultObj.textAlign=="right"){
            txt.textAlign="right";
            x=w;
        }
        txt.fillText(defaultObj.txt,x,y);
        txt.closePath();
    };

    this.showView=false;
    this.show = function(maxBox,info){

        info=info||{w:400,addY:10};
        this.close();
        this.w = info.w;

        this.initComment(info.title,this.title);
        this.initContent(info.content);
        this.initComment(info.btn2,this.btn2);
        this.initComment(info.btn,this.btn);
        if(maxBox){
            this.x=(maxBox.w-info.w)/2;
            this.y=-this.h;

        }
        var  h = 0;
        h = this.title.h+this.content.h+this.btn.h;
        this.h=h;
        this.title.x=0;
        this.title.y=0;
        this.add(this.title);
        this.content.x=0;
        this.content.y = this.title.h;
        this.add(this.content);
        this.btn.x=0;
        this.btn.y=this.content.h+this.title.h;
        this.add(this.btn);
        if(info.btn2){
            this.btn2.x=this.btn.w;
            this.btn2.y=this.btn.y;
            this.add(this.btn2);
        }
        if(maxBox){
            this.box = maxBox;
            maxBox.add(this);
            this.showView=true;
            this.animate.stop();
            this.animate.action=function(){
                if(THIS.y<maxBox.h/2-THIS.h/2){
                    THIS.y+=info.addY;
                }else{
                    THIS.y=maxBox.h/2-THIS.h/2;
                    this.stop();
                    THIS.showEnd&&THIS.showEnd.call(THIS,THIS);
                }
            }
            this.animate.run();
        }

    }
    this.animate=new HGAME.animate();
    this.close=function(){
        if(this.box){

            this.box.remove(this);
            this.showView=false;
        }
    }

}