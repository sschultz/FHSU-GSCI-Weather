$ ->
  makeImgTag = (src) ->
    dis = $('#display')
    img = $ '<img/>'
    img.prop 'src', src
    dis.append img
  
  makeImgTag "http://radar.weather.gov/ridge/Overlays/Topo/Long/DDC_Topo_Long.jpg"
  makeImgTag "http://radar.weather.gov/ridge/RadarImg/NCR/DDC_NCR_0.gif"
  makeImgTag "http://radar.weather.gov/ridge/Warnings/Long/DDC_Warnings_0.gif"
  makeImgTag "http://radar.weather.gov/ridge/Overlays/County/Long/DDC_County_Long.gif"
  makeImgTag "http://radar.weather.gov/ridge/Overlays/Cities/Long/DDC_City_Long.gif"