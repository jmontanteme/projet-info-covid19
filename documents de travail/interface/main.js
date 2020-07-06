window.addEventListener("DOMContentLoaded", (event) => {
    var socket = io.connect("http://" + document.domain + ":" + location.port );

    // words correpond aux mots tapés dans la barre de recherche, c'est une chaine de caractères
    let words;

    document.onkeydown = function(e){


        //une version bête de la barre de recherche, ou plutot de 
        // ce qui prend ce qui est dans la barre de recherche 
        
        /* la touche "entrée" est pressée */
        if (e.keyCode == 13) {            
            socket.emit("move",words );
            words = '';
        }

        /* la touche "backspace" (flèche arrière) est pressée */
        else if(e.keyCode == 8) {
            words = words.slice(0, -1);
            
        }

        else{
            words=words+e.key;
            console.log(words);
        }

    };
    
    var btn_n = document.getElementById("go_n");
    btn_n.onclick = function(e) {
        console.log("Clicked on button north");
        socket.emit("search", {dx:0, dy:-1});
    };

    var btn_s = document.getElementById("go_s");
    btn_s.onclick = function(e) {
        console.log("Clicked on button south");
        socket.emit("move", {dx:0, dy:1});
    };

    var btn_w = document.getElementById("go_w");
    btn_w.onclick = function(e) {
        console.log("Clicked on button w");
        socket.emit("move", {dx:-1, dy:0});
    };

    var btn_e = document.getElementById("go_e");
    btn_e.onclick = function(e) {
        console.log("Clicked on button e");
        socket.emit("move", {dx:1, dy:0});
    };


    socket.on("response", function(data){
        console.log(data);
        for( var i=0; i<2; i++){
            var cell_id = "cell " + data[i].i + "-" + data[i].j;
            var span_to_modif = document.getElementById(cell_id);
            span_to_modif.textContent = data[i].content;
        }
    });

});