import * as _utils from './utils.js?version=2.3'
import * as _quartile from './quartile.js?version=1'
import * as _ImageFromRGB from './createImageFromRGBdata.js?version=1'

function sort_unique(arr) {
  if (arr.length === 0) return arr;
  arr = arr.sort(function (a, b) { return a*1 - b*1; });
  var ret = [arr[0]];
  for (var i = 1; i < arr.length; i++) { 
    if (arr[i-1] !== arr[i]) {
      ret.push(arr[i]);
    }
  }
  return ret;
}

function onlyUnique(value, index, array) {
  return array.indexOf(value) === index;
}

function uniqueArray2(arr) {
    var a = [];
    for (var i=0, l=arr.length; i<l; i++)
        if (a.indexOf(arr[i]) === -1 && arr[i] !== '')
            a.push(arr[i]);
    return a;
}

export function getPaletteUKMap_deprecated(data, palette_colors) {
    
let vls = [];
let cnt = 0;
for (var key in data) {

           vls.push(
                data[key].postcode_total   
            );
           cnt = 0;
       
}
    
    vls.sort(function(a, b) {
        return a - b;
    });
    let all_count = (vls);
            
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

export function getPaletteUKMap(data, palette_colors) {
    
let vls = [];
let cnt = 0;
for (var key in data) {

           vls.push(
                data[key].postcode_total   
            );
           cnt = 0;
       
}
  
    vls.sort(function(a, b) {
        return a - b;
    });
    let all_count = (vls);
       
    let breaks = [];
    let cont = 1;
    let Quartile;
    
    for (var i = 0; i < 10; i++) {
       Quartile = Math.round(_quartile.Quartile(all_count, cont*0.1));
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

    var html = '<div style="width:80px"><p>' + title + '</p></div>';
    
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

    document.getElementById('legend_UKmap_info').innerHTML = html;

}




export function updateUKMap(_map, _layer, geoJson, data, palette_colors) {
    
   _layer.clearLayers();
   _map.removeLayer(_layer);
    let cnt = 0;
    for (var i = 0; i < geoJson.features.length; i++) {
	
           geoJson.features[i].properties.institutions_count = null;
           geoJson.features[i].properties.institutions = null;
                
            var pc_area = geoJson.features[i].properties.pc_area;
	    var res = data[pc_area];
            
            
            if (res){
                geoJson.features[i].properties.institutions_count = res.postcode_total;
                geoJson.features[i].properties.institutions = res.institution_counts;
                cnt=cnt+res.postcode_total;
            }else{
                geoJson.features[i].properties.institutions_count = null;
                geoJson.features[i].properties.institutions = null;
            }

    }


   _layer.addTo(_map);
   _layer.addData(geoJson); 
   
   // document.getElementById('Institutions_count').innerHTML = cnt;
   
    _utils.removeSelectedLayer(_map, "institutions");
    
    let palette  = getPaletteUKMap(data, palette_colors);

    RestyleLayerUKMap(_layer, palette);
    
    loadLagentUKMap("Submissions", palette["colors"], palette["breaks"], "subtitles");
    
    const resizeObserver = new ResizeObserver(() => {
        _map.invalidateSize();
    });

    resizeObserver.observe(document.getElementById("map_uk"));
    
    
}

export function reseAllFeatureUKMap(_map) {

    if (_map) {

        _map.eachLayer(function (layer) {
            if (layer.feature) {

                let institutions = layer.feature.properties.institutions;

                if (institutions != undefined || institutions != null) {

                    layer.setStyle({
                        weight: 0.5,
                        fillOpacity: 0.8,
                        color: "black"
                    });

                }
            }
        });
    }
}

export function resethighlightFeatureUKMap(e, _infoBox, _map, slc_postcode_area) {


    var layer = e.target;
    
    if (_map) {
       
        let institutions = layer.feature.properties.institutions;
            
            if (institutions != undefined || institutions != null) {
           
                let pc_area=layer.feature.properties.pc_area; 
                
                if (pc_area !== slc_postcode_area) {
                    
                    layer.setStyle({
                        weight: 0.5,
                        fillOpacity: 0.8,
                        color: "black"
                    });
    
                    _infoBox.remove(_map);

                }
            }
    }      
}

export function highlightFeatureUKMap(e, _infoBox, _map, slc_postcode_area) {


    var layer = e.target;

    if (_map) {

        let institutions = layer.feature.properties.institutions;

        if (institutions != undefined || institutions != null) {

            let pc_area = layer.feature.properties.pc_area;

            if (pc_area !== slc_postcode_area) {

                layer.setStyle({
                    weight: 1,
                    fillOpacity: 1,
                    color: "black"
                });

                _infoBox.addTo(_map);
                let  html = '<p style="margin-top: 2px;margin-bottom: 2px;padding: 2px;">Submissions from postcode area: <b>' + pc_area + '</b></p>';
                html += '<ul style="list-style-type: none;margin-top: 2px;margin-bottom: 2px;padding: 4px;">';
                for (var key in institutions) {
                    html += '<li>&check; ' + key + ': ' + institutions[key] + '</li>';
                }
                html += '</ul>';
                document.getElementById('infoBoxUKmap_info').innerHTML = html;
            }
        }
    }
}


export function selectFeatureUKMap(e, _infoBox, _map) {


    var layer = e.target;
    
    if (_map) {
        
       let popover_text=''; 
       
       let institutions = layer.feature.properties.institutions;
       
       if (institutions != undefined || institutions != null) {
        
        let pc_area=layer.feature.properties.pc_area;    
            
        layer.setStyle({
            weight: 3,
            fillOpacity: 1,
            color: "green"
        });
    
        _infoBox.addTo(_map);
        
        let popover_text=''; 
        
        let  html = '<p style="margin-top: 2px;margin-bottom: 2px;padding: 2px; color:#0c4128">Selected postcode area: <b>'+pc_area +'</b></p>';
        html += '<ul style="list-style: none;margin-top: 2px;margin-bottom: 2px;padding: 4px;color:#0c4128">';
        for (var key in institutions) {
            html += '<li>&check; ' + key+ ': '+institutions[key]+'</li>';
            popover_text += '&check; ' + key+ '<br/>';
        }
        html += '</ul>';
        
        popover_text += '';
        
        document.getElementById('infoboxSelectedUKmap_info_text').innerHTML = html;   
        $('[data-bs-toggle="tooltip"]').tooltip(); 
        
        
        $('#popover_Institutions').popover('dispose'); 
        // add institutest to label popover in selected option box
        const popover_InstitutionsEl = document.getElementById('popover_Institutions')
        const popover_Institutions = new bootstrap.Popover(popover_InstitutionsEl,{html: true});
    
        popover_Institutions._config.content = popover_text;
        popover_Institutions.setContent();   
        popover_Institutions.enable();        
        
       }
    }      
}

export function getListInstitutionsByCode(e) {

       var layer = e.target;
  
       let institutions = layer.feature.properties.institutions;
       
       if( typeof institutions === 'undefined' || institutions === null ){
           return(institutions);
       }else{
           return(null);
       }      
}