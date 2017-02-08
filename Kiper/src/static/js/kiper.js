/* global countRow */

var item_menu = [
    '#div-menu-ipwall',
    '#div-menu-rf',
    '#div-menu-user',
    '#div-menu-qrcode-reader',
    '#div-menu-guest',
    '#div-menu-request',
    '#div-menu-logs',
    '#div-menu-behave',

    '#div-insert-ipwall',
    '#div-insert-set-rf',
    '#div-insert-user',
    '#div-insert-qrcode-reader',
    '#div-insert-guest',
    '#div-insert-request',

    '#div_delete_ipwall',
    '#div_delete_set_rf',
    '#div_delete_user',
    '#div_delete_qrcode_reader',
    '#div_delete_guest'
];

hide_all_div = function(){
    for(i=0; i<item_menu.length;i++){
        $(item_menu[i]).hide();
    };
};

show = function (event) {
    var corpo = "#corpo"+this.id.split('cabecalho')[1];
    if ($(corpo).is(':visible')) {
        $(corpo).hide();
        return;
    }
    $(corpo).show();
};

show_div = function (div) {
    $('#menu-principal').hide();
    $('#menu-principal-2').show();
    hide_all_div();
    $(div.data.name).show();
};

labelOffset1Model = function( text ){
    var label = $('<label>',{
       class: 'control-label col-md-offset-1',
       text: text
    });
    return label;
};

labelOffset3Model = function( text ){
    var label = $('<label>',{
       class: 'control-label col-md-offset-3',
       text: text
    });
    return label;
};

labelModel = function( text ){
    var label = $('<label>', {
       style:'padding: 15px; padding-left: 30px',
       text: text
    });
    return label;
};

breadcrumb = function(param){
    param.trigger('click');
};

showDivHistoric = function() {
    for(i = 1; i <= 10; i++){

        if(localStorage.getItem(i) === null) {
            localStorage.setItem(i, " ");
        }

        if(localStorage.getItem(i) !== " "){
            $('#div_historic').append(localStorage.getItem(i));
        }
    }
    $('#div_historic').show();
};

showDivHistoric();

//clearLocalStorage = function() {
//    localStorage.clear();
//};
//localStorage.clear();

historicList = function(item) {

    $('#div_historic').empty();
    var addItem = "<div style='padding: 5px'>" + item + "</div>";

    if(localStorage.getItem("1") === " ") {
        localStorage.setItem("1", addItem);
    } else {
        j = 9;
        for(i = 10; i > 1; i--){
            localStorage.setItem(i, localStorage.getItem(j));
            j--;
        }
        localStorage.setItem("1", addItem);
    }
    showDivHistoric();
};


// ***************
// *** IP WALL ***
// ***************

var arrayInputIpwall = [];
showDoorDependency = function (doorId) {
    if ($("#check_door_dependency"+doorId.data.id).is(':checked')) {
        $('#check_door_dependency_content'+doorId.data.id).empty();
        showDivDoorDependency(doorId);
        $('#check_door_dependency_content'+doorId.data.id).show();
    } else {
        $('#check_door_dependency_content'+doorId.data.id).empty();
        $('#check_door_dependency_content'+doorId.data.id).hide();
    };
};

inputDoorId = new function(){
    this.count = 0;
    this.get = function( text ){
        var input = $('<input>',{
           type: 'text',
            class: 'form-control',
            name: 'text'+this.count
        });
        return input;
    };
};

inputIpwallModel = new function(){
    this.count = 0;
    this.get = function(door_dependency){
        var select = $('<input>',{
            class: 'form-control',
            id: 'ipwall-'+door_dependency+'-'+this.count,
            name: 'ipwall-'+door_dependency+'-'+this.count,
            placeholder: 'ipwall_id',
            type: 'number'
        });
        arrayInputIpwall.push(select);
        this.count++;
        return select;
    };
};

var arrayInputDoorId = [];
inputDoorIdModel = new function(){
    this.count = 0;
    this.get = function(door_dependency){
        var select = $('<input>',{
            class: 'form-control',
            id: 'doorid-'+door_dependency+'-'+this.count,
            name: 'doorid-'+door_dependency+'-'+this.count,
            placeholder: 'door_id',
            type: 'number'
        });
        arrayInputDoorId.push(select);
        this.count++;
        return select;
    };
};

optionIpwallModel = function( ipwall ){
    var option = $('<option>',{
            value: ipwall.ipwall_id,
            text: ipwall.ipwall_id+' - '+ipwall.ipwall_name
        });
    return option;
};

//ipwall e user
buttonPlusModel = new function(){
    this.count = 0;
    this.get = function(){
        var button = ($('<button>',{
            class: 'btn btn-default glyphicon glyphicon-plus restrictAccessPlus',
            id: 'button_plus'+this.count,
            type: 'button'
        }));
        button.on('click', showDivRestrictAccess);
        this.count++;
        return button;
    };
};

//ipwall e user
buttonTrashModel = new function(){
    this.count = 0;
    this.get = function(){
        var button = ($('<button>',{
            class: 'btn btn-default glyphicon glyphicon-trash restrictAccessTrash',
            id: 'button_trash'+this.count,
            type: 'button'
        }));
        button.on('click', removeDivRestricAccess);
        this.count++;
        return button;
    };
};

lastButtonPlus = null;
buttonPlusModelDoorDependency = new function(){
    this.count = 0;
    this.get = function(doorId){
        var button = ($('<button>',{
            class: 'btn btn-default glyphicon glyphicon-plus restrictAccessPlus',
            id: 'button_plus'+this.count,
            type: 'button'
        }));
        button.on('click', {id: doorId.data.id}, showDivDoorDependency);
        lastButtonPlus = button;
        this.count++;
        return button;
    };
};

buttonTrashModelDoorDependency = new function(){
    this.count = 0;
    this.get = function(){
        var button = ($('<button>',{
            class: 'btn btn-default glyphicon glyphicon-trash restrictAccessTrash',
            id: 'button_trash'+this.count,
            type: 'button'
        }));
        button.on('click', revomeDivDoorDependency);
        this.count++;
        return button;
    };
};

inputIpWallIdModel = new function(){
    this.count = 0;
    this.get = function(){
        var input = ($('<input>',{
            class: 'form-control',
            name: 'start_time'+this.count,
            type: 'time'
        }));
        this.count++;
        return input;
    };
};

showDivDoorDependency = function(doorId){
    // se este foi chamado por um botao
    // ocultamos o botao plus e exibimos o trash
    var type = $(this).attr('type');
    if (type === 'button'){
        var control = this.id.split('button_plus')[1];
        $(this).hide();
        $(this).parent().find('#button_trash'+control).show();
    };

    //adicionando nova linha
    var divDoorDependency = $('<div>',{
        class: 'form-group',
        id: 'div_content_door_dependency'+doorId.data.id
    });

    divDoorDependency.append(labelModel(' ipwall_id '));
    divDoorDependency.append(inputIpwallModel.get(doorId.data.id));
    divDoorDependency.append(labelModel(' door_id '));
    divDoorDependency.append(inputDoorIdModel.get(doorId.data.id));
    divDoorDependency.append(labelModel('    '));

    divDoorDependency.append(buttonTrashModelDoorDependency.get(doorId).hide());
    divDoorDependency.append(buttonPlusModelDoorDependency.get(doorId));

    $('#check_door_dependency_content'+doorId.data.id).append(divDoorDependency);
};

showDivDoorDependencyDynamically = function(doorId){
    // se este foi chamado por um botao
    // ocultamos o botao plus e exibimos o trash

    //adicionando nova linha
    var divDoorDependency = $('<div>',{
        class: 'form-group',
        id: 'div_content_door_dependency'+doorId.data.id
    });

    divDoorDependency.append(labelModel(' ipwall_id '));
    divDoorDependency.append(inputIpwallModel.get(doorId.data.id));
    divDoorDependency.append(labelModel('    '));
    divDoorDependency.append(labelModel(' door_id '));
    divDoorDependency.append(inputDoorIdModel.get(doorId.data.id));
    divDoorDependency.append(labelModel('    '));
    divDoorDependency.append(buttonPlusModelDoorDependency.get(doorId).hide());
    divDoorDependency.append(buttonTrashModelDoorDependency.get(doorId).show());

    $('#check_door_dependency_content'+doorId.data.id).append(divDoorDependency);
};

revomeDivDoorDependency = function(){
    $(this).parent().remove();
};

showOptionDoors = function () {
    if ($("#check_control_doors").is(':checked')) {
        $('#check_door1').removeAttr("disabled");
        $('#check_door2').removeAttr("disabled");
    } else {
        $('#check_door1').removeAttr("checked");
        $('#check_door2').removeAttr("checked");
        $('#check_door1').attr("disabled", true);
        $('#check_door2').attr("disabled", true);
    }
};

