pad = (number) ->
  r = String(number)
  if r.length is 1
    r = '0' + r

# Ensure all browsers support Date.toISOString()
if !Date.prototype.toISOString
  Date.prototype.toISOString = ->
    return (this.getUTCFullYear() + '-' + pad this.getUTCMonth() + 1 \
      + '-' + pad this.getUTCDate()
      + 'T' + pad this.getUTCHours()
      + ':' + pad this.getUTCMinutes()
      + ':' + pad this.getUTCSeconds()
      + '.' + String((this.getUTCMilliseconds() / 1000).toFixed 3).slice 2, 5
      +'Z')

# Get nearest 5 minutes that has past or currently is in UTC time
genMostRecent = ->
  date = new Date()
  mins = date.getUTCMinutes()
  date.setUTCMinutes mins - mins % 5
  date.setUTCSeconds 0
  date.setUTCMilliseconds 0
  return date

latest = genMostRecent()
ISOdate = latest.toISOString()

$ ->
  $(".timestamp").text(latest.toString())
  
google.maps.event.addDomListener window, 'load', ->
  NEXRADLayer = new google.maps.ImageMapType {
    getTileUrl: (coord, zoom) ->
      proj = map.getProjection()
      zfactor = Math.pow 2, zoom
      top = proj.fromPointToLatLng new google.maps.Point(coord.x * 256 / zfactor, coord.y * 256 / zfactor)
      bot = proj.fromPointToLatLng new google.maps.Point((coord.x + 1) * 256 / zfactor, (coord.y + 1) * 256 / zfactor)
      bbox = top.lng() + "," + bot.lat() + "," + bot.lng() + "," + top.lat()
      
      url = "http://mesonet.agron.iastate.edu/cgi-bin/wms/nexrad/n0r-t.cgi?"
      url += "REQUEST=GetMap"
      url += "&SERVICE=WMS"
      url += "&VERSION=1.1.1"
      url += "&LAYERS=" + "nexrad-n0r-wmst"
      url += "&TIME=" + ISOdate
      url += "&FORMAT=image/png"
      url += "&BGCOLOR=0xFFFFFF"
      url += "&TRANSPARENT=TRUE"
      url += "&SRS=EPSG:4326"
      url += "&BBOX=" + bbox
      url += "&WIDTH=256"
      url += "&HEIGHT=256"
      return url
    tileSize: new google.maps.Size 256, 256
    isPng: true
  }
  mapOptions = {
    center: {
      lat: 38.885475
      lng: -99.317831
    }
    zoom: 8
    maxZoom: 12
    minZoom: 5
    streetViewControl: false
  }
  map = new google.maps.Map $("#radar")[0], mapOptions
  return map.overlayMapTypes.push NEXRADLayer