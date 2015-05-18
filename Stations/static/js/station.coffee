$ ->
  update()
  $('#update-btn').click update

update = ->
  start = $("#start-date").datepicker "getDate"
  end = $("#end-date").datepicker "getDate"

  graph = (sensor) ->
    $("#graphs").append $("<div id="+sensor+"></div>")

    #build URL to retrieve station info from webserver
    #url is defined in django template
    url = window.url.replace '999', sensor
    url = url.replace '888', window.curStation

    url += "?start=" + (start.getMonth()+1) + "-" +
            start.getDate() + '-' +
            start.getFullYear()

    url += (end.getMonth()+1) + "-" +
            end.getDate() + '-' +
            end.getFullYear()

    $.getJSON url, (opts) ->
        chart = new Highcharts.Chart(opts)

  graph sensor for sensor in window.sensorList

###
var curStation = '{{selStation.slug}}';
var sensorList = JSON.parse('{{default_sensor_list}}');
$(function() {
    update();
    $('#update-btn').click(update);
});
function update() {
    var start = $("#start-date").datepicker("getDate");
    var end = $("#end-date").datepicker("getDate");
    for (var i in sensorList) {
        $("#graphs").append($("<div id="+sensorList[i]+"></div>"));
        $.getJSON("{% url 'graph-view' '888' '999' %}"
            .replace('999', sensorList[i])
            .replace('888', curStation) +
            "?start=" + (start.getMonth()+1)+"-"+start.getDate()+'-'+start.getFullYear() +
            "&end=" + (end.getMonth()+1)+"-"+end.getDate()+'-'+end.getFullYear(),
            function(opts) {
                var chart = new Highcharts.Chart(opts);
            });
    }
}
###