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
var all_div = [
      "#div-gym",
      "#div-jjclass"
]
var table;

hideAll = function() {
    for(i=0; i<all_div.length; i++) {
      $(all_div[i]).hide();
    }
}

showGym = function(data) {
  console.log(data)
  $("#div-student").hide();
  $("#div-gym").show();
}


showStudent = function(data, table) {
  $("#div-gym").hide();
  table.clear()
  $.each(data, function(key, value){
    table.row.add([value.full_name, value.email]).draw();
  })


  $("#div-student").show();
}

submitGym = function() {
  var gym = {};
  gym['name'] = $("#gym-name").val();
  // gym['addr'] = $("#gym-addr").val();
  // gym['contact'] = $("#gym-contact").val();
  console.log(gym);
  // $.ajax({
  //     type: 'POST',
  //     url: 'http://179.223.188.164:5000/gym/',
  //     dataType: 'json',
  //     data: gym,
  //     headers: {
  //         "Authorization": make_base_auth("benhurzi@gmail.com", "pierin2017")
  //     },
  //     success: function(data) {
  //       console.log(data);
  //     }
  //     });
}


function make_base_auth(user, password) {
    var tok = user + ':' + password;
    var hash = btoa(tok);
    return 'Basic ' + hash;
}

$( document ).ready(function() {
    hideAll();
    let table = $("#table-student").DataTable({
      columns: [
                {title: "Name"},
                {title: "Email"}
              ],
    });
  $("#gym-contact").on('change', function (event) {
    console.log(event.target.value);
    // console.log($("gym-name").attr('value'));
    // if ($.isNumeric(event.originalEvent.key)){
    //   console.log(true);
    // }else{
    //   console.log(false);
    // }
  })
  $("#navGym").on("click", function(){
    // $.ajax({
    //     type: 'GET',
    //     url: 'http://179.223.188.164:5000/gym/',
    //     dataType: 'json',
    //     headers: {
    //         "Authorization": make_base_auth("benhurzi@gmail.com", "pierin2017")
    //     },
    //     success: function(data) {
    //       showGym(data.results);
    //     }
    //     });
      showGym({name: "bla"});
    });

    $("#navStudent").on("click", function(){
      $.ajax({
          type: 'GET',
          url: 'http://179.223.188.164:5000/user/',
          dataType: 'json',
          headers: {
              "Authorization": make_base_auth("benhurzi@gmail.com", "pierin2017")
          },
          success: function(data) {

            showStudent(data.results, table)
          }
        });
        // services.api.get("http://179.223.188.164:5000/user/")
      });

    $("#submit-gym").on("click", function(){
      submitGym();
    })
});
