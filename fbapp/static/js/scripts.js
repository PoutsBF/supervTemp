$(function() {
    $('#table').bootstrapTable()
});

var socket = new WebSocket('ws://' + document.domain + ':' + location.port + '/ws');

socket.onopen = function (e) 
{ 
    console.log("WebSocket : connecté ");
    socket.send('{\"Connect\":\"' + new Date() + '\"}'); 
};
socket.onclose = function(e) { alert("closed"); }
socket.onerror = function (error) { console.log('WebSocket Error ', error); };

socket.onmessage = function (event) 
{
    console.log("réception message websocket");
    try
    {
        var msg = JSON.parse(event.data);
    }
    catch (e)
    {
        console.error("Parsing error:", e);
        console.log(event.data);
    }
    var text = "";
    if (typeof msg.message != 'undefined')
    {
        switch(msg.message)
        {
            case "majDataInst" : majDataInst(msg.data); break;            
        }
    }
};

function majDataInst(data) 
{
    console.log("Mise à jour des données");
    for (let item in data)
    {
        $('#dv-' + item + ' [name="timeS"]').text(data[item][1]);
        $('#dv-' + item + ' [name="temp"]').text(data[item][3]);
        $('#dv-' + item + ' [name="hygro"]').text(data[item][4]);
        $('#dv-' + item + ' [name="bat"]').attr("title", "batterie : " +  data[item][5].toString() + " %");
        $('#dv-' + item + ' [name="bat"]').attr("alt", "batterie : " + data[item][5].toString() + " %");   
    }
};

function json_button() {
    socket.send('json_button', '{"message": "test"}');
}

function alert_button() {
    socket.send('alert_button', 'Message from client!!')
}

position_thermometres = [
    {pos_x :  420, pos_y : 700},   // 1 : chambre Maxine
    {pos_x :  870, pos_y : 870},   // 2 : véranda
    {pos_x : 1100, pos_y : 230},   // 3 : garage
    {pos_x :   30, pos_y : 740},   // 4 : Martin
    {pos_x :   50, pos_y : 300},   // 5 : Salle de bain
    {pos_x :   50, pos_y : 170},   // 6 : chambre parents
    {pos_x : 1150, pos_y : 440},   // 7 : salle à manger
    {pos_x :  570, pos_y : 530}    // 8 : mobile
    ];

style_rect = "fill:none;fill-opacity:0;stroke:#000069;stroke-width:1.545;stroke-linejoin:round;stroke-miterlimit:4.9;stroke-dasharray:none;";

var_svg = document.getElementById("svgMaison");

/* <g id="svg_15">
<rect fill="none" fill-opacity="0" height="47" id="svg_8" stroke="#000069" stroke-linejoin="round" stroke-miterlimit="4.9" stroke-width="1.545" width="50" x="766" y="177"/>
<rect fill="none" fill-opacity="0" height="15" id="svg_9" stroke="#000069" stroke-linejoin="round" stroke-miterlimit="4.9" stroke-width="1.545" width="44" x="769" y="181"/>
<rect fill="none" fill-opacity="0" height="15" id="svg_10" stroke="#000069" stroke-linejoin="round" stroke-miterlimit="4.9" stroke-width="1.545" width="44" x="769" y="199"/>
</g> */

var xmlns = "http://www.w3.org/2000/svg";

