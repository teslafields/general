
// function temperature(data){
//   document.getElementById("temp").innerHTML = data.result.temperature[data.result.temperature.length-1][1];
//   drawChart(data.result);
// }
// function myTimer() {
//     $.getJSON('/temperature')
//     .done(temperature);
//     var d = new Date();
//     document.getElementById("txt2").innerHTML = d.toLocaleTimeString();
// }


function make_base_auth(user, password) {
    var tok = user + ':' + password;
    var hash = btoa(tok);
    return 'Basic ' + hash;
}

jQuery(function($) {
  $("#navGym").on("click", function(){
    $.ajax({
        type: 'GET',
        url: 'http://179.223.188.164:5000/gym/',
        dataType: 'json',
        headers: {
            "Authorization": make_base_auth("benhurzi@gmail.com", "pierin2017")
        },
        // beforeSend: function (xhr) {
        //     xhr.setRequestHeader('Authorization', make_base_auth('benhurzi@gmail.com', 'pierin2017'));
        // },
        success: function (data) {
          console.log(data);}
        });
    });
});
