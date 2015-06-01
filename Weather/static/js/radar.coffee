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
  # base map will not draw roads and cities
  map = new google.maps.Map document.getElementById("radar"), {
    zoom: 8
    maxZoom: 10
    minZoom: 4
    mapTypeId: google.maps.MapTypeId.ROADMAP
    navigationControl: true
    center: new google.maps.LatLng 38.885425, -99.317830
    styles: [
      {featureType: 'all', stylers: [{visibility: 'on'}]},
      {featureType: 'administrative', stylers: [{visibility: 'off'}]},
      {featureType: 'road', stylers: [{visibility: 'off'}]}
    ]
  }

  buildLayer = (layer) ->
    mapType = new google.maps.ImageMapType {
      alt: layer.name
      name: layer.name
      credit: layer.credit
      minZoom: 4
      maxZoom: 10
      getTileUrl: (coord, zoom) ->
        proj = map.getProjection()
        zfactor = Math.pow 2, zoom
        top = proj.fromPointToLatLng new google.maps.Point(coord.x * 256 / zfactor, coord.y * 256 / zfactor)
        bot = proj.fromPointToLatLng new google.maps.Point((coord.x + 1) * 256 / zfactor, (coord.y + 1) * 256 / zfactor)
        bbox = top.lng() + "," + bot.lat() + "," + bot.lng() + "," + top.lat()

        url = layer.url
        url += "&BBOX=" + bbox
        url += "&TIME=" + ISOdate
        return url

      isPng: true,
      tileSize: new google.maps.Size layer.width, layer.height
    }

    map.overlayMapTypes.push mapType
    return layer.name

  layerNames = (buildLayer layer for layer in window.wms_overlays)

  # top layer will draw roads and cities over all overlays
  toplevelLayer = new  google.maps.StyledMapType [
    {featureType: 'all', stylers: [{visibility: 'off'}]},
    {featureType: 'road', stylers: [{visibility: 'on'}]},
    {featureType: 'administrative', stylers: [{visibility: 'on'}]}
  ], {name: 'abc'}

  map.overlayMapTypes.push toplevelLayer
