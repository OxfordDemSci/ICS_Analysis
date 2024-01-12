import * as _utils from './utils.js?version=3'
import * as _quartile from './quartile.js?version=1'
import * as _ImageFromRGB from './createImageFromRGBdata.js?version=1'

function uniqueArray2(arr) {
    var a = [];
    for (var i=0, l=arr.length; i<l; i++)
        if (a.indexOf(arr[i]) === -1 && arr[i] !== '')
            a.push(arr[i]);
    return a;
}

export function highlightFeatureGlobalImactMap(e, _infoBox, _map) {

    var layer = e.target;
    
    if (_map) {
        let country_count = e.target.feature.properties.countriy_count;
        let country = e.target.feature.properties.country;
        if (typeof country_count !== 'undefined' && country_count !== null) {
            layer.setStyle({
                weight: 1,
                fillOpacity: 1
            });
        }
        
        _infoBox.addTo(_map);
        
        let  html = '<p style="margin-top: 2px;margin-bottom: 2px;padding: 4px;"><b>'+e.target.feature.properties.country + '</b><br/>Impact Case Studies: '+e.target.feature.properties.countriy_count+'</p>';
        document.getElementById('infoBoxMapGlobal_info').innerHTML = html;
    }

}


export function RestyleLayerGlobalImactMap(_layer, palette) {
    
    let propertyName = "countriy_count";
    let Opacity = 0.8; 
    _layer.eachLayer(function(featureInstanceLayer) {
    var propertyValue = featureInstanceLayer.feature.properties[propertyName];
        

        if( typeof propertyValue === 'undefined' || propertyValue === null ){
            
//                featureInstanceLayer.setStyle({
//                    fillColor: "#EBEBE4",
//                    fillOpacity: 0,
//                    color: "#EBEBE4",
//                    weight: 0
//                });
            
        }else{
                featureInstanceLayer.setStyle({
                fillColor: _utils.getColor(propertyValue, palette),
                fillOpacity: Opacity,
                weight: 0.5,
                color: "black"
            });
        }       
        
    });
}

export function clickGlobalImactMap(e, _mapGlobal, _mapGlobalPopup) {
               
                let propertyValue = e.target.feature.properties.countriy_count;
             
                if( typeof propertyValue !== 'undefined' && propertyValue !== null ){
                    if (_mapGlobal) {
                        _mapGlobalPopup
                                .setLatLng(e.latlng)
                                .setContent("<b>"+e.target.feature.properties.country + '</b><br/>Beneficiaries: '+e.target.feature.properties.countriy_count)
                                .openOn(_mapGlobal);
                    }  
                }
                
}


export function resetHighlightGlobalImactMap(e, _infoBox, _map) {
    
    var layer = e.target;

    layer.setStyle({
        weight: 0.5,
        fillOpacity: 0.8
    });
    _infoBox.remove(_map);
}

export function getPaletteGlobalImactMap(dataCountries_counts, palette_colors) {
    
    let  all_country_count = Object.keys(dataCountries_counts).map(key => dataCountries_counts[key].country_count);

    let breaks = [];
    let cont = 1;
    let Quartile;

    
    for (var i = 0; i < 10; i++) {
       Quartile = Math.round(_quartile.Quartile(all_country_count, cont*0.1));
       breaks.push(Quartile);
        cont++;  
    }  

    let breaks_unique = uniqueArray2(breaks);

    let palette_final = [];
    let diference = palette_colors.length-breaks_unique.length;
    for (var i = 0; i < breaks_unique.length; i++) {
             palette_final.push(
                    palette_colors[i+diference]
            );
    }  
    let palette = {"breaks":breaks_unique, "colors":palette_final};
   
    return palette;
 
}

export function getPaletteGlobalImactMap_deprecated(dataCountries_counts, palette_colors) {
    
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

    var html = '<div style="width:80px"><p>' + title + '</p></div>';
    
    var subtitlesArray = Array(colors.length).fill('');
    subtitlesArray[0] = subtitles[0];
    subtitlesArray[colors.length-1] = subtitles[1];    
  
    html += '<ul style="list-style-type: none;margin-top: 2px;margin-bottom: 2px;padding-inline-start: 10px;">';
    for (var i = 0, len = colors.length; i < len; i++) {
        var rgb = _ImageFromRGB.hexToRGB(colors[i]);
        var mCanvas = _ImageFromRGB.createImageFromRGBdata(rgb.r, rgb.g, rgb.b, 20, 20);

        html += '<li><img width="16px" height="16px" src="' + mCanvas.toDataURL() + '"><span>&#32;&#32;&#32;&#32;	&nbsp;&nbsp;' + breaks[i] + '</span></li>';
    }
    html += '</ul>';

    document.getElementById('legend_mapGlobal_info').innerHTML = html;

}


export function updateGlobalImactMap(_map, _layer, geoJson, dataCountries_counts, palette_colors) {

    let cnt=0;
    _layer.clearLayers();

   _map.removeLayer(_layer);

    geoJson.countriy_count = null;
    
    for (var i = 0; i < geoJson.features.length; i++) {
			
            var iso_a3 = geoJson.features[i].properties.iso_a3;

	    var res = dataCountries_counts.find(e => e.country === iso_a3);
           
            if (typeof res !== "undefined" && res !== null) {   
                geoJson.features[i].properties.countriy_count = res.country_count;
                cnt=cnt+res.country_count;
            }else{
                geoJson.features[i].properties.countriy_count = null;
            }
    }


   _layer.addTo(_map);
   _layer.addData(geoJson); 
   
   // document.getElementById('Beneficiaries_count').innerHTML = cnt;
    
    _utils.removeSelectedLayer(_map, "countriy_count");
    
    let palette  = getPaletteGlobalImactMap(dataCountries_counts, palette_colors);

    RestyleLayerGlobalImactMap(_layer, palette);
    loadLagentGlobalImactMap("Beneficiaries", palette["colors"], palette["breaks"], "subtitles");

    const resizeObserver = new ResizeObserver(() => {
        _map.invalidateSize();
    });

    resizeObserver.observe(document.getElementById("map_global"));
}


