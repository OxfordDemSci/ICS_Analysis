var API_URL = "http://127.0.0.1:8000/api/";

import * as _api from './api.js?version=2.6'
import * as _init from './init.js?version=4.2'
import * as _utils from './utils.js?version=2.6'
import * as _UOAChart from './uoa_chart.js?version=5.4'
import * as _funderChart from './funder_chart.js?version=3.3'
import * as _GlobalImactMap from './global_impact_map.js?version=3.5'
import * as _UKMap from './UK_map.js?version=5.5'

//window.slc_postcode_area=null;
//window.slc_beneficiary=null;
//window.slc_uoa=null;
//window.slc_topic=null;
//window.slc_threshold=null;

var slc_postcode_area=null;
var slc_beneficiary=null;
var slc_uoa=null;
var slc_topic=null;
var slc_threshold=0.5;
var slc_funder=null;

let palette_colors_GlobalMap = ["#f7fbff", "#e9f2f9", "#deebf7", "#c6dbef", "#9ecae1", "#6baed6", "#4292c6", "#2171b5", "#08519c", "#08306b"];
let palette_colors_UKMap = ["#fff5f0", "#fff5f0", "#fee0d2", "#fcbba1", "#fc9272", "#fb6a4a", "#ef3b2c", "#cb181d", "#a50f15", "#67000d"];


let initialData = _api.getInitData(API_URL);
let GlobalBoundary = _api.getGlobalBoundary();
let UKPostCodeAreasBoundary = _api.getUKPostCodeAreasBoundary();

console.log(initialData);


// base map
var basemaps = {
        "OpenStreetMaps": L.tileLayer(
            "https://cartodb-basemaps-b.global.ssl.fastly.net/light_nolabels/{z}/{x}/{y}.png", {
                attribution: "<a href='http://www.esri.com/'>Esri</a>, HERE, Garmin, (c) OpenStreetMap",
                minZoom: 1,
                maxZoom: 11,
                // noWrap: true,
                id: "osm.streets"
            }
        )
};



//******************************************************************************
// start setting a g lobal map 

var mapGlobalOptions = {
        zoomControl: true,
        attributionControl: false,
        center: [48.864716, 2.349014],
        zoom: 1,
        maxZoom: 11,
        minZoom: 1,
        layers: [basemaps.OpenStreetMaps]
};


var mapGlobal = L.map("map_global", mapGlobalOptions);
var mapGlobalPopup = L.popup({closeButton: false});
var layerGlobal = L.geoJson(null, {
        style: {
            weight: 1,
            color: "#FFFFFF00",
            fillOpacity: 0.9
        },
        onEachFeature: function (feature, layer) {

            layer.on({
                mouseover:  function (e) {
                    _GlobalImactMap.highlightFeatureGlobalImactMap(e, mapGlobal);
                },
                mouseout: function (e) {
                    _GlobalImactMap.resetHighlightGlobalImactMap(e);
                    if (mapGlobalPopup && mapGlobal) {
                        mapGlobal.closePopup(mapGlobalPopup);
                    }                    
                },
                click: function (e) {
                    
                        _GlobalImactMap.clickGlobalImactMap(e, mapGlobal, mapGlobalPopup);

                        slc_beneficiary = e.target.feature.properties.iso_a3;
                        _utils.updateLabelsSelectedOptionsBoxs(slc_postcode_area, slc_beneficiary);
                        _utils.progressMenuOn();
                         slc_topic = _utils.getActiveTopic();
                        _api.get_ics_data(API_URL, 
                                        slc_threshold,
                                        slc_topic,
                                        slc_postcode_area,
                                        slc_beneficiary,
                                        slc_uoa,
                                        slc_funder).then(result => {
                            _UKMap.updateUKMap(mapUK, layerUK, UKPostCodeAreasBoundary, result.institution_counts, palette_colors_UKMap);                    
                            _UOAChart.updateUOAChart(result.uoa_counts);
                            _funderChart.updateFunderChart(result.funders_counts, 20);    
                            _GlobalImactMap.updateGlobalImactMap(mapGlobal, layerGlobal, GlobalBoundary, result.countries_counts, palette_colors_GlobalMap);
                        }).then(() => {
                            _utils.progressMenuOff();
                        }).catch(error => {
                            console.log('In the catch', error);
                        });                     
                }
            });

        }.bind(this)
});
// }).addTo(mapGlobal);
mapGlobal.zoomControl.setPosition('topright');