var global_request=0;
showIpwall = function( ipwall ){
    if (ipwall.ipwall_id !== -1){
    div_principal = $('#show-ipwall');
    //<div class="panel panel-primary">
    div = $('<div>',{
        class: 'panel panel-primary',
        style: 'margin-bottom: 5px'
    });

    //<div class='panel-heading' id="cabecalho{{ipwall['ipwall_id']}}">
    div_heading = $('<div>',{
        class: 'panel-heading',
        id: 'cabecalho' + ipwall.ipwall_id
    });

    //ID: {{ ipwall['ipwall_id'] }}  Name: {{ ipwall['ipwall_name'] }}<br>
    div_heading.append('ID: ' + ipwall.ipwall_id + ' Name: ' + ipwall.ipwall_name);
//    div.append(div_heading);

    //<div class="panel-body" id="corpo{{ipwall['ipwall_id']}}">
    div_body = $('<div>', {
        class: 'panel-body',
        id: 'corpo' + ipwall.ipwall_id
    });

    var stringDoor1Dep = "";
    if (ipwall.door1_dependency) {
        if (ipwall.door1_dependency.length > 0) {
            $('#check_door_dependency1').trigger('click');
            $.each(ipwall.door1_dependency, function (key, value) {
                stringDoor1Dep += '<br><b>ipwall_id: </b>' + value.ipwall_id + '<b style="margin-left: 10px"> door_id: </b>' + value.door_id;
            });
        }

    }
    else {
        stringDoor1Dep = "<br>null";
    }

    var stringDoor2Dep = "";
    if (ipwall.door2_dependency) {
        if (ipwall.door2_dependency.length > 0) {
            $('#check_door_dependency2').trigger('click');
            $.each(ipwall.door2_dependency, function (key, value) {
                stringDoor2Dep += '<br><b>ipwall_id: </b>' + value.ipwall_id + '<b style="margin-left: 10px"> door_id: </b>' + value.door_id;
            });
        }
    }
    else {
        stringDoor2Dep = "<br>null";
    }

    var stringDays = "";
    if (ipwall.days_of_week) {
        $.each(ipwall.days_of_week, function (key, value) {
            stringDays += '<br><b>days_of_week: </b>' + key;
            stringDays += '<b style="margin-left: 10px"> start: </b>' + value.split("-")[0];
            stringDays += '<b style="margin-left: 10px"> end: </b>' + value.split("-")[1];
        });
    }

    div_body.append(
            '<div class="row">' +
            '<div class="col-md-2">' +
            '<b>ipwall_ip: </b>' + ipwall.ip +
            '<br><b>access_type: </b>' + ipwall.access_type +
            '<br><b>control_doors</b>' +
            '<br><b>door1: </b>' + ipwall.control_doors.door1 +
            '<b style="margin-left: 10px">door2: </b></b>' + ipwall.control_doors.door2 +
            '</div>' +

            '<div class="col-md-2">' +
            '<b>button_enable:</b> ' + ipwall.button_enable +
            '<br><b>disable_emergency:</b> ' + ipwall.disable_emergency +
            '</div>' +

            '<div class="col-md-8">' +
            '<div class="col-md-3 text-center"><b>door1_dependency</b>' + stringDoor1Dep + '</div>' +
            '<div class="col-md-3 text-center"><b>door2_dependency</b>' + stringDoor2Dep + '</div>' +
            '<div class="col-md-6 text-center"><b>allow_access</b>' + stringDays + '</div>' +
            '</div></div>'
            );

    var button_reset = $('<span>',{
        class: 'glyphicon glyphicon-off  pull-right',
        title: 'Reset',
        style: 'margin-left: 10px',
        id: 'button-reset-ipwall',
        name: ''+ipwall.ipwall_id
    });

    var button_edit = $('<span>',{
        class: 'glyphicon glyphicon-pencil pull-right',
        style: 'margin-left: 10px',
        title: 'Edit',
        id: 'button-edit-ipwall',
        name: ''+ipwall.ipwall_id
    });

    var button_remove = $('<span>',{
        class: 'glyphicon glyphicon-remove pull-right',
        style: 'margin-left: 10px',
        title: 'Delete',
        id: 'button-remove-ipwall',
        name: ''+ipwall.ipwall_id
    });

    var button_update = $('<span>',{
        class: 'glyphicon glyphicon-refresh pull-right',
        style: 'margin-left: 10px',
        title: 'Update',
        id: 'button-update-ipwall',
        name: ''+ipwall.ipwall_id
    });


    div_heading.append(button_remove);
    div_heading.append(button_edit);
    div_heading.append(button_reset);
    div_heading.append(button_update);
    div_heading.on("click", show);
    div.append(div_heading);
//    div.append(div_footer);
    div.append(div_body);

    div_body.hide();


    button_edit.on('click', showIpwallEdit);

    button_remove.on('click', function(){
        done = function(data){
            console.log(data);
            if (data.result === -1){
              alert('Remova os elementos associados a este IPWall')
            }
            $('#button-menu-ipwall').trigger('click');
        };
        var result = $.post('/delete_ipwall/' + ipwall.ipwall_id);
        result.done(done);
        historicList("IP Wall deleted");
        //location.reload();
        $('#button-menu-ipwall').trigger('click');

    });
    div_principal.append(div);
    // button_reset.on('click', resetIpwall(ipwall.ipwall_id));
    // button_update.on('click', updateIpwall(ipwall.ipwall_id));
//    $('#show-event').append(div);
}};

resetIpwall = function(id){
    var request = {};
    request['request_id'] = 12;
    request['ipwall_id'] = id;

    var result = $.post('/insert_request', JSON.stringify(request));
    result.done(done);

    historicList("REQUEST requested");
};

showIpwallEdit = function(){
    var id = $(this).attr('name'); //inserir novamente atributo name



    $.getJSON('/edit_ipwall/'+id, function( data ){
        $('#ipwall_id').val(data.ipwall_id).attr("disabled", true);
        $('#ipwall_name').val(data.ipwall_name);
        $('#ip').val(data.ip);
        console.log(data);
        if(data.door1_dependency){
            if(data.door1_dependency.length > 0){
                $('#check_door_dependency1').attr('checked', false);
                $('#check_door_dependency1').trigger('click');
                var length = data.door1_dependency.length -1;
                var iteration = 0;

                $.each(data.door1_dependency, function(key, value){
                    arrayInputIpwall.pop().val(value.ipwall_id);
                    arrayInputDoorId.pop().val(value.door_id);
                    if(iteration < length){
                        lastButtonPlus.trigger('click');
                    }
                    iteration++;
                });
                arrayInputIpwall = [];
                arrayInputDoorId = [];
            }
        }

        if(data.door2_dependency){
            if(data.door2_dependency.length > 0){
                $('#check_door_dependency2').attr('checked', false);
                $('#check_door_dependency2').trigger('click');
                var length = data.door2_dependency.length -1;
                var iteration = 0;
                $.each(data.door2_dependency, function(key, value){
                    arrayInputIpwall.pop().val(value.ipwall_id);
                    arrayInputDoorId.pop().val(value.door_id);
                    if(iteration<length){
                        lastButtonPlus.trigger('click');
                    }
                    iteration++;
                });
                arrayInputIpwall = [];
                arrayInputDoorId = [];
            }
        }

        if(data.control_doors.door1 || data.control_doors.door2){
            $('#check_door1').prop('checked', data.control_doors.door1);
            $('#check_door1').attr("disabled", false);
            $('#check_door2').prop('checked', data.control_doors.door2);
            $('#check_door2').attr("disabled", false);
            $("#check_control_doors").prop('checked', true);
        };

        $('#check_button_enable').prop('checked', data.button_enable);
        $('#check_disable_emergency').prop('checked', data.disable_emergency);
        $('#access_type').val(data.access_type);

        $('#div_allow_access_content').empty();
        countRow.count = 0;
        divAllowAccess();

        if(data.days_of_week) {
            var length = Object.keys(data.days_of_week).length - 1;
            var iteration = 0;
            $.each(data.days_of_week, function (key, value) {
                var startTime = value.split("-")[0];
                var endTime = value.split("-")[1];
                $('#select_ipwall_days_of_week-' + iteration).val(key);
                $('#ipwall_start_time-' + iteration).val(startTime);
                $('#ipwall_end_time-' + iteration).val(endTime);
                if (iteration < length) {
                    $('#button_plus').trigger('click');
                }
                iteration++;
            });
        }
    });
    $('#div-menu-ipwall').hide();
    $('#div-insert-ipwall').show();
    $('#breadcrumb_insertIpWall').text("Edit IP Wall");
    $('#title_insert_ipwall').text("Edit IP Wall");
    clearIpWall();
};

clearIpWall = function() {
    if($('#ipwall_id').val() !== ""){
        $('#ipwall_id').val("").attr("disabled", false);
        $('#ipwall_name').val("");
        $('#ip').val("");
        $('#access_type').val("");
        $('#check_control_doors').prop("checked", false);
        $('#check_door1').prop("checked", false);
        $('#check_door1').attr("disabled", true);
        $('#check_door2').prop("checked", false);
        $('#check_door2').attr("disabled", true);
        $('#check_button_enable').prop("checked", false);
        $('#check_disable_emergency').prop("checked", false);
    };

    $('#check_door_dependency1').prop("checked", false);
    $('#check_door_dependency_content1').hide();
    $('#check_door_dependency2').prop("checked", false);
    $('#check_door_dependency_content2').hide();

    this.inputStartTimeModel.count = 0;
    this.inputEndTimeModel.count = 0;
    buttonPlusModel.count = 0;
    buttonTrashModel.count = 0;
    countRow.count = 0;

    $('#allow_access').empty();
    divAllowAccess();
};

submitIpwall = function(){
    var ipwall = {};

    var inputs = document.getElementById('div-insert-ipwall').getElementsByTagName('input');
    var selects = document.getElementById('div-insert-ipwall').getElementsByTagName('select');
    ipwall['access_type'] = $('#access_type').val();

    for(i = 0; i < inputs.length; i++){
        if(inputs[i].id.match(/check/)){
            ipwall[inputs[i].id] = $(inputs[i]).prop("checked");
        }else{
            ipwall[inputs[i].id] = $(inputs[i]).val();
        }
    };

    for(i = 0; i < selects.length; i++) {
        ipwall[selects[i].id] = $(selects[i]).val();
    }

    done = function(data){
        console.log('IP Wall inserted with ' + data.result.msg);
        $('#button-menu-ipwall').trigger('click');
    };

    var result = $.post('/insert_ipwall', JSON.stringify(ipwall));
    result.done(done);

    var title = document.getElementById("title_insert_ipwall").textContent;
    if(title === "Edit IP Wall") {
        historicList("IP Wall edited");
    } else {
        historicList("IP Wall inserted");
    }
    setInterval(500);
    $('#button-menu-ipwall').trigger("click");
};

deleteAllIpwalls = function(){
    $.post('/delete_all_ipwalls');
    $('#button-menu-ipwall').trigger("click");

    historicList("All IP Walls deleted");
};

