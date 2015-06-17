id2div = (id) ->
  id.split('.').join('::')
  
div2id = (div) ->
  div.split('::').join('.')
  

graph = (station, sensor) ->
  start = $("#start-date").datepicker "getDate"
  end = $("#end-date").datepicker "getDate"
  $("#graphs").append $("<div id="+station+"::"+sensor+"></div>")

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

$ ->
  $('#update-btn').click ->
    $("#graphs").empty()
    tree = $.jstree.reference('#sidebar-panel')
    selected = tree.get_selected()
    graph station, sensor for [station, sensor] in selected
  
  # initial checking of checkboxes that are on by default
  $('#sidebar-panel').on 'ready.jstree', (e, data) ->
    nodes = [station + '.' + sensor for [station, sensor] in window.sensorList]
    tree = $.jstree.reference '#sidebar-panel'
    tree.select_node nodes
    
  $('#sidebar-panel').on 'changed.jstree', (e, data) ->
    update = (id) ->
      [station, sensor] = id.split "."
      
      # if not found we need to add it
      if $("#graphs #"+station+"\\:\\:"+sensor).length == 0
        graph station, sensor
    
    clean = (cld) ->
      if $.inArray(div2id(cld.id), data.selected) == -1
        cld.remove()
    
    # remove all unselected graphs
    cldrn = $("#graphs").children()
    clean cld for cld in cldrn
        
    update id for id in data.selected