var fps_arr=[];
var insertIntoFpsArr = false;

function extractFps(fps) {
  if (insertIntoFpsArr) fps_arr.push(fps);  
};

function MyAnimation() {    
    window.requestAnimFrame = (function(){return  window.requestAnimationFrame||window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame })();

    var useHighAnimation = false;
    var lastTime = performance.now();
    var frame = 0;
    var container, fpsDiv, fpsText, fpsGraph, msDiv, msText, msGraph;

    var animation = function(){        
        container = document.createElement( 'div' );
        container.id = 'stats';
        container.style.cssText = 'width:80px;opacity:0.9;cursor:pointer';

        fpsDiv = document.createElement( 'div' );
        fpsDiv.id = 'fps';
        fpsDiv.style.cssText = 'padding:0 0 3px 3px;text-align:left;background-color:#002';
        container.appendChild( fpsDiv );

        fpsText = document.createElement( 'div' );
        fpsText.id = 'fpsText';
        fpsText.style.cssText = 'color:#0ff;font-family:Helvetica,Arial,sans-serif;font-size:9px;font-weight:bold;line-height:15px';
        fpsText.innerHTML = 'FPS';
        fpsDiv.appendChild( fpsText );

        fpsGraph = document.createElement( 'div' );
        fpsGraph.id = 'fpsGraph';
        fpsGraph.style.cssText = 'position:relative;width:74px;height:30px;';
        fpsDiv.appendChild( fpsGraph );
        if (useHighAnimation) {
            fpsFastGraph = document.createElement( 'div' );
            fpsFastGraph.id = 'fpsFastGraph';
            fpsFastGraph.style.cssText = 'position:relative;width:74px;height:30px; margin-top:5px';
            fpsDiv.appendChild( fpsFastGraph );
        }
        var initGraph = function (dom){
	        while ( dom.children.length < 74 ) {

		        var bar = document.createElement( 'span' );
		        bar.style.cssText = 'width:1px;height:30px;float:left;background-color:#000';
		        dom.appendChild( bar );
	        }
        };
        initGraph(fpsGraph);

        if (useHighAnimation) initGraph(fpsFastGraph);

        fpsDiv.style.display = 'block';
        container.style.position = 'absolute';
        container.style.left = '0px';
        container.style.top = '0px';
        container.id = "fpsContainer";

        container.style.position='fixed';
        container.style.zIndex='10000';


        document.body.appendChild( container );
        
    };  
      
    animation();   
      
    var updateGraph = function ( dom, value ) {
        if (!useHighAnimation) return;   
        if (value > 30)
            value = 30;     
        var child = dom.appendChild( dom.firstChild );
        child.style.height = (value) + 'px';
        child.style.marginTop = (30-value)+'px';
        child.style.backgroundColor = "#1eff1e";         
    };
    var updateGraphRed = function ( dom, value ) {
       
        if (value > 30)
            value = 30;     
        var child = dom.appendChild( dom.firstChild );
        child.style.height = (value) + 'px';
        child.style.marginTop = (30-value)+'px';
        child.style.backgroundColor = "#ff0000";           
    };

    var lastFameTime = performance.now();
    var fsMin = Infinity;
    var fsMax = 0;
    setTimeout(function(){loop(0)},1000);

    var loop = function(time) {
        var now =  performance.now();
        var fs = (now - lastFameTime);
        lastFameTime = now;
        var fps = Math.round(1000/fs);
        frame++;
        if (now > 1000 + lastTime){
            var fps = Math.round( ( frame * 1000 ) / ( now - lastTime ) );
            fsMin = Math.min( fsMin, fps );
            fsMax = Math.max( fsMax, fps );
            extractFps(fps);

            fpsText.textContent = fps + ' FPS (' + fsMin + '-' + fsMax + ')'; 
            updateGraphRed( fpsGraph, Math.round(( fps / 60 ) * 30 ));          
            frame = 0;    
            lastTime = now;
            
        };
        if (useHighAnimation)
            updateGraph( fpsFastGraph,  Math.round(( fps / 60 ) * 30 )  );              
        window.requestAnimFrame(loop);   
    }

      
};
MyAnimation();