divAllowAccess = function(){
    var divContentAllowAccess = $('<div>',{
        class: 'form-group col-md-10 col-md-offset-1',
        id: 'div_allow_access_content'
    });

    var div_newRow = $('<div>', {
       class: 'row'
    });

    var label_day_of_week = '<div class="col-md-2"><label> day_of_week </label></div>';

    var select = $('<select>',{
        id: 'select_ipwall_days_of_week-' + countRow.count,
        name: 'select_ipwall_days_of_week',
        class: 'form-control'
    });
    select.append(optionDaysOfWeekModel());

    var divS = $('<div class="col-md-3">');
    divS.append(select);

    divContentAllowAccess.append(label_day_of_week);
    divContentAllowAccess.append(divS);

    var label_start = '<div class="col-md-1"><label> start </label></div>';

    var input_start_time = $('<input>',{
        id: 'ipwall_start_time-' + countRow.count,
        class: 'form-control col-md-2',
        value: 'start_time'
    });

    var divIn1 = $('<div class="col-md-2">');
    divIn1.append(input_start_time);

    divContentAllowAccess.append(label_start);
    divContentAllowAccess.append(divIn1);

    var label_end = '<div class="col-md-1"><label> end </label></div>';

    var input_end_time = $('<input>',{
        id: 'ipwall_end_time-' + countRow.count,
        class: 'form-control col-md-2',
        name: 'ipwall_end_time',
        type: 'time',
        value: 'end_time'
    });

    var divIn2 = $('<div class="col-md-2">');
    divIn2.append(input_end_time);

    divContentAllowAccess.append(label_end);
    divContentAllowAccess.append(divIn2);

    var button_plus = $('<button>',{
        class: 'btn btn-default glyphicon glyphicon-plus allowAccessPlus',
        id: 'button_plus',
        type: 'button'

    });
    var button_trash = $('<button>',{
        class: 'btn btn-default glyphicon glyphicon-trash allowAccessTrash',
        id: 'button_trash',
        type: 'button'
    });
    button_trash.hide();

    button_plus.on('click', function(){
        button_plus.remove();
        button_trash.show();
        divAllowAccess();
    });

    button_trash.on('click', function(){
        $(this).parent().remove();
    });
    divContentAllowAccess.append(button_plus);
    divContentAllowAccess.append(button_trash);

    div_newRow.append(divContentAllowAccess);

    $('#allow_access').append(div_newRow);
    countRow.count++;
};

// **************
// *** SET RF ***
// **************

optionDefaultIpwallModel = function(){
    var optionDefault = $('<option>',{
        value: '',
        text: 'Select a Ipwall'
    });
    return optionDefault;
};


optionRfModel = function( rf ){
    var option = $('<option>',{
       value: rf.set_rf_id,
       text: rf.set_rf_id
    });
    return option;
};

optionDefaultRfModel = function(){
    var optionDefault = $('<option>',{
        value: '',
        text: ''
    });
    return optionDefault;
};

addDropdownInsertSetRf = function(  ){
    var ipwall_id_1 = $('#ipwall_id_1').empty();
    var ipwall_id_2 = $('#ipwall_id_2').empty();
    var ipwall_id_3 = $('#ipwall_id_3').empty();
    var ipwall_id_4 = $('#ipwall_id_4').empty();

    ipwall_id_1.append(optionDefaultIpwallModel());
    ipwall_id_2.append(optionDefaultIpwallModel());
    ipwall_id_3.append(optionDefaultIpwallModel());
    ipwall_id_4.append(optionDefaultIpwallModel());

    $.getJSON( '/get_ipwalls', function( data ){
        $.each(data.result, function(key, value){
            ipwall_id_1.append(optionIpwallModel(value));
            ipwall_id_2.append(optionIpwallModel(value));
            ipwall_id_3.append(optionIpwallModel(value));
            ipwall_id_4.append(optionIpwallModel(value));
        });
    });
};

$("#select_ipwall_id").append(optionDefaultIpwallModel());

showSetRf = function( rf ){
    div_principal = $('#show_rf');
    div = $('<div>',{
        class: 'panel panel-primary',
        style: 'margin-bottom: 5px'
    });
    console.log(rf);
    div_heading = $('<div>',{
        class: 'panel-heading',
        id: 'cabecalho'+rf.set_rf_id
    });

    div_heading.append('ID: ' + rf.set_rf_id);

    div_body = $('<div>', {
        class: 'panel-body',
        id: 'corpo'+rf.set_rf_id
    });

    div_body.append(
            '<div class="row text-center">' +
            '<div class="col-md-3">' +
            '<b>Button1</b><br>' +
            '<b>ipwall_id: </b>' + rf.set_rf.button1.ipwall_id +
            '<b style="margin-left: 10px"> door_id: </b>' + rf.set_rf.button1.door_id +
            '</div>' +

            '<div class="col-md-3">' +
            '<b>Button2</b><br>' +
            '<b>ipwall_id: </b>' + rf.set_rf.button2.ipwall_id +
            '<b style="margin-left: 10px"> door_id: </b>' + rf.set_rf.button2.door_id +
            '</div>' +

            '<div class="col-md-3">' +
            '<b>Button3</b><br>' +
            '<b>ipwall_id: </b>' + rf.set_rf.button3.ipwall_id +
            '<b style="margin-left: 10px"> door_id: </b>' + rf.set_rf.button3.door_id +
            '</div>' +

            '<div class="col-md-3">' +
            '<b>Button4</b><br>' +
            '<b>ipwall_id: </b>' + rf.set_rf.button4.ipwall_id +
            '<b style="margin-left: 10px"> door_id: </b>' + rf.set_rf.button4.door_id +
            '</div></div>'

            );

    var button_edit = $('<span>',{
        class: 'glyphicon glyphicon-pencil pull-right',
        title: 'Edit',
        id: 'button-edit-ipwall',
        name: ''+rf.set_rf_id
    });

    var button_remove = $('<span>',{
        class: 'glyphicon glyphicon-remove pull-right',
        style: 'margin-left: 10px',
        title: 'Delete',
        id: 'button-remove-ipwall',
        name: ''+rf.set_rf_id
    });

    div_heading.append(button_remove);
    div_heading.append(button_edit);
    div.append(div_heading);
    div.append(div_body);

    div_body.hide();
    div_heading.on("click", show);

    button_edit.on('click', showSetRfEdit);

    button_remove.on('click', function(){
        done = function(data){
            if(data.result === -1){
              alert('Remova o User associado a este Set RF');
            }
            $('#button-menu-rf').trigger('click');
        };
        var result = $.post('/delete_set_rf/' + rf.set_rf_id);
        result.done(done);

        historicList("RF deleted");
    });
    div_principal.append(div);
};

showSetRfEdit = function(){
     var id = $(this).attr('name');
     addDropdownInsertSetRf();
     $.getJSON('/edit_rf/'+id, function(data){

        $('#set_rf_id').val(data.set_rf_id).attr("disabled", true);

        $('#ipwall_id_1').val(data.set_rf.button1.ipwall_id);
        $('#door_id_1').val(data.set_rf.button1.door_id);

        $('#ipwall_id_2').val(data.set_rf.button2.ipwall_id);
        $('#door_id_2').val(data.set_rf.button2.door_id);

        $('#ipwall_id_3').val(data.set_rf.button3.ipwall_id);
        $('#door_id_3').val(data.set_rf.button3.door_id);

        $('#ipwall_id_4').val(data.set_rf.button4.ipwall_id);
        $('#door_id_4').val(data.set_rf.button4.door_id);

        $('#div-menu-rf').hide();
        $('#div-insert-set-rf').show();
        $('#breadcrumb_insertSetRF').text("Edit Set RF");
        $('#title_insert_rf').text("Edit Set RF");

     });
     clearSetRf();
};

clearSetRf = function() {
    if($('#set_rf_id').val() !== ""){
        $('#set_rf_id').val("").attr("disabled", false);
        $('#door_id_1').val("");
        $('#door_id_2').val("");
        $('#door_id_3').val("");
        $('#door_id_4').val("");
    };
};

submitSetRf = function(){
    var rf = {};

    var inputs = document.getElementById('div-insert-set-rf').getElementsByTagName('input');
    var selects = document.getElementById('div-insert-set-rf').getElementsByTagName('select');

    for(i = 0; i < inputs.length; i++) {
        rf[inputs[i].id] = $(inputs[i]).val();
    }

    for(i = 0; i < selects.length; i++) {
        rf[selects[i].id] = $(selects[i]).val();
    }

    done = function(data){
        console.log('Set RF inserted with '+data.result.msg);
        $('#button-menu-rf').trigger('click');
    };

    var result = $.post('/insert_set_rf', JSON.stringify(rf));
    result.done(done);

    var title = document.getElementById("title_insert_rf").textContent;
    if(title === "Edit Set RF") {
        historicList("Set RF edited");
    } else {
        historicList("Set RF inserted");
    }
};

deleteAllSetRf = function(){
    $.post('/delete_all_set_rf');
    $('#button-menu-rf').trigger("click");

    historicList("All RF deleted");
};

// ************
// *** USER ***
// ************

showRestrictAccess = function () {
    if ($("#check_restrict_access").is(':checked')) {
        $('#days_of_week').empty();
        showDivRestrictAccess();
        $('#days_of_week').show();
    } else {
        $('#days_of_week').hide();
    };
};

countIpWallDaysOfWeek = new function(){
    this.count = 0;
};

selectModel = new function(){
    this.count = 0;
    this.get = function(){
        var select = $('<select>',{
            class: 'form-control',
            id: 'select_days_of_week-'+this.count,
            name: 'select_days_of_week-'+this.count
        });
        this.count++;
        return select;
    };
};

//var divIpwallAccessTag = $('#div_ipwall_access_tag').empty();
addDropdownRfIdInsertUser = function(){
    var select = $('#select_set_rf_id').empty();
    select.append(optionDefaultRfModel());
    $.getJSON('/get_rfs', function(data){
       $.each(data.result, function(key, value){
           select.append(optionRfModel(value));
       });
    });
};

addIpwallCheckList = function( divId, name ){
    var divIpwallAccess = $('#' + divId).empty();
    userLabelModel = function(id, text){
        var label = $('<label>',{
            class: 'control-label',
            text: id+' - '+text
        });
        return label;
    };
    userInputModel = function( value ){
        var input = $('<input>',{
           id: 'check_ipwall_id_' + name + '+' + value,
           type: 'checkbox',
           value: value,
           name: 'check_ipwall_id+' + value
        });
        return input;
    };
    $.getJSON('/get_ipwalls', function(data){
        $.each(data.result, function(key, value){
            if (value.ipwall_id !== -1){
              label = userLabelModel(value.ipwall_id, value.ipwall_name);
              label.prepend(userInputModel(value.ipwall_id));
              divIpwallAccess.append(label);
              divIpwallAccess.append('</br>');
            }
        });
    });
};



