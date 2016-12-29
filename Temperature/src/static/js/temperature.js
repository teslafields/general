var myVar = setInterval(myTimer, 1000);

function temperature(data){
  document.getElementById("temp").innerHTML = data.result.temperature[data.result.temperature.length-1][1];
  drawChart(data.result);
}
function myTimer() {
    $.getJSON('/temperature')
    .done(temperature);
    var d = new Date();
    document.getElementById("txt2").innerHTML = d.toLocaleTimeString();
}
