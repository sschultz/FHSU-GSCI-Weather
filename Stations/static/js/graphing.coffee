expand = (evnt) ->
  $('#sidebar-panel').show 0
  $('#sidebar-panel').animate {width: '400px'}

  $('#sidebar-handle').one 'click', shrink
  $('#sidebar-handle').text '<<'

shrink = (evnt) ->
  $('#sidebar-panel').animate {width: '0px'}, 400, "swing", () ->
    $('#sidebar-panel').hide 0
  $('#sidebar-handle').one 'click', expand
  $('#sidebar-handle').text '>>'

$ ->
  Highcharts.setOptions {global: { useUTC: false }}
  start = new Date()
  end = new Date()
  fmt = "yy-mm-dd"

  start.setDate start.getDate() - 2
  $('#start-date').datepicker {dateFormat: "m-d-yy"}

  #format the date and assign it
  $('#start-date').val (start.getMonth()+1) + '-' +
  start.getDate() + '-' +
  start.getFullYear()

  $('#end-date').datepicker {dateFormat: "m-d-yy"}
  $('#end-date').val (end.getMonth()+1) + '-' +
  end.getDate() + '-' +
  end.getFullYear()

  $('#sidebar-panel').hide 0
  $('#sidebar-handle').one 'click', expand
  $.jstree.defaults.core.data = true
  $('#sidebar-panel').jstree {
    plugins : ["themes", "ui", "checkbox"],
    core: {
      data: {
        url:'/station-tree/',
        data: (node) ->
          {id: node.id}
      }
    }
  }