optionDaysOfWeekModel = function(){
    var target = [];
    target.push($('<option>', {
        value: 'null',
        text: ' '
    }));
    target.push($('<option>', {
        value: 'sunday',
        text: 'Sunday'
    }));
    target.push($('<option>', {
        value: 'monday',
        text: 'Monday'
    }));
    target.push($('<option>', {
        value: 'tuesday',
        text: 'Tuesday'
    }));
    target.push($('<option>', {
        value: 'wednesday',
        text: 'Wednesday'
    }));
    target.push($('<option>', {
        value: 'thursday',
        text: 'Thursday'
    }));
    target.push($('<option>', {
        value: 'friday',
        text: 'Friday'
    }));
    target.push($('<option>', {
        value: 'saturday',
        text: 'Saturday'
    }));
    return target;
};

inputStartTimeModel = new function(){
    this.count = 0;
    this.get = function(){
        var input = ($('<input>',{
            class: 'form-control',
            name: 'start_time-'+this.count,
            id: 'start_time-'+this.count,
            type: 'time',
            value: 'start_time'
        }));
        this.count++;
        return input;
    };
};

inputEndTimeModel = new function(){
    this.count = 0;
    this.get = function(){
        var input = ($('<input>',{
            class: 'form-control ',
            name: 'end_time-'+this.count,
            id: 'end_time-'+this.count,
            type: 'time',
            value: 'end_time'
        }));
        this.count++;
        return input;
    };
};

countRow = function(){
     this.count = 0;
};

showDivRestrictAccess = function(){
    var divContentDaysOfWeek = $('<div>',{
        class: 'form-group',
        id: 'div_content_days_of_week'
    });
    var label_empty = labelModel('    ');
    var label_day_of_week = labelModel(' day_of_week ');

    var select = $('<select>',{
        id: 'select_days_of_week-' + countRow.count,
        name: 'select_days_of_week',
        class: 'form-control'
    });
    select.append(optionDaysOfWeekModel());

    divContentDaysOfWeek.append(label_empty);
    divContentDaysOfWeek.append(label_day_of_week);
    divContentDaysOfWeek.append(select);

    var label_start = labelModel(' start ');
    var input_start_time = $('<input>',{
        id: 'start_time-' + countRow.count,
        class: 'form-control',
        name: 'start_time',
        type: 'time',
        value: 'start_time'
    });

    divContentDaysOfWeek.append(label_empty);
    divContentDaysOfWeek.append(label_start);
    divContentDaysOfWeek.append(input_start_time);

    var label_end = labelModel(' end ');
    var input_end_time = $('<input>',{
        id: 'end_time-' + countRow.count,
        class: 'form-control ',
        name: 'end_time',
        type: 'time',
        value: 'end_time'
    });
    divContentDaysOfWeek.append(label_empty);
    divContentDaysOfWeek.append(label_end);
    divContentDaysOfWeek.append(input_end_time);

    var button_plus = $('<button>',{
        class: 'btn btn-default glyphicon glyphicon-plus restrictAccessPlus',
        id: 'button_plus_restrict_access',
        type: 'button'

    });
    var button_trash = $('<button>',{
        class: 'btn btn-default glyphicon glyphicon-trash restrictAccessTrash',
        id: 'button_trash_restrict_access',
        type: 'button'
    });
    button_trash.hide();

    button_plus.on('click', function(){
        button_plus.remove();
        button_trash.show();
        showDivRestrictAccess();
    });

    button_trash.on('click', function(){
        $(this).parent().remove();
    });
    divContentDaysOfWeek.append(label_empty);
    divContentDaysOfWeek.append(button_plus);
    divContentDaysOfWeek.append(button_trash);

    $('#days_of_week').append(divContentDaysOfWeek);
    this.countRow.count++;
};

removeDivRestricAccess = function(){
    $(this).parent().remove();
};

showUser = function( user ){
    div_principal = $('#show_user');
    div = $('<div>',{
        class: 'panel panel-primary',
        style: 'margin-bottom: 5px'
    });

    div_heading = $('<div>',{
        class: 'panel-heading',
        id: 'cabecalho'+user.user_id
    });

    div_heading.append('ID: ' + user.user_id);

    div_body = $('<div>', {
        class: 'panel-body',
        id: 'corpo'+user.user_id
    });

    var setRf_id = user.set_rf_id;
    if(setRf_id === '') {
        setRf_id = 'null';
    }

    var counterRF = user.counter_rf;
    if(counterRF === ""){
        counterRF = "null";
    }

    var secret = user.secret;
    if(secret === ''){
        secret = 'null';
    }
    console.log(user);
    var ipwallAccessTag = user.ipwall_access_tag;
    console.log(user.ipwall_access_tag);
    for(i = 0; i < user.ipwall_access_tag.length; i++ ) {
        console.log(user.ipwall_access_tag[i]);
        $.getJSON('/get_ipwall/' + user.ipwall_access_tag[i], function(data){
            console.log(data);
            ipwallAccessTag = '<div class="row col-md-offset-1">' + data.result.ipwall_id + ' - ' + data.result.ipwall_name + '</div>';
            $('#no_acesstag'+user.user_id).remove();
            $('#accessTag'+user.user_id).append(ipwallAccessTag);
        });
    }

    var stringDays = "";
    if(user.restrict_access){

        var days = "";
        var start = "";
        var end = "";

        $.each(user.days_of_week, function(key, value){
            days += '<b>days_of_week: </b>' + key + '<br>';
            start += '<b>start: </b>' + value.split("-")[0] + '<br>';
            end += '<b>end: </b>' + value.split("-")[1] + '<br>';
        });
        stringDays = '<div class="col-md-5 col-md-offset-1 text-left">' + days + '</div>'+
            '<div class="col-md-3">' + start + '</div>'+
            '<div class="col-md-3">' + end + '</div>';
    };

    div_body.append(
            '<div class="row">' +

            '<div class="col-md-2">' +
            '<b>set_rf_id: </b>' + setRf_id + '<br>' +
            '<b>tag_id: </b>' + user.tag_id + '<br>' +
            '<b>rf_id: </b>' + user.rf_id +
            '</div>' +

            '<div class="col-md-2">' +
            '<b>counter_rf: </b>' + counterRF + '<br>' +
            '<b>opening_time: </b>' + user.opening_time + '<br>' +
            '<b>secret: </b>' + secret + '<br>' +
            '</div>' +

            '<div class="col-md-2">' +
            '<b>blocked: </b>' + user.blocked + '<br>' +
            '<b>administrator: </b>' + user.administrator + '<br>' +
            '</div>' +

            '<div class="col-md-2" id="accessTag' + user.user_id + '">' +
            '<b>ipwall_access_tag: </b>' +
            '<div id="no_acesstag' + user.user_id + '" class="row col-md-offset-1"> null </div>'+
            '</div>' +

            '<div class="col-md-4 text-center">' +
            '<b>restrict_access: </b>' + user.restrict_access + '<br>' +
            stringDays +
            '</div>' +
            '</div>'
    );

    var button_edit = $('<span>',{
        class: 'glyphicon glyphicon-pencil pull-right',
        title: 'Edit',
        id: 'button-edit-ipwall',
        name: ''+user.user_id
    });

    var button_remove = $('<span>',{
        class: 'glyphicon glyphicon-remove pull-right',
        style: 'margin-left: 10px',
        title: 'Delete',
        id: 'button-remove-ipwall',
        name: ''+user.user_id
    });

    div_heading.append(button_remove);
    div_heading.append(button_edit);
    div.append(div_heading);
    div.append(div_body);

    div_body.hide();
    div_heading.on("click", show);

    button_edit.on('click', showUserEdit);

    button_remove.on('click', function(){
        done = function(data){
            $('#button-menu-user').trigger('click');
        };
        var result = $.post('/delete_user/' + user.user_id);
        result.done(done);

        historicList("User deleted");
    });
    div_principal.append(div);
};

showUserEdit = function() {
    var id = $(this).attr('name');
    addDropdownRfIdInsertUser();
    addIpwallCheckList("div_ipwall_access_tag", "user");
    $.getJSON('/edit_user/'+id, function(data){

        $('#user_id').val(data.user_id).attr("disabled", true);
        $('#select_set_rf_id').val(data.set_rf_id);
        $('#tag_id').val(data.tag_id);
        $('#rf_id').val(data.rf_id);
        $('#counter_rf').val(data.counter_rf);
        $('#opening_time').val(data.opening_time);

        for(i = 0; i < data.ipwall_access_tag.length; i++){
            $('#check_ipwall_id_user-' + data.ipwall_access_tag[i]).prop('checked',true);
        }

        $('#check_blocked').prop('checked', data.blocked);
        $('#check_administrator').prop('checked', data.administrator);

        if(data.restrict_access){
            $('#check_restrict_access').attr('checked', false);
            $('#check_restrict_access').trigger('click');
            var length = Object.keys(data.days_of_week).length -1;
            var iteration = 0;
            $.each(data.days_of_week, function(key, value){
                var startTime = value.split("-")[0];
                var endTime = value.split("-")[1];
                $('#select_days_of_week-'+iteration).val(key);
                $('#start_time-'+iteration).val(startTime);
                $('#end_time-'+iteration).val(endTime);
                if(iteration < length){
                    $('#button_plus_restrict_access').trigger('click');
                }
                iteration++;
            });
        };
    });
    $('#div-menu-user').hide();
    $('#div-insert-user').show();
    $('#breadcrumb_insertUser').text("Edit User");
    $('#title_insert_user').text("Edit User");
    clearUser();
};

clearUser = function() {
    if($('#user_id').val() !== ""){
        $('#user_id').val("").attr("disabled", false);
        $('#select_set_rf_id').val("");
        $('#tag_id').val("");
        $('#rf_id').val("");
        $('#counter_rf').val("");
        $('#opening_time').val("");
        $('#check_blocked').prop("checked", false);
        $('#check_administrator').prop("checked", false);
    };

    $('#check_restrict_access').prop("checked", false);
    $('#days_of_week').hide();
//        $('#days_of_week_content').remove();
    inputStartTimeModel.count = 0;
    inputEndTimeModel.count = 0;
    buttonPlusModel.count = 0;
    buttonTrashModel.count = 0;
    countRow.count = 0;
};