var legendMapGlobal = L.control({position: 'bottomright'});

legendMapGlobal.onAdd = function (map) {
    var legent_text = "legend ";
    var div = L.DomUtil.create('div', 'legend_mapGlobal');
    div.innerHTML += '<div id="legend_mapGlobal_info"></div>';
    L.DomEvent.disableClickPropagation(div);
    L.DomEvent.disableScrollPropagation(div);
    return div;
};
legendMapGlobal.addTo(mapGlobal);

// end  setting a g lobal map 
//******************************************************************************

//******************************************************************************
// start setting a UK map 

var basemapsUKmap = {
        "OpenStreetMaps": L.tileLayer(
            "https://cartodb-basemaps-b.global.ssl.fastly.net/light_nolabels/{z}/{x}/{y}.png", {
                attribution: "<a href='http://www.esri.com/'>Esri</a>, HERE, Garmin, (c) OpenStreetMap",
                minZoom: 1,
                maxZoom: 11,
                // noWrap: true,
                id: "osm.streets"
            }
        )
};

var mapUKOptions = {
        zoomControl: true,
        attributionControl: false,
        center: [55.464453, -2.956112],
        zoom: 5,
        maxZoom: 11,
        minZoom: 1,
        layers: [basemapsUKmap.OpenStreetMaps]
};


var mapUK = L.map("map_uk", mapUKOptions);

var layerUK = L.geoJson(null, {
        style: {
                fillColor: "#EBEBE4",
                fillOpacity: 0,
                color: "#EBEBE4",
                weight: 0
        },
        onEachFeature: function (feature, layer) {

            layer.on({
                mouseover:  function (e) {
                    //if (slc_postcode_area === undefined || slc_postcode_area === null) {
                       
                        _UKMap.highlightFeatureUKMap(e, infoboxUKmap, mapUK , slc_postcode_area);
                    //}
                },
                mouseout: function (e) {
                    //if (slc_postcode_area === undefined || slc_postcode_area === null) {
                        _UKMap.resethighlightFeatureUKMap(e, infoboxUKmap, mapUK , slc_postcode_area);
                    //}
                },
                click: function (e) {
                         _UKMap.reseAllFeatureUKMap(layerUK);
                         slc_postcode_area = e.target.feature.properties.pc_area;
                         _utils.updateLabelsSelectedOptionsBoxs(slc_postcode_area, slc_beneficiary);
                         infoboxUKmap.remove(mapUK);
                         _UKMap.selectFeatureUKMap(e, infoboxSelectedUKmap, mapUK );
                        _utils.progressMenuOn();
                         slc_topic = _utils.getActiveTopic();
                        _api.get_ics_data(API_URL, 
                                        slc_threshold,
                                        slc_topic,
                                        slc_postcode_area,
                                        slc_beneficiary,
                                        slc_uoa,
                                        slc_funder).then(result => {
                            //_UKMap.updateUKMap(mapUK, layerUK, UKPostCodeAreasBoundary, result.institution_counts, palette_colors_UKMap);                    
                            _UOAChart.updateUOAChart(result.uoa_counts);
                            _funderChart.updateFunderChart(result.funders_counts, 20);    
                            _GlobalImactMap.updateGlobalImactMap(mapGlobal, layerGlobal, GlobalBoundary, result.countries_counts, palette_colors_GlobalMap);
                        }).then(() => {
                            _utils.progressMenuOff();
                        }).catch(error => {
                            console.log('In the catch', error);
                        });                   
                }
            });

        }.bind(this)
}).addTo(mapUK);
mapUK.zoomControl.setPosition('topright');

var infoboxUKmap = L.control({ position: 'topleft' });

infoboxUKmap.onAdd = function (mapUK) {
    this._div = L.DomUtil.create('div', 'infoBoxUKmap'); 
    this._div.innerHTML += '<div id="infoBoxUKmap_info"></div>';
    L.DomEvent.disableClickPropagation(this._div);
    L.DomEvent.disableScrollPropagation(this._div);    
    //this.update();
    return this._div;
};

