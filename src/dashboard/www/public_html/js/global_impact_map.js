import * as _utils from './utils.js?version=3'
import * as _quartile from './quartile.js?version=1'
import * as _ImageFromRGB from './createImageFromRGBdata.js?version=1'

export function highlightFeatureGlobalImactMap(e, _map) {

    var layer = e.target;

    layer.setStyle({
        weight: 1,
        fillOpacity: 1
    });
}


export function RestyleLayerGlobalImactMap(_layer, palette) {
    
    let propertyName = "countriy_count";
    let Opacity = 0.8; 
    //console.log(_layer);
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
                featureInstanceLayer.setStyle({
                fillColor: _utils.getColor(propertyValue, palette),
                fillOpacity: Opacity,
                weight: 0.5
            });
        }       
     
    });
}

export function clickGlobalImactMap(e, _mapGlobal, _mapGlobalPopup) {
    
                    if (_mapGlobal) {
                        _mapGlobalPopup
                                .setLatLng(e.latlng)
                                .setContent("<b>"+e.target.feature.properties.country + '</b><br/>Impact factor: '+e.target.feature.properties.countriy_count)
                                .openOn(_mapGlobal);
                    }  
    
}


export function resetHighlightGlobalImactMap(e) {
    
    var layer = e.target;

    layer.setStyle({
        weight: 0.5,
        fillOpacity: 0.8
    });
    
}

export function getPaletteGlobalImactMap(dataCountries_counts, palette_colors) {
    
    let  all_country_count = Object.keys(dataCountries_counts).map(key => dataCountries_counts[key].country_count);

    let breaks = [];
    let cont = 1;
    let Quartile;
    for (var i = 0; i < palette_colors.length; i++) {
       Quartile = Math.round(_quartile.Quartile(all_country_count, cont*0.1));
     
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

export function loadLagentGlobalImactMap(title, colors, breaks, subtitles) {

    var html = '<div style="width:60px"><p>' + title + '</p></div>';
    
    var subtitlesArray = Array(colors.length).fill('');
    subtitlesArray[0] = subtitles[0];
    subtitlesArray[colors.length-1] = subtitles[1];    
    
//    html += '<div style="width:100px">' + subtitles[0] + '</div>';
    
    html += '<ul style="list-style-type: none;margin-top: 2px;margin-bottom: 2px;padding-inline-start: 10px;">';
    for (var i = 0, len = colors.length; i < len; i++) {
        var rgb = _ImageFromRGB.hexToRGB(colors[i]);
        var mCanvas = _ImageFromRGB.createImageFromRGBdata(rgb.r, rgb.g, rgb.b, 20, 20);

        html += '<li><img width="16px" height="16px" src="' + mCanvas.toDataURL() + '"><span>&#32;&#32;&#32;&#32;	&nbsp;&nbsp;' + breaks[i] + '</span></li>';
    }
    html += '</ul>';
//    html += '<div style="width:100px">' + subtitles[1] + '</div>';
    document.getElementById('legend_mapGlobal_info').innerHTML = html;

}


export function updateGlobalImactMap(_map, _layer, geoJson, dataCountries_counts, palette_colors) {
    

   
    _layer.clearLayers();

   _map.removeLayer(_layer);
   
    for (var i = 0; i < geoJson.features.length; i++) {
			
            var iso_a3 = geoJson.features[i].properties.iso_a3;

	    var res = dataCountries_counts.find(e => e.country === iso_a3);
    
            if (res !== undefined && res !== null){
                geoJson.features[i].properties.countriy_count = res.country_count;
            }else{
                geoJson.features[i].properties.countriy_count = null;
                //geoJson[i] = null;
                //delete geoJson[i];                
            }
    }

//    $(geoJson.features).each(function (key, data_g) {
//                _layer.addData(data_g);
//    });
    
//   let result = geoJson.filter(val => val.countriy_count !== null);
   
   _layer.addTo(_map);
   _layer.addData(geoJson);    
    
    
    
    let palette  = getPaletteGlobalImactMap(dataCountries_counts, palette_colors);

    RestyleLayerGlobalImactMap(_layer, palette);
    loadLagentGlobalImactMap("Impact", palette["colors"], palette["breaks"], "subtitles");
    
    //console.log(palette);
    const resizeObserver = new ResizeObserver(() => {
        _map.invalidateSize();
    });

    resizeObserver.observe(document.getElementById("map_global"));
}