submitUser = function(){
    var user = {};

    var inputs = document.getElementById('div-insert-user').getElementsByTagName('input');
    var selects = document.getElementById('div-insert-user').getElementsByTagName('select');

    for(i = 0; i < inputs.length; i++) {
        if(inputs[i].id.match(/check/)){
            user[inputs[i].id] = $(inputs[i]).prop("checked");
        }else{
            user[inputs[i].id] = $(inputs[i]).val();
        }
    };

    for(i = 0; i < selects.length; i++) {
        user[selects[i].id] = $(selects[i]).val();
    }

    done = function(data){
        console.log('User inserted with ' + data.result.msg);
        $('#button-menu-user').trigger('click');
    };

    var result = $.post('/insert_user', JSON.stringify(user));
    result.done(done);

    var title = document.getElementById("title_insert_user").textContent;
    if(title === "Edit User") {
        historicList("User edited");
    } else {
        historicList("User inserted");
    }
};

deleteAllUsers = function(){
    $.post('/delete_all_users');
    $('#button-menu-user').trigger("click");

    historicList("All Users deleted");
};

// ***************
// *** QR CODE ***
// ***************

showQrcodeReader = function( qrcode_reader ){
    div_principal = $('#show-qrcode-reader');
    div = $('<div>',{
        class: 'panel panel-primary',
        style: 'margin-bottom: 5px'
    });

    div_heading = $('<div>',{
        class: 'panel-heading',
        id: 'cabecalho'+qrcode_reader.qrcode_reader_id
    });

    div_heading.append('ID: ' + qrcode_reader.qrcode_reader_id);

    div_body = $('<div>', {
        class: 'panel-body',
        id: 'corpo'+qrcode_reader.qrcode_reader_id
    });

    var stringRelation = "";

    var cam_id = "";
    var ipwall_id = "";
    var wiegand_id = "";

    $.each(qrcode_reader.relation, function(key, value){
        cam_id += '<b>cam_id: </b><label style="font-weight: normal">' + value.cam_id + '</label><br>';
        ipwall_id += '<b>ipwall_id: </b><label style="font-weight: normal">' + value.ipwall_id + '</label><br>';
        wiegand_id += '<b>wiegand_id: </b><label style="font-weight: normal">' + value.wiegand_id + '</label><br>';
    });
    stringRelation = '<div class="col-md-4">' + cam_id + '</div>'+
        '<div class="col-md-4">' + ipwall_id + '</div>'+
        '<div class="col-md-4">' + wiegand_id + '</div>';

    div_body.append(
            '<div class="row">' +
                '<div class="col-md-3 col-md-offset-1">' +
                    '<b>qrcode_reader_ip: </b>' + qrcode_reader.qrcode_reader_ip + '<br>' +
                '</div>' +
                '<div class="col-md-7 text-center"><b> Relation <b/><br>' +
                    stringRelation +
                '</div>' +
            '</div>'
    );
    var button_edit = $('<span>',{
        class: 'glyphicon glyphicon-pencil pull-right',
        title: 'Edit',
        id: 'button-edit-ipwall',
        name: '' + qrcode_reader.qrcode_reader_id
    });

    var button_remove = $('<span>',{
        class: 'glyphicon glyphicon-remove pull-right',
        style: 'margin-left: 10px',
        title: 'Delete',
        id: 'button-remove-ipwall',
        name: '' + qrcode_reader.qrcode_reader_id
    });

    div_heading.append(button_remove);
    div_heading.append(button_edit);
    div.append(div_heading);
    div.append(div_body);

    div_body.hide();
    div_heading.on("click", show);

    button_edit.on('click', showQrcodeReaderEdit);

    button_remove.on('click', function(){
        done = function(data){
            $('#button-menu-qrcode-reader').trigger('click');
        };
        var result = $.post('/delete_qrcode_reader/' + qrcode_reader.qrcode_reader_id);
        result.done(done);

        historicList("QR Code Reader deleted");
    });
    div_principal.append(div);
};

submitQrcodeReader = function(){
    var qrcode_reader = {};

    var inputs = document.getElementById('div-insert-qrcode-reader').getElementsByTagName('input');
    var selects = document.getElementById('div-insert-qrcode-reader').getElementsByTagName('select');

    for(i = 0; i < inputs.length; i++) {
        qrcode_reader[inputs[i].id] = $(inputs[i]).val();
    };

    for(i = 0; i < selects.length; i++) {
        qrcode_reader[selects[i].id] = $(selects[i]).val();
    }

    done = function(data){
        console.log('QR Code inserted with ' + data.result.msg);
        $('#button-menu-qrcode-reader').trigger('click');
    };

    var result = $.post('/insert_qrcode_reader', JSON.stringify(qrcode_reader));
    result.done(done);

    var title = document.getElementById("title_insert_qrcode_reader").textContent;
    if(title === "Edit QR Code Reader") {
        historicList("QR Code Reader edited");
    } else {
        historicList("QR Code Reader inserted");
    }
};

showQrcodeReaderEdit = function(){
    var id = $(this).attr('name');
    $.getJSON('/edit_qrcode_reader/'+id, function(data){
        console.log(data);
        $('#qrcode_reader_id').val(data.qrcode_reader_id).attr("disabled", true);
        $('#qrcode_reader_ip').val(data.qrcode_reader_ip);

        $('#div_relation_content').empty();
        countRow.count = 0;
        divRelation();

        var length = Object.keys(data.relation).length -1;
        var iteration = 0;
        $.each(data.relation, function(key, value){
            console.log(value);
            var ipwall_id = value.ipwall_id;
            var wiegand_id = value.wiegand_id;
            $('#relation_cam_id-' + iteration).val(key);
            // $('#relation_ipwall_id-' + iteration).val(ipwall_id);
            $('#relation_wiegand_id-' + iteration).val(wiegand_id);
            if(iteration < length){
                $('#button_plus_relation').trigger('click');
            }
            iteration++;
        });
    });
    $('#div-menu-qrcode-reader').hide();
    $('#div-insert-qrcode-reader').show();
    $('#breadcrumb_insertQrcodeReader').text("Edit QR Code Reader");
    $('#title_insert_qrcode_reader').text("Edit QR Code Reader");
    clearQrcodeReader(); // Clear tb est� aqui, pois caso usu�rio clique em editar em 2 registros seguidos, os dados do 1� registro precisam ser limpos para mostrar o 2� registro.
};

clearQrcodeReader = function() {
    $('#qrcode_reader_id').val("").prop("disabled", false);
    $('#qrcode_reader_ip').val("");

    buttonPlusModel.count = 0;
    buttonTrashModel.count = 0;
    countRow.count = 0;

    $('#relation').empty();
};

deleteAllQrcodeReaders = function(){
    $.post('/delete_all_qrcode_readers');
    $('#button-menu-qrcode-reader').trigger("click");

    historicList("All QR Code Readers deleted");
};

divRelation = function(){
    var divContentRelation = $('<div>',{
        id: 'div_relation_content',
        style: 'padding: 8px',
        class: 'col-md-12'
    });

//    var label_cam_id = '<div class="col-md-4"><label> cam_id </label></div>';
    var label_1 = $('<label>', {
       text: 'cam_id',
       class: 'col-md-4'
    });

//    var input_cam_id = '<div class="col-md-8">' +
//                '<input type="number" class="form-control" placeholder="cam_id" name="relation_cam_id" id ="relation_cam_id-' + countRow.count + '">' +
//                '</div>';
    var colMd8_input_1 = $('<div>', {
       class: 'col-md-8'
    });
    var input_1 = $('<input>', {
       type: 'number',
       class: 'form-control',
       placeholder: 'cam_id',
       name: 'relatin_cam_id',
       id: 'relation_cam_id-' + countRow.count
    });
    var col1_col2 = colMd8_input_1.append(input_1);

//    var col1 = '<div class="col-md-4">' + label_cam_id + input_cam_id + '</div>';
    var col1 = $('<div>', {
       class: 'col-md-4'
    });
    col1.append(label_1);
    col1.append(col1_col2);

//    var label_ipwall_id = '<div class="col-md-4"><label> ipwall_id </label></div>';
    var label_2 = $('<label>', {
       text: 'ipwall_id',
       class: 'col-md-4'
    });

//    var select_ipwall_id = '<div class="col-md-8">' +
//                                '<select class="form-control" id="relation_ipwall_id-' + countRow.count + '" name="relation_ipwall_id">' +
//                                '</select>' +
//                            '</div>';
    var colMd8_select_2 = $('<div>', {
       class: 'col-md-8'
    });
    var select_2 = $('<select>', {
       class: 'form-control',
       name: 'relatin_ipwall_id',
       id: 'relation_ipwall_id-' + countRow.count
    });
    var col2_col2 = colMd8_select_2.append(select_2);

//    var col2 = '<div class="col-md-4">' + label_ipwall_id + select_ipwall_id + '</div>';
    var col2 = $('<div>', {
       class: 'col-md-4'
    });
    col2.append(label_2);
    col2.append(col2_col2);

//    var label_wiegand_id = '<div class="col-md-7"><label> wiegand_id </label></div>';
    var label_3 = $('<label>', {
       text: 'wiegand_id',
       class: 'col-md-7'
    });

//    var select_wiegand_id = '<div class="col-md-5">' +
//                                '<select class="form-control" id="relation_wiegand_id-' + countRow.count + '" name="relation_wiegand_id">' +
//                                    '<option value="0"> 0 </option>' +
//                                    '<option value="1"> 1 </option>' +
//                                '</select>' +
//                            '</div>';
    var colMd5_select_3 = $('<div>', {
       class: 'col-md-5'
    });
    var select_3 = $('<select>', {
       class: 'form-control',
       name: 'relatin_wiegand_id',
       id: 'relation_wiegand_id-' + countRow.count
    });
    var option_0 = $('<option>', {
       value: '0',
       text: '0'
    });
    var option_1 = $('<option>', {
       value: '1',
       text: '1'
    });
    select_3.append(option_0);
    select_3.append(option_1);
    var col3_col2 = colMd5_select_3.append(select_3);

//    var col3 = '<div class="col-md-3">' + label_wiegand_id + select_wiegand_id + '</div>';
    var col3 = $('<div>', {
       class: 'col-md-3'
    });
    col3.append(label_3);
    col3.append(col3_col2);

    var button_plus = $('<button>',{
        class: 'btn btn-default glyphicon glyphicon-plus relationPlus',
        id: 'button_plus_relation',
        type: 'button'
    });

    var button_trash = $('<button>',{
        class: 'btn btn-default glyphicon glyphicon-trash relationTrash',
        id: 'button_trash_relation',
        type: 'button'
    });

    divContentRelation.append(col1);
    divContentRelation.append(col2);
    divContentRelation.append(col3);

    divContentRelation.append(button_plus);
    divContentRelation.append(button_trash);

    button_trash.hide();

    button_plus.on('click', function(){
        button_plus.remove();
        button_trash.show();
        divRelation();
    });

    button_trash.on('click', function(){
        $(this).parent().remove();
    });

    $('#relation').append(divContentRelation);
    selectIpwallRelation(countRow.count);

    countRow.count++;
};

