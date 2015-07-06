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

  $('#sidebar-handle').click ->
    $('#sidebar-panel').animate {width: "toggle"}, "slow", "swing", ->
      if $('#sidebar-panel').css('display') == 'none'
        $('#sidebar-handle').html '<table><tr><td>&gt;&gt;</td></tr></table>'
      else
        $('#sidebar-handle').html '<table><tr><td>&lt;&lt;</td></tr></table>'

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