for(i=0; i<8; i++)
{
    thermometre = document.createElementNS(xmlns, "g");  //thermomètre
    thermometre.setAttribute("class", "layer");
    // thermometre.setAttribute("width", "250");
    // thermometre.setAttribute("height", "142");
    rectangle_cadre = document.createElementNS(xmlns, "rect");
    //  width="50" height="42" x="37" y="171"   -- cadre tour
    rectangle_cadre.setAttribute("x", "0");
    rectangle_cadre.setAttribute("y", "0");
    rectangle_cadre.setAttribute("width", "50");
    rectangle_cadre.setAttribute("height", "47");
    rectangle_cadre.setAttribute("style", style_rect);
    
    rectangle_temp = document.createElementNS(xmlns, "rect");
    //  width="44" height="15" x="39" y="174.625"
    rectangle_temp.setAttribute("width", "44");
    rectangle_temp.setAttribute("height", "15");
    rectangle_temp.setAttribute("x", "3");
    rectangle_temp.setAttribute("y", "3");
    rectangle_temp.setAttribute("style", style_rect);
    
    rectangle_hydro = document.createElementNS(xmlns, "rect");
    //  width="44" height="15" x="39.6875" y="193"
    rectangle_hydro.setAttribute("width", "44");
    rectangle_hydro.setAttribute("height", "15");
    rectangle_hydro.setAttribute("x", "3");
    rectangle_hydro.setAttribute("y", "21");
    rectangle_hydro.setAttribute("style", style_rect);
    
    text_temp = document.createElementNS(xmlns, "text");
    //  style="font-style:normal;font-weight:normal;font-size:10.5833px;line-height:1.25;font-family:sans-serif;fill:#000000;fill-opacity:1;stroke:none;stroke-width:0"
    //                x="43" y="186"
    text_temp.setAttribute("x", "5");
    text_temp.setAttribute("y", "14");
    text_temp.setAttribute("name", "temp");
    text_temp.setAttribute("style", "font-style:normal;font-weight:normal;font-size:10.5833px;line-height:1.25;font-family:sans-serif;fill:#000000;fill-opacity:1;stroke:none;stroke-width:0");
    text_temp.textContent = "20.0";
    
    text_temp_exp = document.createElementNS(xmlns, "text");
    //  style="font-style:normal;font-weight:normal;font-size:5px;line-height:1.25;font-family:sans-serif;fill:#000000;fill-opacity:1;stroke:none;stroke-width:0"
    //  x="69" y="182" id="text10136-2">
    text_temp_exp.setAttribute("x", "33");
    text_temp_exp.setAttribute("y", "10");
    text_temp_exp.setAttribute("style", "font-style:normal;font-weight:normal;font-size:5px;line-height:1.25;font-family:sans-serif;fill:#000000;fill-opacity:1;stroke:none;stroke-width:0");
    text_temp_exp.textContent = "°C";
    
    text_hydro = document.createElementNS(xmlns, "text");
    //  style="font-style:normal;font-weight:normal;font-size:10.5833px;line-height:1.25;font-family:sans-serif;fill:#000000;fill-opacity:1;stroke:none;stroke-width:0"
    //                x="43" y="204" 
    text_hydro.setAttribute("x", "5");
    text_hydro.setAttribute("y", "32");
    text_hydro.setAttribute("name", "hygro");
    text_hydro.setAttribute("style", "font-style:normal;font-weight:normal;font-size:10.5833px;line-height:1.25;font-family:sans-serif;fill:#000000;fill-opacity:1;stroke:none;stroke-width:0");
    text_hydro.textContent = "70,0";
    
    text_hydro_exp = document.createElementNS(xmlns, "text");
    // style="font-style:normal;font-weight:normal;font-size:5px;line-height:1.25;font-family:sans-serif;fill:#000000;fill-opacity:1;stroke:none;stroke-width:0"
    // x="68" y="200" id="text10136-5-6">
    text_hydro_exp.setAttribute("x", "33");
    text_hydro_exp.setAttribute("y", "28");
    text_hydro_exp.setAttribute("style", "font-style:normal;font-weight:normal;font-size:5px;line-height:1.25;font-family:sans-serif;fill:#000000;fill-opacity:1;stroke:none;stroke-width:0");
    text_hydro_exp.textContent = "%HR";
    
    
    thermometre.appendChild(rectangle_cadre);
    thermometre.appendChild(rectangle_temp);
    thermometre.appendChild(rectangle_hydro);
    thermometre.appendChild(text_hydro);
    thermometre.appendChild(text_hydro_exp);
    thermometre.appendChild(text_temp);
    thermometre.appendChild(text_temp_exp);

    position = "translate(" + position_thermometres[i].pos_x + "," + position_thermometres[i].pos_y + ") scale(2)";
    thermometre.setAttribute("transform", position);
    thermometre.setAttribute("id", "dv-"+ (i+1));
    
    var_svg.appendChild(thermometre);
}