selectIpwallRelation = function(count) {
    var select = $("#relation_ipwall_id-" + count);
    select.append(optionDefaultIpwallModel());
    $.getJSON('/get_ipwalls', function(data){
       $.each(data.result, function(key, value){
            select.append(optionIpwallModel(value));
       });
    });
};

// *************
// *** GUEST ***
// *************

submitGuest = function(){
    var guest = {};

    var inputs = document.getElementById('div-insert-guest').getElementsByTagName('input');

    for(i = 0; i < inputs.length; i++) {
        if(inputs[i].id.match(/check/)){
            guest[inputs[i].id] = $(inputs[i]).prop("checked");
        }else{
            guest[inputs[i].id] = $(inputs[i]).val();
        }
    };

    console.log(guest);

    done = function(data){
        console.log('Guest Inserted with ' + data.result.msg);
        $('#button-menu-guest').trigger('click');
    };

    var result = $.post('/insert_guest', JSON.stringify(guest));
    result.done(done);

    var title = document.getElementById("title_insert_guest").textContent;
    if(title === "Edit Guest") {
        historicList("Guest edited");
    } else {
        historicList("Guest inserted");
    }
};

showGuest = function( guest ) {
    console.log(guest);
    div_principal = $('#show-guest');
    div = $('<div>', {
        class: 'panel panel-primary',
        style: 'margin-bottom: 5px'
    });

    div_heading = $('<div>', {
        class: 'panel-heading',
        id: 'cabecalho' + guest.guest_id
    });

    div_heading.append('ID: ' + guest.guest_id);

    div_body = $('<div>', {
        class: 'panel-body',
        id: 'corpo' + guest.guest_id
    });

    var ipwallAccessList = guest.ipwall_access_list;
    for (i = 0; i < guest.ipwall_access_list.length; i++) {
        $.getJSON('/get_ipwall/' + guest.ipwall_access_list[i], function (data) {
            ipwallAccessList = '<div class="row col-md-offset-1">' + data.result.ipwall_id + ' - ' + data.result.ipwall_name + '</div>';
            $('#ipwallAccessList').append(ipwallAccessList);
            $('#no_ipwallAccessList').hide();
        });
    }


    var validFrom = guest.valid.valid_from;
    if(validFrom === "") {
        validFrom = "null"
    } else {
        validFrom = guest.valid.valid_from.split("T")[0] + ", " + guest.valid.valid_from.split("T")[1];
    }

    var validUntil = guest.valid.valid_until;
    if(validUntil === "") {
        validUntil = "null"
    } else {
        validFrom = guest.valid.valid_until.split("T")[0] + ", " + guest.valid.valid_until.split("T")[1];
    }

    var code = guest.code;
    if(code === "") {
        code = "null";
    }

    div_body.append(
            '<div class="row">' +
            '<div class="col-md-3">' +
            '<b>valid_from: </b>' + validFrom + '<br>' +
            '</div>' +
            '<div class="col-md-3">' +
            '<b>valid_until: </b>' + validUntil + '<br>' +
            '</div>' +
            '<div class="col-md-6">' +
            '<div class="col-md-4">' +
            '<b>access_counter: </b>' + guest.valid.access_counter + '<br>' +
            '</div>' +
            '<div class="col-md-3">' +
            '<b>code: </b>' + guest.code + '<br>' +
            '</div>' +
            '<div class="col-md-5" id="ipwallAccessList">' +
            '<b>ipwall_access_list: </b>' +
            '<div id="no_ipwallAccessList" class="row col-md-offset-1"> null </div>' +
            '</div>' +
            '</div>' +
            '</div>'
            );

    var button_edit = $('<span>',{
        class: 'glyphicon glyphicon-pencil pull-right',
        title: 'Edit',
        id: 'button-edit-ipwall',
        name: '' + guest.guest_id
    });

    var button_remove = $('<span>',{
        class: 'glyphicon glyphicon-remove pull-right',
        style: 'margin-left: 10px',
        title: 'Delete',
        id: 'button-remove-ipwall',
        name: '' + guest.guest_id
    });

    div_heading.append(button_remove);
    div_heading.append(button_edit);
    div.append(div_heading);
    div.append(div_body);

    div_body.hide();
    div_heading.on("click", show);

    button_edit.on('click', showGuestEdit);

    button_remove.on('click', function(){
        done = function(data){
            $('#button-menu-guest').trigger('click');
        };
        var result = $.post('/delete_guest/' + guest.guest_id);
        result.done(done);

        historicList("Guest deleted");
    });
    div_principal.append(div);
};

showGuestEdit = function(){
    var id = $(this).attr('name');
    addIpwallCheckList("div_ipwall_access_list", "guest");
    $.getJSON('/edit_guest/'+id, function(data){
        $('#guest_id').val(data.guest_id).attr("disabled", true);
        $('#valid_from').val(data.valid.valid_from);
        $('#valid_until').val(data.valid.valid_until);
        $('#access_counter').val(data.valid.access_counter);
        $('#code').val(data.code);

        for(i = 0; i < data.ipwall_access_list.length; i++){
            $('#check_ipwall_id_guest+' + data.ipwall_access_list[i]).prop('checked',true);
        }
    });
    $('#div-menu-guest').hide();
    $('#div-insert-guest').show();
    $('#breadcrumb_insertGuest').text("Edit Guest");
    $('#title_insert_guest').text("Edit Guest");
    clearUser();
};

clearGuest = function(){
    if($('#guest_id').val() !== ""){
        $('#guest_id').val("").attr("disabled", false);
        $('#valid_from').val("");
        $('#valid_until').val("");
        $('#access_counter').val("");
        $('#code').val("");
    }
};

deleteAllGuests = function(){
    $.post('/delete_all_guests');
    $('#button-menu-guest').trigger('click');
    historicList("All Guests deleted");
};

// ***************
// *** REQUEST ***
// ***************

selectIpWall = function () {

    var select1 = $("#select_ipwall_id_1").empty();
    select1.append(optionDefaultIpwallModel());
    $.getJSON('/get_ipwalls', function(data){
       $.each(data.result, function(key, value){
            select1.append(optionIpwallModel(value));
       });
    });

    var select2 = $("#select_ipwall_id_2").empty();
    select2.append(optionDefaultIpwallModel());
    $.getJSON('/get_ipwalls', function(data){
       $.each(data.result, function(key, value){
            select2.append(optionIpwallModel(value));
       });
    });
};

submitFlush = function(){
  var request = {};
  request['request_id'] = 16;
  request['version'] = $('#flush-version').val();
  request['cmd'] = 'flush';
  $.post('/insert_request', JSON.stringify(request));
  historicList("Flush requested");
}

clearUpdateIpwall = function() {
    addDropdownIpwall("#select_ipwall_id_3");
    $("#http_server_ip_2").val("10.5.0.13");
    $("#http_server_port_2").val("8888");
    $("#file_path2").val("/updates/ipwall/ipax282h16-M3-K.bin");
    $("#file_name2").val("ipax282h16-M3-K.bin");
    $("#file_size").val("459256");
};
submitUpdateIpwall = function(){
    var request = {};
    request['request_id'] = 13;
    request['cmd'] = 'update_ipwall';

    request['file_size'] = $("#file_size").val();
    request['file_path'] = $("#file_path2").val();
    request['http_server_ip'] = $("#http_server_ip_2").val();
    request['http_server_port'] = $("#http_server_port_2").val();
    request['ipwall_id'] = $("#select_ipwall_id_3").val();
    request['file_name'] = $("#file_name2").val();

    // var inputs = document.getElementById('modal_update_ipwall').getElementsByTagName('input');
    // var selects = document.getElementById('modal_update_ipwall').getElementsByTagName('select');
    //
    // for(i = 0; i < inputs.length; i++) {
    //     request[inputs[i].id] = $(inputs[i]).val();
    // }
    //
    // for(i = 0; i < selects.length; i++) {
    //     request[selects[i].id] = $(selects[i]).val();
    //
    // }

    done = function(data){
        console.log('REQUEST requested with ' + data.result.msg);
        $('#button-menu-request').trigger('click');
    };
    console.log('request');
    console.log(request);
    var result = $.post('/insert_request', JSON.stringify(request));
    result.done(triggador);
    $('#modal_update_ipwall').modal('hide');
    historicList("Update Ipwall requested");
};

clearUpdateCPU = function() {
    $("#update_to_version").val("1.5.2");
    $("#check_restore").attr('checked', false);
    $("#http_server_ip").val("10.5.0.13");
    $("#http_server_port").val("8888");
    $("#file_path").val("/updates/kiper152");
    $("#update_file").val("last-version.update_web");
    $('#send_update_cpu').on('click', submitUpdateCpu);
};

submitUpdateCpu = function(){
    var request = {};
    console.log('maickel feio');
    request['request_id'] = 6;
    // $('#request_id').val('request_' + requestCount);
    // requestCount++;
    request['cmd'] = 'update_cpu';

    var inputs = document.getElementById('modal_update_cpu').getElementsByTagName('input');

    for(i = 0; i < inputs.length; i++) {
        if(inputs[i].id.match(/check/)){
            request[inputs[i].id] = $(inputs[i]).prop("checked");
        }else{
            request[inputs[i].id] = $(inputs[i]).val();
        }
    }

    done = function(data){
        console.log('REQUEST requested with ' + data.result.msg);
        $('#button-menu-request').trigger('click');
    };

    console.log(request);

    var result = $.post('/insert_request', JSON.stringify(request));
    result.done(triggador);
    $('#modal_update_cpu').modal('hide');
    historicList("Update CPU requested");
};