infoboxUKmap.update = function (props) {
    this._div.innerHTML = '<div id="infoBoxUKmap_info"></div>';
};
infoboxUKmap.addTo(mapUK);
infoboxUKmap.remove(mapUK);



 
 
///
var infoboxSelectedUKmap = L.control({ position: 'bottomleft' });

infoboxSelectedUKmap.onAdd = function (mapUK) {
    this._div = L.DomUtil.create('div', 'infoboxSelectedUKmap'); 
    this._div.innerHTML += '<div id="infoboxSelectedUKmap_info">';
    this._div.innerHTML += '<button type="button" id="Reset_selection_UKmap" class="btn btn-sm btn-circle" data-bs-toggle="tooltip" data-bs-placement="top" data-bs-title="Reset selection"><i class="fa-solid fa-xmark" style="color:#6c757d"></i></button>';
    this._div.innerHTML += '<div id="infoboxSelectedUKmap_info_text"></div>';
    this._div.innerHTML += '</div>';
    
    this._div.addEventListener('click', () => { 
        resetSelectionUKmap(); 
    });    
    L.DomEvent.disableClickPropagation(this._div);
    L.DomEvent.disableScrollPropagation(this._div);   
    
    //this.update();
    return this._div;
};
infoboxSelectedUKmap.update = function (props) {
    this._div.innerHTML = '';
};
infoboxSelectedUKmap.addTo(mapUK);
infoboxSelectedUKmap.remove(mapUK);



var legendUKmap = L.control({position: 'bottomright'});

legendUKmap.onAdd = function (map) {
    var legent_text = "legend ";
    var div = L.DomUtil.create('div', 'legend_UKmap');
    div.innerHTML += '<div id="legend_UKmap_info"></div>';
    L.DomEvent.disableClickPropagation(div);
    L.DomEvent.disableScrollPropagation(div);
    return div;
};
legendUKmap.addTo(mapUK);

// end  setting a UK map 
//******************************************************************************
 //_utils.updateInfoBox(initialData);

_init.setTopicsMenu(initialData.topics).then(() => {
    _utils.initialSetInfoBox(initialData);
}).then(() => 
    _api.get_ics_data(API_URL, 
                      slc_threshold,
                      slc_topic,
                      slc_postcode_area,
                      slc_beneficiary,
                      slc_uoa,
                      slc_funder)         
).then(result => {
    console.log(result);

    _UOAChart.updateUOAChart(result.uoa_counts);
    _funderChart.updateFunderChart(result.funders_counts);
    _GlobalImactMap.updateGlobalImactMap(mapGlobal, layerGlobal, GlobalBoundary, result.countries_counts, palette_colors_GlobalMap);
    //console.log(result.institution_counts);
    _UKMap.updateUKMap(mapUK, layerUK, UKPostCodeAreasBoundary, result.institution_counts, palette_colors_UKMap);
}).then(() => {
    document.getElementById('firstloader').style.display = 'none';
}).catch(error => {
    console.log('In the catch', error);
});



$(window).on("resize", function () {
    _utils.setHightBoxs();
}).trigger("resize");



$("#idTopics .list-group-item").click(function (e) {
    
    $("#idTopics .list-group-item").removeClass("active");
    $(e.target).addClass("active");

    slc_topic = _utils.getActiveTopic();

    _utils.progressMenuOn();
    
    _api.get_ics_data(API_URL, 
                      slc_threshold,
                      slc_topic,
                      slc_postcode_area,
                      slc_beneficiary,
                      slc_uoa,
                      slc_funder).then(result => {
        _utils.updateLabelsSelectedOptionsBoxs(slc_postcode_area, slc_beneficiary);                   
        _utils.updateInfoBox(initialData);
        _UOAChart.updateUOAChart(result.uoa_counts);
        _funderChart.updateFunderChart(result.funders_counts);    
        _GlobalImactMap.updateGlobalImactMap(mapGlobal, layerGlobal, GlobalBoundary, result.countries_counts, palette_colors_GlobalMap);
        _UKMap.updateUKMap(mapUK, layerUK, UKPostCodeAreasBoundary, result.institution_counts, palette_colors_UKMap);
     }).then(() => {
          _utils.progressMenuOff();
     }).catch(error => {
        console.log('In the catch', error);
     });
     
});

