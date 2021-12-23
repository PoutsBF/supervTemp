$(function() {
    $('#table').bootstrapTable()
});

var socket = new WebSocket('ws://' + document.domain + ':' + location.port);
socket.on('connect', function() {
        // we emit a connected message to let knwo the client that we are connected.
    socket.send('client_connected', {data: 'New client!'});
});

socket.on('my_response', function (data) {
    console.send('message from backend ' + data);
});

socket.on('majData', function (data) {
    for (item of data)
    {
        console.log('message from backend ' + item);
        $('#dv-' + item[0] + ' [name="temp"]')[0].innerHTML = item[3];
        $('#dv-' + item[0] + ' [name="hygro"]')[0].innerHTML = item[4];
        $('#dv-' + item[0] + ' [name="bat"]').title = "batterie : " + item[5];
        $('#dv-' + item[0] + ' [name="bat"]').alt = "batterie : " + item[5];      
    }
});

socket.on('alert', function (data) {
    alert('Alert Message!! ' + data);
});

function json_button() {
    socket.send('json_button', '{"message": "test"}');
}

function alert_button() {
    socket.send('alert_button', 'Message from client!!')
}

// <rect
//   style="fill:#000000;fill-opacity:0.109804;stroke:#000069;stroke-width:1.545;stroke-linejoin:round;stroke-miterlimit:4.9;stroke-dasharray:none;stroke-opacity:0.535484"
//   id="rect25740"
//   width="50.270832"
//   height="42.333332"
//   x="37.041668"
//   y="171.97917" />
// <rect
//   style="mix-blend-mode:normal;fill:#000000;fill-opacity:0.112903;stroke:#000069;stroke-width:1.54499;stroke-linejoin:round;stroke-miterlimit:4.9;stroke-dasharray:none;stroke-opacity:0.535484"
//   id="rect3542"
//   width="44.979168"
//   height="15.874994"
//   x="39.687504"
//   y="174.625" />
// <text
//   xml:space="preserve"
//   style="font-style:normal;font-weight:normal;font-size:10.5833px;line-height:1.25;font-family:sans-serif;fill:#000000;fill-opacity:1;stroke:none;stroke-width:0.264583"
//   x="43.215515"
//   y="186.08981"
//   id="temp"><tspan
//     sodipodi:role="line"
//     id="tspan4490"
//     style="stroke-width:0.264583"
//     x="43.215515"
//     y="186.08981">20.5</tspan></text>
// <text
//   xml:space="preserve"
//   style="font-style:normal;font-weight:normal;font-size:5.65103px;line-height:1.25;font-family:sans-serif;fill:#000000;fill-opacity:1;stroke:none;stroke-width:0.211913"
//   x="69.608765"
//   y="182.05086"
//   id="text10136"><tspan
//     sodipodi:role="line"
//     id="tspan10134"
//     style="font-size:5.65103px;stroke-width:0.211913"
//     x="69.608765"
//     y="182.05086">°C</tspan></text>
// <rect
//   style="fill:#000000;fill-opacity:0.109804;stroke:#000069;stroke-width:1.545;stroke-linejoin:round;stroke-miterlimit:4.9;stroke-dasharray:none;stroke-opacity:0.535484"
//   id="rect3542-3"
//   width="44.979172"
//   height="15.874994"
//   x="39.6875"
//   y="193.14583" />
// <text
//   xml:space="preserve"
//   style="font-style:normal;font-weight:normal;font-size:10.5833px;line-height:1.25;font-family:sans-serif;fill:#000000;fill-opacity:1;stroke:none;stroke-width:0.264583"
//   x="43.215511"
//   y="204.61064"
//   id="hygro"><tspan
//     sodipodi:role="line"
//     id="tspan4490-6"
//     style="stroke-width:0.264583"
//     x="43.215511"
//     y="204.61064">78.9</tspan></text>
// <text
//   xml:space="preserve"
//   style="font-style:normal;font-weight:normal;font-size:5.65103px;line-height:1.25;font-family:sans-serif;fill:#000000;fill-opacity:1;stroke:none;stroke-width:0.211913"
//   x="68.550423"
//   y="200.57169"
//   id="text10136-5"><tspan
//     sodipodi:role="line"
//     id="tspan10134-4"
//     style="font-size:5.65103px;stroke-width:0.211913"
//     x="68.550423"
//     y="200.57169">%HR</tspan></text>
// </g>

position_thermometres = [
    {pos_x : 37, pos_y : 171},   // 0
    {pos_x : 50, pos_y : 42},   // 1
    {pos_x : 50, pos_y : 42},   // 2
    {pos_x : 37, pos_y : 171},   // 3
    {pos_x : 50, pos_y : 42},   // 4
    {pos_x : 50, pos_y : 42},   // 5
    {pos_x : 50, pos_y : 42},   // 6
    {pos_x : 50, pos_y : 42},   // 7
    {pos_x : 50, pos_y : 42}    // 8
    ];
parametres_thermometres = {
    largeur : 50,
    hauteur : 42
};
valeur = 10;

var_svg = document.getElementById("svgMaison");

for(i=0; i<8; i++)
{
    thermometre = document.createElement("g");
    rectangle_cadre = document.createElement("rect");
    rectangle_cadre.setAttribute("x", position_thermometres[i].pos_x.toString());
    rectangle_cadre.setAttribute("y", position_thermometres[i].pos_y.toString());
    rectangle_temp = document.createElement("rect");
    rectangle_hydro = document.createElement("rect");
    text_temp = document.createElement("rect");
    text_hydro = document.createElement("rect");
    
    thermometre.appendChild(rectangle_cadre);
    thermometre.appendChild(rectangle_temp);
    thermometre.appendChild(rectangle_hydro);
    thermometre.appendChild(rectangle_temp);
    thermometre.appendChild(rectangle_hydro);
    var_svg.appendChild(thermometre);
}