clearResetIpwall = function() {
    $("#select_ipwall_id_1").val("");
    $('#send_get_sensor_status').on('click', submitResetIpwall);

};
submitResetIpwall = function () {
    var request = {};
    request['request_id'] = 12;
    request['cmd'] = 'reset_ipwall';
    var selects = document.getElementById('modal_get_sensor_relay_status').getElementsByTagName('select');
    for(i = 0; i < selects.length; i++) {
        request[selects[i].id] = $(selects[i]).val();
    }

    var result = $.post('/insert_request', JSON.stringify(request));
    result.done(triggador);

    historicList("Reset Ipwall requested");

};

addDropdownIpwall = function(id){
    var ipwall = $(id).empty();

    $.getJSON( '/get_ipwalls', function( data ){
        $.each(data.result, function(key, value){
            ipwall.append(optionIpwallModel(value));
        });
    });
};

clearGetSensorsStatus = function() {
    addDropdownIpwall('#select_ipwall_id_1');
    $('#send_get_sensor_status').on('click', submitGetSensorsStatus);

};
submitGetSensorsStatus = function () {
    var request = {};
    request['request_id'] = 7;
    request['cmd'] = 'get_sensors_status';
    var selects = document.getElementById('modal_get_sensor_relay_status').getElementsByTagName('select');

    for(i = 0; i < selects.length; i++) {
        request[selects[i].id] = $(selects[i]).val();
    }


    var result = $.post('/insert_request', JSON.stringify(request));
    result.done(triggador);
    $('#modal_get_sensor_relay_status').modal('hide');
    historicList("Get Sensors requested");
};

clearGetRelaysStatus = function() {
    addDropdownIpwall('#select_ipwall_id_1');
    $('#send_get_sensor_status').on('click', submitGetRelaysStatus);

};
submitGetRelaysStatus = function () {
    var request = {};
    request['request_id'] = 8;
    request['cmd'] = 'get_relays_status';
    var selects = document.getElementById('modal_get_sensor_relay_status').getElementsByTagName('select');

    for(i = 0; i < selects.length; i++) {
        request[selects[i].id] = $(selects[i]).val();
    }


    var result = $.post('/insert_request', JSON.stringify(request));
    result.done(triggador);
    $('#modal_get_sensor_relay_status').modal('hide');
    historicList("Get Relays requested");
};

clearOpenTheDoor = function() {
    addDropdownIpwall('#select_ipwall_id_2');
    $("#door_id").val("");
    console.log('OpenDoor');
    $('#send_open_door').on('click', submitOpenTheDoor);

};
submitOpenTheDoor = function(){
    var request = {};
    request['request_id'] = 9;
    request['cmd'] = 'open_the_door';
    console.log(request);
    var selects = document.getElementById('modal_open_keep_close_door').getElementsByTagName('select');
    var inputs = document.getElementById('modal_open_keep_close_door').getElementsByTagName('input');

    for(i=0; i<selects.length; i++) {
        request[selects[i].id] = $(selects[i]).val();
    }

    for(i=0; i<inputs.length; i++) {
        request[inputs[i].id] = $(inputs[i]).val();
    }
    console.log(request);
    var result = $.post('/insert_request', JSON.stringify(request));
    result.done(triggador);
    $('#modal_open_keep_close_door').modal('hide');
    historicList("Open the Door requested");
};

clearKeepDoorOpened = function () {
    addDropdownIpwall('#select_ipwall_id_2');
    $("#door_id").val("");
    $('#send_open_door').on('click', submitKeepDoorOpened);
};
submitKeepDoorOpened = function(){
    var request = {};
    request['request_id'] = 10;
    request['cmd'] = 'keep_door_opened';
    var selects = document.getElementById('modal_open_keep_close_door').getElementsByTagName('select');
    var inputs = document.getElementById('modal_open_keep_close_door').getElementsByTagName('input');

    for(i=0; i<selects.length; i++) {
        request[selects[i].id] = $(selects[i]).val();
    }

    for(i=0; i<inputs.length; i++) {
        request[inputs[i].id] = $(inputs[i]).val();
    }
    console.log(request);
    var result = $.post('/insert_request', JSON.stringify(request));
    result.done(triggador);
    $('#modal_open_keep_close_door').modal('hide');
    historicList("Keep the Door Opened requested");
};

clearCloseTheDoor = function () {
    addDropdownIpwall('#select_ipwall_id_2');
    $("#door_id").val("");
    $('#send_open_door').on('click', submitCloseTheDoor);
};
submitCloseTheDoor = function(){
    var request = {};
    request['request_id'] = 11;
    request['cmd'] = 'close_the_door';
    var selects = document.getElementById('modal_open_keep_close_door').getElementsByTagName('select');
    var inputs = document.getElementById('modal_open_keep_close_door').getElementsByTagName('input');

    for(i=0; i<selects.length; i++) {
        request[selects[i].id] = $(selects[i]).val();
    }

    for(i=0; i<inputs.length; i++) {
        request[inputs[i].id] = $(inputs[i]).val();
    }
    console.log(request);
    var result = $.post('/insert_request', JSON.stringify(request));
    result.done(triggador);
        historicList("Close the Door requested");


};

changeLogType = function() {
    var request = {};
    request['request_id'] = 17;
    request['type'] = $("#select_log_type").val();
    var result = $.post('/insert_request', JSON.stringify(request));
    result.done(triggador);
    historicList("Change Log Type requested")
};

showRequest = function( request ){
    console.log(request);
    div_principal = $('#show-request');
    div = $('<div>',{
        class: 'panel panel-primary',
        style: 'margin-bottom: 5px'
    });

    div_heading = $('<div>',{
        class: 'panel-heading',
        id: 'cabecalho' + request
    });

    div_heading.append('Request: ' + request.cmd);
    div.append(div_heading);

    div_principal.append(div);
};

var requestCount = 0;

submitPing = function(){
    console.log("PING-1");
    var request = {};
    request['request_id'] = 1;
    request['cmd'] = 'ping';

    console.log(request);
    var result = $.post('/insert_request', JSON.stringify(request));
    result.done(triggador);
    historicList("Ping requested");
};

triggador = function(){
    $('#button-menu-request-2').trigger('click');
};

submitDatetime = function(){
    var request ={};
    request['request_id'] = 2;
    request['cmd'] = 'set_datetime';
    console.log(request);
    var result = $.post('/insert_request', JSON.stringify(request));
    result.done(triggador);
        historicList("Datetime requested");


};

submitVacuum = function(){
    var request ={};
    request['request_id'] = 3;
    request['cmd'] = 'vacuum_db';
    console.log(request);
    var result = $.post('/insert_request', JSON.stringify(request));
    result.done(triggador);
        historicList("Vacuum requested");

};

startEmergency = function(){
    var request ={};
    request['request_id'] = 4;
    request['cmd'] = 'start_emergency';
    console.log(request);
    var result = $.post('/insert_request', JSON.stringify(request));
    result.done(triggador);
        historicList("Start Emergency requested");

};

stopEmergency = function(){
    var request ={};
    request['request_id'] = 5;
    request['cmd'] = 'stop_emergency';
    console.log(request);
    var result = $.post('/insert_request', JSON.stringify(request));
    result.done(triggador);
            historicList("Stop Emergency requested");

};

// *************
// *** BEHAVE ***
// *************
showBehave = function() {
    console.log('showBehave');
    $('#button-confirm-behave').on('click', function(){
        startBehave();
    });
};

startBehave = function(){
    var done = null;
    var div = null;
    var div_body = null;
    var txt = "";
    var string = "";
    console.log('behave start');
    var result = $.getJSON('/get_behave', function(data){
        console.log(data.result);
        for(i = 0; i < data.result.length; i++) {
            if (String(data.result[i]).includes('@')){
                txt = txt + "<tr> <td> <b>"+ data.result[i] + "</b> </td> </tr>";
            }else{
                txt = txt + "<tr> <td>"+ data.result[i] + "</td> </tr>";
            }

        }
        string = "<table class='table table-striped'><thead><tr><th>Result</th></tr></thead><tbody>"+ txt +"</tbody></table>";
        $("#result_behave").empty()
        $("#result_behave").append(string);

    });
};

// *************
// *** LOGS ***
// *************

downloadLogFile = function() {
    var input = $("#log_file").val();
    var request = {};
    request['request_id'] = 15;
    request['file_name'] = input;
    $.post('/insert_request', JSON.stringify(request));
    console.log(request);

};
showLogs = function() {
    $('#button_log_file').on('click', function(){
        downloadLogFile();
    });
};

setConnection = function(check) {
  var params = {};
  // console.log(localStorage.getItem('connection'));
  params['check'] = check;
  params['protocol'] = $('#protocol').val();
  $.post('/connection', JSON.stringify(params))
  .done(function(){
    // alert("Conexao estabelecida");
  });
};