$("#Options_of_Assessment").change(function(){
        var selectedAssessment = $('#Options_of_Assessment').children("option:selected").val();
        slc_uoa=selectedAssessment;
        
    _utils.progressMenuOn();
    
    _api.get_ics_data(API_URL, 
                      slc_threshold,
                      slc_topic,
                      slc_postcode_area,
                      slc_beneficiary,
                      slc_uoa,
                      slc_funder).then(result => {
        _utils.updateLabelsSelectedOptionsBoxs(slc_postcode_area, slc_beneficiary);    
        _UOAChart.updateUOAChart(result.uoa_counts);
        _funderChart.updateFunderChart(result.funders_counts);    
        _GlobalImactMap.updateGlobalImactMap(mapGlobal, layerGlobal, GlobalBoundary, result.countries_counts, palette_colors_GlobalMap);
        _UKMap.updateUKMap(mapUK, layerUK, UKPostCodeAreasBoundary, result.institution_counts, palette_colors_UKMap);
     }).then(() => {
          _utils.progressMenuOff();
     }).catch(error => {
        console.log('In the catch', error);
     });        
});
 
function resetSelectionUKmap(){
    
     $('[data-bs-toggle="tooltip"]').tooltip('hide'); 
     slc_postcode_area=null;
     infoboxSelectedUKmap.remove(mapUK);
    _utils.progressMenuOn();
    
    _api.get_ics_data(API_URL, 
                      slc_threshold,
                      slc_topic,
                      slc_postcode_area,
                      slc_beneficiary,
                      slc_uoa,
                      slc_funder).then(result => {
        _utils.updateLabelsSelectedOptionsBoxs(slc_postcode_area, slc_beneficiary);    
        _UOAChart.updateUOAChart(result.uoa_counts);
        _funderChart.updateFunderChart(result.funders_counts);    
        _GlobalImactMap.updateGlobalImactMap(mapGlobal, layerGlobal, GlobalBoundary, result.countries_counts, palette_colors_GlobalMap);
        _UKMap.updateUKMap(mapUK, layerUK, UKPostCodeAreasBoundary, result.institution_counts, palette_colors_UKMap);
     }).then(() => {
          _utils.progressMenuOff();
     }).catch(error => {
        console.log('In the catch', error);
     });   
}  

    
$( "#reload_selected_options" ).on( "click", function() {
    
     $('#Options_of_Assessment').prop("selectedIndex", 0);
     
     $('[data-bs-toggle="tooltip"]').tooltip('hide'); 

     slc_topic=null;
     slc_postcode_area=null;
     slc_beneficiary=null;
     slc_uoa=null;
     slc_funder=null;
     infoboxSelectedUKmap.remove(mapUK);
    _utils.progressMenuOn();
    
    _api.get_ics_data(API_URL, 
                      slc_threshold,
                      slc_topic,
                      slc_postcode_area,
                      slc_beneficiary,
                      slc_uoa,
                      slc_funder).then(result => {
        _utils.updateLabelsSelectedOptionsBoxs(slc_postcode_area, slc_beneficiary);    
        _UOAChart.updateUOAChart(result.uoa_counts);
        _funderChart.updateFunderChart(result.funders_counts);    
        _GlobalImactMap.updateGlobalImactMap(mapGlobal, layerGlobal, GlobalBoundary, result.countries_counts, palette_colors_GlobalMap);
        _UKMap.updateUKMap(mapUK, layerUK, UKPostCodeAreasBoundary, result.institution_counts, palette_colors_UKMap);
     }).then(() => {
          _utils.progressMenuOff();
     }).catch(error => {
        console.log('In the catch', error);
     });
} );

 
 
//$( "#ics_table_all_btn" ).on( "click", function() {
//    
//    var ics_table_all_Modal = new bootstrap.Modal(document.getElementById('ics_table_all_modal'), {
//    keyboard: false
//    });
//
//    ics_table_all_Modal.show();
//
//});
 
 
//  initialize all tooltips
//var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
//var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
//  return new bootstrap.Tooltip(tooltipTriggerEl)
//})
