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
genMostRecent = (minutes) ->
  date = new Date()
  mins = date.getUTCMinutes()
  date.setUTCMinutes mins - mins % minutes
  date.setUTCSeconds 0
  date.setUTCMilliseconds 0
  return date

google.maps.event.addDomListener window, 'load', ->
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
  
  add_wms_overlay = (overlay) ->
    NEXRADLayer = new google.maps.ImageMapType {
      getTileUrl: (coord, zoom) ->
        proj = map.getProjection()
        zfactor = Math.pow 2, zoom
        
        top = proj.fromPointToLatLng new google.maps.Point(
          coord.x * overlay.width / zfactor,
          coord.y * overlay.height / zfactor
        )
        
        bot = proj.fromPointToLatLng new google.maps.Point(
          (coord.x + 1) * overlay.width / zfactor,
          (coord.y + 1) * overlay.height / zfactor
        )
        
        bbox = top.lng() + "," + bot.lat() + "," + bot.lng() + "," + top.lat()
        
        latest = genMostRecent overlay.update
        ISOdate = latest.toISOString()
        $(".timestamp").text(latest.toString())
        
        url = overlay.url
        #url += "&TIME=" + ISOdate
        return url
      tileSize: new google.maps.Size overlay.width, overlay.height
      isPng: true
      name: overlay.name
    }
    map.overlayMapTypes.push NEXRADLayer
  
  a = add_wms_overlay overlay for overlay in window.wms_overlays
  return a