jQuery(function($) {
    // ***************
    // *** IP WALL ***
    // ***************

    $('#menu-principal-2').hide();

    $('#button-menu-ipwall').on('click', function(){
        div = { data: {name: '#div-menu-ipwall'}};
        $('#show-ipwall').empty();
        done = function(data){
            if (data.result.length === 0){
                $('#div-no-ipwall').show();
                $('#div-yes-ipwall').hide();
            }else{
                $('#div-no-ipwall').hide();
                $('#div-yes-ipwall').show();
                $.each(data.result, function(key, ipwall){
                    showIpwall(ipwall);
                });
            }
        };
        $.getJSON('/get_ipwalls', done);
        show_div(div);
    });

    $('#button-menu-ipwall-2').on('click', function() {
        $('#button-menu-ipwall').trigger('click');
    });

    $('#div-yes-ipwall').hide();

    $('#button_insert_ipwall').on('click', function(){
        $('#breadcrumb_insertIpWall').text("Insert IP Wall");
        $('#title_insert_ipwall').text("Insert IP Wall");
        clearIpWall();
        div = {
            data:{
                name: '#div-insert-ipwall'
            }
        };
        show_div(div);
    });

    $('#button_insert_ipwall2').on('click', function(){
        $('#button_insert_ipwall').trigger('click');
    });

    $('#form_ipwall').submit( function(){ return; });
    $("#check_control_doors").on("click", showOptionDoors);
    $("#check_door_dependency1").on("click", {id: "1"}, showDoorDependency);
    $("#check_door_dependency2").on("click", {id: "2"}, showDoorDependency);
    $("#delete_all_ipwalls").on("click", deleteAllIpwalls);

    // **************
    // *** SET RF ***
    // **************

    $('#button-menu-rf').on('click', function(){
        div = { data: {name: '#div-menu-rf'}};
        $('#show_rf').empty();
        done = function(data){
            if (data.result.length === 0){
                $('#div_no_rf').show();
                $('#div_yes_rf').hide();
            }else{
                $('#div_no_rf').hide();
                $('#div_yes_rf').show();
                $.each(data.result, function(key, rf){
                    showSetRf(rf);
                });
            }
        };
        $.getJSON('/get_rfs', done);
        show_div(div);
    });

    $('#button-menu-rf-2').on('click', function() {
        $('#button-menu-rf').trigger('click');
    });

    $('#button_insert_rf').on('click', function(){
        $('#breadcrumb_insertSetRF').text("Insert Set RF");
        $('#title_insert_rf').text("Insert Set RF");
        clearSetRf();
        addDropdownInsertSetRf();
        div = {
            data: {
                name: '#div-insert-set-rf'
            }
        };
        show_div(div);
    });

    $('#button_insert_rf2').on('click', function(){
        $('#button_insert_rf').trigger('click');
    });

    $('#form_rf').submit( function(){ return; });
    $('#div_yes_rf').hide();
    $('.EditRf').on('click', showSetRfEdit);
    $("#delete_all_rf").on("click", deleteAllSetRf);

    // ************
    // *** USER ***
    // ************

    $('#button-menu-user').on('click', function(){
        div = { data: {name: '#div-menu-user'}};
        $('#show_user').empty();
        done = function(data){
            console.log("RETURN "+data.result);
            if (data.result.length === 0){
                $('#div_no_user').show();
                $('#div_yes_user').hide();
            }else{
                $('#div_no_user').hide();
                $('#div_yes_user').show();
                $.each(data.result, function(key, user){
                    showUser(user);
                });
            }
        };
        $.getJSON('/get_users', done);
        show_div(div);
    });

    $('#button-menu-user-2').on('click', function() {
        $('#button-menu-user').trigger('click');
    });

    $('#button_insert_user').on('click', function(){
        $('#breadcrumb_insertUser').text("Insert User");
        $('#title_insert_user').text("Insert User");
        clearUser();
        addDropdownRfIdInsertUser();
        addIpwallCheckList("div_ipwall_access_tag", "user");
        div = {
            data: {
                name: '#div-insert-user'
            }
        };
        show_div(div);
      });

    $('#button_insert_user2').on('click', function(){
        $('#button_insert_user').trigger('click');
    });

    $('#form_user').submit( function(){ return; });
    $('#days_of_week').hide();
    $("#check_restrict_access").on("click", showRestrictAccess);
    $('.EditUser').on('click', showUserEdit);
    $("#delete_all_users").on("click", deleteAllUsers);

    // ***************
    // *** QR CODE ***
    // ***************

    $('#button-menu-qrcode-reader').on('click', function(){
        div = { data: {name: '#div-menu-qrcode-reader'}};
        $('#show-qrcode-reader').empty();
        done = function(data){
            if (data.result.length === 0){
                $('#div_no_qrcode_reader').show();
                $('#div_yes_qrcode_reader').hide();
            }else{
                $('#div_no_qrcode_reader').hide();
                $('#div_yes_qrcode_reader').show();
                $.each(data.result, function(key, qrcode_reader){
                    showQrcodeReader(qrcode_reader);
                });
            }
        };
        $.getJSON('/get_qrcode_readers', done);
        show_div(div);
    });

    $('#button-menu-qrcode-reader-2').on('click', function(){
        $('#button-menu-qrcode-reader').trigger('click');
    });

    $('#button_insert_qrcode_reader').on('click', function(){
        $('#breadcrumb_insertQrcodeReader').text("Insert QR Code Reader");
        $('#title_insert_qrcode_reader').text("Insert QR Code Reader");
        clearQrcodeReader();
        divRelation();
        div = {
            data:{
                name: '#div-insert-qrcode-reader'
            }
        };
        show_div(div);
    });

    $('#button_insert_qrcode_reader2').on('click', function(){
        $('#button_insert_qrcode_reader').trigger('click');
    });

    $('#form_qrcode_reader').submit( function(){ return; });
    $("#delete_all_qrcode_readers").on("click", deleteAllQrcodeReaders);

    // ***************
    // *** GUEST ***
    // ***************

    $('#button-menu-guest').on('click', function(){
        div = { data: {name: '#div-menu-guest'}};
        $('#show-guest').empty();
        done = function(data){
            if (data.result.length === 0){
                $('#div_no_guest').show();
                $('#div_yes_guest').hide();
            }else{
                $('#div_no_guest').hide();
                $('#div_yes_guest').show();
                $.each(data.result, function(key, guest){
                    showGuest(guest);
                });
            }
        };
        $.getJSON('/get_guests', done);
        show_div(div);
    });

    $('#button-menu-guest-2').on('click', function(){
        $('#button-menu-guest').trigger('click');
    });

    $('#button_insert_guest').on('click', function(){
        $('#breadcrumb_insertGuest').text("Insert Guest");
        $('#title_insert_guest').text("Insert Guest");
        addIpwallCheckList("div_ipwall_access_list", "guest");
        clearGuest();
        div = {
            data:{
                name: '#div-insert-guest'
            }
        };
        show_div(div);
    });

    $('#button_insert_guest2').on('click', function(){
        $('#button_insert_guest').trigger('click');
    });

    $('#delete_all_guests').on('click', deleteAllGuests);

    // ***************
    // *** REQUEST ***
    // ***************

    $('#button-menu-request').on('click', function(){
        div = { data: {name: '#div-menu-request'}};
        //selectIpWall();
        $('#show-request').empty();
        done = function(data){
            if (data.result.length === 0){
                $('#div_no_request').show();
                $('#div_yes_request').hide();
            }else{
                $('#div_no_request').hide();
                $('#div_yes_request').show();
                $.each(data.result, function(key, request){
                    console.log('chama request');
                    showRequest(request);
                });
            }
        };
        $.getJSON('/get_requests', done);
        show_div(div);
    });

    $('#button-menu-request-2').on('click', function(){
        $('#button-menu-request').trigger('click');
    });

    $('#request_id').hide();

    $('#button-get-sensors-status').on('click', function(){
        $('#title_get_sensor_relay_status').text(" Get Sensors Status ");
    });
    $('#button-get-relays-status').on('click', function(){
        $('#title_get_sensor_relay_status').text(" Get Relays Status ");
    });
    $('#button-open-door').on('click', function(){
        $('#title_open_keep_close_door').text(" Open The Door ");
    });
    $('#button-keep-door-opened').on('click', function(){
        $('#title_open_keep_close_door').text(" Keep The Door Opened");
    });
    $('#button-close-door').on('click', function(){
        $('#title_open_keep_close_door').text(" Close The Door ");
    });

    $("#button-update-cpu").on("click", clearUpdateCPU);
    $("#button-update-ipwall").on("click", clearUpdateIpwall);
    $("#button-reset-ipwall").on("click", clearResetIpwall);
    $("#button-get-sensors-status").on("click", clearGetSensorsStatus);
    $("#button-get-relays-status").on("click", clearGetRelaysStatus);
    $("#button-open-door").on("click", clearOpenTheDoor);
    $("#button-keep-door-opened").on("click", clearKeepDoorOpened);
    $("#button-close-door").on("click", clearCloseTheDoor);

    $("#send_change_log_type").on("click", changeLogType);
    $('#button-ping').on('click', submitPing);
    $('#button-set-datetime').on('click', submitDatetime);
    $('#button-start-emergency').on('click', startEmergency);
    $('#button-stop-emergency').on('click', stopEmergency);
    $('#button-vacuum-db').on('click', submitVacuum);
    $('#send_flush').on('click', submitFlush);

    // *************
    // *** LOGS ***
    // *************

    $('#button-menu-logs').on('click', function() {
        div = { data: {name: '#div-menu-logs'}};
        $('#show-logs').empty();
        showLogs();
        done = function(data){
            if (data.result.length === 0){
                $('#div_no_logs').show();
                $('#div_yes_logs').hide();
            }else{
                $('#div_no_logs').hide();
                $('#div_yes_logs').show();
                $.each(data.result, function(key, logs) {
//                    showLogs();
                });
            }
        };
//        $.getJSON('/get_logs', done);
        show_div(div);
    });

    $('#button-menu-logs-2').on('click', function() {
        $('#button-menu-logs').trigger('click');
    });

    // *************
    // *** BEHAVE ***
    // *************

    $('#button-menu-behave').on('click', function() {
        div = { data: {name: '#div-menu-behave'}};
        $('#show-behave').empty();
        showBehave();
        done = function(data){
            console.log(data);
            if (data.result.length === 0){
                $('#div_no_behave').show();
                $('#div_yes_behave').hide();
                console.log('button_behave2');
            }else{
                $('#div_no_behave').hide();
                $('#div_yes_behave').show();
                console.log('button_behave');
                $.each(data.result, function(key, behave){
//                    showBehave();
                });
            }
        };
//        $.getJSON('/get_behaves', done);
        show_div(div);
    });

    $('#button-menu-behave-2').on('click', function() {
        $('#button-menu-behave').trigger('click');
    });

    $('#connection').on('click', function() {
      // console.log('Check: '+$('#connection').prop('checked'));
      // if ($('#connection').prop('checked') === false){
      //       localStorage.setItem('connection', false);
      // }
      // else if ($('#connection').prop('checked') === true){
      //       localStorage.setItem('connection', true);
      // }
        setConnection($('#connection').prop('checked'));
    });
    var done = function(data) {
      console.log(data.result);
      $('#connection').prop('checked', data.result.connection);
    }
    $.getJSON('/itsalive', done);
    // $(document).ready(function() {
    //   console.log('Connection: '+localStorage.getItem('connection'));
    //   if(localStorage.getItem('connection') === false){
    //         $('#connection').prop('checked', false);
    //   }
    //   else if(localStorage.getItem('connection') === true){
    //           console.log('Entrou aqui');
    //           $('#connection').prop('checked', true);
    //   }
    // });
    $('#send_update_ipwall').on('click', submitUpdateIpwall);


});
hide_all_div();
