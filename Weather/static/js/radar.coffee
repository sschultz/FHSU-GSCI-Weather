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

# Get latest update period (in minutes) that has past or currently is in UTC time
genMostRecent = (updatePeriod) ->
  date = new Date()
  mins = date.getUTCMinutes()
  date.setUTCMinutes mins - mins % updatePeriod
  date.setUTCSeconds 0
  date.setUTCMilliseconds 0
  return date
  
$ ->
  # print radar time
  latest = genMostRecent(5)
  $(".timestamp").text " " +
    (if latest.getHours() % 12 == 0 then "12" else latest.getHours() % 12) +
    ":" + ('0' + latest.getMinutes()).slice(-2) + " " +
    (if latest.getHours() >= 12 then "PM " else "AM ") +
    (latest.getMonth()+1) + "/" +
    latest.getDate() + "/" +
    latest.getFullYear()

  # base map will not draw roads and cities
  map = new ol.Map {
    target: "radar"
    layers: [
      new ol.layer.Tile {
        source: new ol.source.MapQuest {layer: 'sat'}
      }
    ]
    view: new ol.View {
      center: ol.proj.transform [-99.317830, 38.885425], 'EPSG:4326', 'EPSG:3857'
      zoom: 7
      minZoom: 4
      maxZoom: 12
      extent: ol.proj.transformExtent [-126.428053, 22.447429, -66.266922, 48.962796], 'EPSG:4326', 'EPSG:3857'
      enableRotation: false
    }
  }
  window.map = map
  # Details: http://wiki.openstreetmap.org/wiki/EPSG:3857
  # Spherical Mercator projection coordinate system popularized by web services such as Google and later OpenStreetMap.
  BaseMapProjection = ol.proj.get "EPSG:3857"
  
  buildLayer = (layer) ->
    latest = genMostRecent layer.update
    ISOdate = latest.toISOString()
    
    map.addLayer new ol.layer.Tile {
      source: new ol.source.TileWMS {
        url: layer.url
        params: {
          'LAYERS': layer.layers
          'TIME': ISOdate
        }
        projection: BaseMapProjection
        attributions: [ new ol.Attribution {html: '<p>' + layer.credit + '</p>'} ] if layer.credit
        logo: layer.logo if layer.logo
      }
    }
  buildLayer layer for layer in window.wms_overlays
  
  map.addLayer new ol.layer.Tile {
    source: new ol.source.MapQuest {layer: 'hyb'}
  }
a = 'NEXRAD Composites Courtesy of <a href="http://mesonet.agron.iastate.edu/docs/nexrad_composites/">Iowa State University of Science and Technology</a>'