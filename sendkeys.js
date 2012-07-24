// send keys to websocket and echo the response
$(document).ready(function() {
    // create websocket
    if (! ("WebSocket" in window)) WebSocket = MozWebSocket; // firefox
    var socket = new WebSocket("ws://localhost:8076");

    // open the socket
    socket.onopen = function(event) {
        socket.send('connected');

        // show server response
        socket.onmessage = function(e) {
            //x = e.data.split(',')[0];
            //y = e.data.split(',')[1];
            //$("#output").text(move_cursor(x,y));
           $("#output").text(e.data) 
        }
        var init_x = null;
        var init_y = null;
        var init_curs_x = null;
        var init_curs_y = null;
        var obj = document.getElementById('test');
        document.addEventListener('touchmove', function(event) {
            alert('Touched')
        // If there's exactly one finger inside this element
        if (event.targetTouches.length == 1) {
            var touch = event.targetTouches[0];
            // Place element where the finger is
            //obj.style.left = touch.pageX + 'px';
            //obj.style.top = touch.pageY + 'px';
                var x = touch.pageX - this.offsetLeft;
                var y = touch.pageY - this.offsetTop;
                if (!init_x || !init_y){
                    init_x = x;
                    init_y = y;
                };
                offset_x = x - init_x ;
                offset_y = y - init_y;
                socket.send('move:'+ offset_x +','+ offset_y);

        }
        }, false); 

        $("#test").mousedown(function(e){
            //socket.send('start_record');
            //alert('recording')
            $("#test").mousemove(function(e){
                var x = e.pageX - this.offsetLeft;
                var y = e.pageY - this.offsetTop;
                if (!init_x || !init_y){
                    init_x = x;
                    init_y = y;
                };
                offset_x = x - init_x ;
                offset_y = y - init_y;
                socket.send('move:'+ offset_x +','+ offset_y);
            });
        });

        $(window).mouseup(function(e){
            $("#test").unbind('mousemove');
            init_x = null;
            init_y = null;
            init_curs_x = null;
            init_curs_y = null;
            //socket.send('stop_record')
        });

        function move_cursor(x,y){
            if(!init_curs_x){
                off = $("#cursor").offset();
                init_curs_x = off.left;
                init_curs_y = off.top;
            }
            new_x = parseInt(init_curs_x) + parseInt(x);
            new_y = parseInt(init_curs_y) + parseInt(y);
            $('#cursor').offset({top: new_y, left: new_x});
            return new_x +','+new_y;
        }
        // for each typed key send #entry's text to server
        $("#entry").keyup(function (e) {
        socket.send($("#entry").attr("value"));
        });
    }
});
