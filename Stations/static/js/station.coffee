$ ->
  update()
  $('#update-btn').click update
  
  # initial checking of checkboxes that are on by default
  $('#sidebar-panel').on 'ready.jstree', (e, data) ->
    nodes = [station + '::' + sensor for [station, sensor] in window.sensorList]
    tree = $.jstree.reference '#sidebar-panel'
    tree.select_node nodes

update = ->
  start = $("#start-date").datepicker "getDate"
  end = $("#end-date").datepicker "getDate"

  graph = ([station, sensor]) ->
    $("#graphs").append $("<div id="+station+".."+sensor+"></div>")

    #build URL to retrieve station info from webserver
    #url is defined in django template
    url = window.url.replace '999', sensor
    url = url.replace '888', station

    url += "?start=" + (start.getMonth()+1) + "-" +
            start.getDate() + '-' +
            start.getFullYear()

    url += (end.getMonth()+1) + "-" +
            end.getDate() + '-' +
            end.getFullYear()

    $.getJSON url, (opts) ->
        chart = new Highcharts.Chart(opts)

  graph sensor for sensor in window.sensorList