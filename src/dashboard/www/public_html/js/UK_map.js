import * as _utils from './utils.js?version=2.3'
import * as _quartile from './quartile.js?version=1'
import * as _ImageFromRGB from './createImageFromRGBdata.js?version=1'

function sort_unique(arr) {
  if (arr.length === 0) return arr;
  arr = arr.sort(function (a, b) { return a*1 - b*1; });
  var ret = [arr[0]];
  for (var i = 1; i < arr.length; i++) { //Start loop at 1: arr[0] can never be a duplicate
    if (arr[i-1] !== arr[i]) {
      ret.push(arr[i]);
    }
  }
  return ret;
}

export function getPaletteUKMap(data, palette_colors) {
    
let vls = [];
let cnt = 0;
for (var key in data) {
    
//    for (var value in data[key]) {
//       //console.log(data[key][value]);
//       cnt = cnt + data[key].postcode_total ;
//    }
           vls.push(
                data[key].postcode_total   
            );
           cnt = 0;
       
}
  //console.log(sort_unique(breaks));  
    vls.sort(function(a, b) {
        return a - b;
    });
    let all_count = (vls);
     console.log(all_count);         
    let breaks = [];
    let cont = 1;
    let Quartile;
    for (var i = 0; i < palette_colors.length; i++) {
       Quartile = Math.round(_quartile.Quartile(all_count, cont*0.1));
        if (i === 0){
            breaks.push(
                Quartile  
            );         
        }else{
            breaks.push(
                Quartile   
            );         
        } 
        
        cont++;
    }  
    
    let palette = {"breaks":breaks, "colors":palette_colors};

    return palette;
 
}

export function RestyleLayerUKMap(_layer, palette) {
    
    let propertyName = "institutions_count";
    let Opacity = 0.8; 
        
    _layer.eachLayer(function(featureInstanceLayer) {
       var propertyValue = featureInstanceLayer.feature.properties[propertyName];
        

        if (propertyValue == undefined || propertyValue == null) {
            
            featureInstanceLayer.setStyle({
                fillColor: "#EBEBE4",
                fillOpacity: 0,
                color: "#EBEBE4",
                weight: 0
            });           
        }else{

            var mFillColor = _utils.getColor(propertyValue, palette);
            featureInstanceLayer.setStyle({
                fillColor: mFillColor,
                fillOpacity: Opacity,
                color: "black",
                weight: 0.5
            });
        }
        
        
    });
}


export function loadLagentUKMap(title, colors, breaks, subtitles) {

    var html = '<div style="width:60px"><p>' + title + '</p></div>';
    
    var subtitlesArray = Array(colors.length).fill('');
    subtitlesArray[0] = subtitles[0];
    subtitlesArray[colors.length-1] = subtitles[1];    
    
//    html += '<div style="width:100px">' + subtitles[0] + '</div>';
    
    html += '<ul style="list-style-type: none;margin-top: 2px;margin-bottom: 2px;padding-inline-start: 10px;">';
    for (var i = 0, len = colors.length; i < len; i++) {
        var rgb = _ImageFromRGB.hexToRGB(colors[i]);
        var mCanvas = _ImageFromRGB.createImageFromRGBdata(rgb.r, rgb.g, rgb.b, 20, 20);

        html += '<li><img width="16px" height="16px" src="' + mCanvas.toDataURL() + '"><span>&#32;&#32;&#32;&#32; &nbsp;&nbsp;' + breaks[i] + '</span></li>';
    }
    html += '</ul>';
//    html += '<div style="width:100px">' + subtitles[1] + '</div>';
    document.getElementById('legend_UKmap_info').innerHTML = html;

}

export function updateUKMap(_map, _layer, geoJson, data, palette_colors) {
    
    _layer.clearLayers();

   _map.removeLayer(_layer);

    for (var i = 0; i < geoJson.features.length; i++) {
	
           geoJson.features[i].properties.institutions_count = null;
           geoJson.features[i].properties.institutions = null;
                
            var pc_area = geoJson.features[i].properties.pc_area;
	    var res = data[pc_area];
            let cnt = 0;
            
            if (res){
//                    for (var key in res) {
//                        cnt=cnt+res[key];
//                    }
                geoJson.features[i].properties.institutions_count = res.postcode_total;
                geoJson.features[i].properties.institutions = res.institution_counts;
            }else{
                geoJson.features[i].properties.institutions_count = null;
                geoJson.features[i].properties.institutions = null;
            }

    }

//   result = geoJson.filter(val => val.institutions_count !== null);
  
//    $(geoJson.features).each(function (key, data_g) {
//                _layer.addData(data_g);
//    });

   _layer.addTo(_map);
   _layer.addData(geoJson);     
    
    let palette  = getPaletteUKMap(data, palette_colors);

    RestyleLayerUKMap(_layer, palette);
    
    loadLagentUKMap("Counts", palette["colors"], palette["breaks"], "subtitles");
    
    const resizeObserver = new ResizeObserver(() => {
        _map.invalidateSize();
    });

    resizeObserver.observe(document.getElementById("map_uk"));
}



export function resethighlightFeatureUKMap(e, _infoBox, _map) {


    var layer = e.target;
    
    if (_map) {
       
       let institutions = layer.feature.properties.institutions;
       
       if (institutions != undefined || institutions != null) {
           
        layer.setStyle({
            weight: 0.5,
            fillOpacity: 0.8
        });
    
        _infoBox.remove(_map);
       }

    }      

}

export function highlightFeatureUKMap(e, _infoBox, _map) {


    var layer = e.target;
    
    if (_map) {
       
       let institutions = layer.feature.properties.institutions;
       
       if (institutions != undefined || institutions != null) {
           
        layer.setStyle({
            weight: 1,
            fillOpacity: 1
        });
    
        _infoBox.addTo(_map);
        let  html = '<ul style="list-style-type: none;margin-top: 2px;margin-bottom: 2px;padding: 4px;">';
        for (var key in institutions) {
            html += '<li>&check; ' + key+ ': '+institutions[key]+'</li>';
        }
        html += '</ul>';
        document.getElementById('infoBoxUKmap_info').innerHTML = html;   
       }

    }      
    
    
}

