addImgTag = (src, cl) ->
  dis = $('#display')
  img = $ '<img/>'
  img.attr 'src', src
  img.attr("class", cl) if cl
  dis.append img

$ ->
  addImgTag "http://radar.weather.gov/ridge/Overlays/Topo/Long/DDC_Topo_Long.jpg"
  
  overlays = [
    "http://radar.weather.gov/ridge/Overlays/Highways/Short/DDC_Highways_Short.gif",
    "http://radar.weather.gov/ridge/RadarImg/NCR/DDC_NCR_0.gif",
    "http://radar.weather.gov/ridge/Warnings/Long/DDC_Warnings_0.gif",
    "http://radar.weather.gov/ridge/Overlays/County/Long/DDC_County_Long.gif",
    "http://radar.weather.gov/ridge/Overlays/Cities/Long/DDC_City_Long.gif",
    "http://radar.weather.gov/ridge/Legend/NCR/DDC_NCR_Legend_0.gif",
  ]
  
  addImgTag overlay, "overlay" for overlay in overlays