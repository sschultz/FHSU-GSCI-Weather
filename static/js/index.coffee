$ ->
  Highcharts.setOptions {
    global: {useUTC: false}
  }

  $.get "http://localhost:8000/forecast/", (forecast) ->
    headerRow = $ ".ftable .header"
    dayRow = $ ".ftable .day"
    nightRow = $ ".ftable .night"

    format = (period) ->
      #daytime
      if period.start.substring(11,16) is "06:00"
        headerRow.append $("<td>" + period.period + "</td>")
        
        day = ""
        if period.max
          day += "High: " + period.max + "&deg;F</br>"
        if period.precip
          day += "Chance of Rain: " + period.precip + "%</br>"
        if period.conditions
          day += period.conditions + "</br>"

        if period.icon
          day += "<img src=\"" + period.icon + "\"/>"
          
        data = $("<td><p>" + day + "</p></td>")
        dayRow.append(data)
      #nighttime
      else
        night = ""
        if period.min
          night += "Low: " + period.min + "&deg;F</br>"
        if period.precip
          night += "Chance of Rain: " + period.precip + "%</br>"
        if period.conditions
          night += period.conditions + "</br>"

        if period.icon
          night += "<img src=\"" + period.icon + "\"/>"
        
        data = $("<td><p>" + night + "</p></td>")
        nightRow.append(data)
    
    format period for period in forecast.forecast

    source = $ "#source p"
    dt = new Date(forecast.refreshed)
    refreshed = dt.getMonth()+1 + "-" +
      dt.getDate() + "-" +
      dt.getFullYear() + " " +
      (if dt.getHours() % 12 == 0 then "12" else dt.getHours() % 12) +
      ":" + dt.getMinutes() + " " +
      (if dt.getHours() >= 12 then "PM" else "AM")

    source.text "Source: National Weather Service (updated " + refreshed + ")"