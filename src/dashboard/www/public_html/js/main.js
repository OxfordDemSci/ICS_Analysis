//var API_URL = "./api/";
var API_URL = "http://127.0.0.1:8000/api/";

import * as _api from './api.js?version=2.8'
import * as _init from './init.js?version=4.9'
import * as _utils from './utils.js?version=6.5'
import * as _UOAChart from './uoa_chart.js?version=6.2'
import * as _funderChart from './funder_chart.js?version=3.4'
import * as _GlobalImactMap from './global_impact_map.js?version=3.8'
import * as _UKMap from './UK_map.js?version=5.8'
import * as _ICSTable_columns from './ICSTable_columns.js?version=5.8'
import * as _generateReport from './generate_report.js?version=0.8'

var slc_postcode_area=null;
var slc_beneficiary=null;
var slc_uoa=null;
var slc_topic=null;
var slc_threshold=0.5;
var slc_funder=null;
var slc_numberFundersLimit=30;
var slc_group_ID=0;
var slc_group_Name="All Groups";


let initialData = _api.getInitData(API_URL);
let GlobalBoundary = _api.getGlobalBoundary();
let UKPostCodeAreasBoundary = _api.getUKPostCodeAreasBoundary();

let palette_colors_GlobalMap = initialData.website_text.global_colourramp;
let palette_colors_UKMap = initialData.website_text.uk_map_colourramp;
let color_bar_Funder = initialData.website_text.funders_bar_colour;

let ICSTable_columns = null;
//let ICSTable_columns = _ICSTable_columns.getICSTable_columns();
let ICSTable_max_text_length = 40;


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
                    _GlobalImactMap.highlightFeatureGlobalImactMap(e, infoboxMapGlobal, mapGlobal);
                },
                mouseout: function (e) {
                    _GlobalImactMap.resetHighlightGlobalImactMap(e, infoboxMapGlobal, mapGlobal);
//                    if (mapGlobalPopup && mapGlobal) {
//                        mapGlobal.closePopup(mapGlobalPopup);
//                    }                    
                },
                click: function (e) {
                    
                        //_GlobalImactMap.clickGlobalImactMap(e, mapGlobal, mapGlobalPopup);
                        slc_beneficiary = e.target.feature.properties.iso_a3;
                        _utils.updateLabelsSelectedOptionsBoxs(slc_postcode_area, slc_beneficiary, slc_funder);
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
                            _UOAChart.updateUOAChart(result.uoa_counts, slc_numberFundersLimit);
                            _funderChart.updateFunderChart(result.funders_counts, color_bar_Funder, slc_numberFundersLimit);    
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

mapGlobal.createPane('labels');
mapGlobal.getPane('labels').style.zIndex = 650;
mapGlobal.getPane('labels').style.pointerEvents = 'none';
var cartocdn = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_only_labels/{z}/{x}/{y}.png',{ 
    pane: 'labels'
});


var infoboxMapGlobal = L.control({ position: 'topleft' });

infoboxMapGlobal.onAdd = function (mapUK) {
    this._div = L.DomUtil.create('div', 'infoBoxMapGlobal'); 
    this._div.innerHTML += '<div id="infoBoxMapGlobal_info"></div>';
    L.DomEvent.disableClickPropagation(this._div);
    L.DomEvent.disableScrollPropagation(this._div);    
    //this.update();
    return this._div;
};

infoboxMapGlobal.update = function (props) {
    this._div.innerHTML = '<div id="infoBoxMapGlobal_info"></div>';
};
infoboxMapGlobal.addTo(mapGlobal);
infoboxMapGlobal.remove(mapGlobal);



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
        center: [55.10, -3.22],
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
                         _utils.updateLabelsSelectedOptionsBoxs(slc_postcode_area, slc_beneficiary, slc_funder);
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
                            console.log("click UK map", result);
                            _utils.LoadCurrentICSTable(result.ics_table, ICSTable_columns, ICSTable_max_text_length);
                            if ( document.getElementById('chKeepPOSTarea').checked === false ){    
                                _UKMap.updateUKMap(mapUK, layerUK, UKPostCodeAreasBoundary, result.institution_counts, palette_colors_UKMap);                    
                            }                            
                            _UOAChart.updateUOAChart(result.uoa_counts);
                            _funderChart.updateFunderChart(result.funders_counts, color_bar_Funder,  20);    
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

_init.setTopicsMenu(initialData).then(() => {
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
    _init.setContactInfo(initialData.website_text.contact); 
    _init.setAboutInfo(initialData.website_text.about); 
    _utils.updateModalInfoBox(initialData);
    _utils.initialSetLabels(initialData);
    _utils.LoadCurrentICSTable(result.ics_table, ICSTable_columns, ICSTable_max_text_length);
    _UOAChart.updateUOAChart(result.uoa_counts, slc_numberFundersLimit);
    _funderChart.updateFunderChart(result.funders_counts, color_bar_Funder, slc_numberFundersLimit);
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
    //_utils.ResiseICSTable();
}).trigger("resize");


//$("#idTopics .list-group-item").click(function (e) {
$("#idTopics").on('click','li',function(e){    
    
    $("#idTopics .list-group-item").removeClass("active");
    $(e.target).addClass("active");

    slc_topic = _utils.getActiveTopic();

    slc_postcode_area=null;
    infoboxSelectedUKmap.remove(mapUK);
    slc_beneficiary=null;
    slc_funder=null;
    slc_uoa=null;
    
    mapUK.setView(mapUK.options.center, mapUK.options.zoom);
    mapGlobal.setView(mapGlobal.options.center, mapGlobal.options.zoom);
    
    _utils.progressMenuOn();
    
    _api.get_ics_data(API_URL, 
                      slc_threshold,
                      slc_topic,
                      slc_postcode_area,
                      slc_beneficiary,
                      slc_uoa,
                      slc_funder).then(result => {
        _utils.LoadCurrentICSTable(result.ics_table, ICSTable_columns, ICSTable_max_text_length);                  
        _utils.updateLabelsSelectedOptionsBoxs(slc_postcode_area, slc_beneficiary, slc_funder);                   
        _utils.updateInfoBox(initialData);
        _utils.updateModalInfoBox(initialData);
        _UOAChart.updateUOAChart(result.uoa_counts);
        _funderChart.updateFunderChart(result.funders_counts, color_bar_Funder, slc_numberFundersLimit); 
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
        _utils.LoadCurrentICSTable(result.ics_table, ICSTable_columns, ICSTable_max_text_length);                    
        _utils.updateLabelsSelectedOptionsBoxs(slc_postcode_area, slc_beneficiary, slc_funder);    
        _UOAChart.updateUOAChart(result.uoa_counts);
        _funderChart.updateFunderChart(result.funders_counts, color_bar_Funder, slc_numberFundersLimit);    
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
        _utils.LoadCurrentICSTable(result.ics_table, ICSTable_columns, ICSTable_max_text_length);                    
        _utils.updateLabelsSelectedOptionsBoxs(slc_postcode_area, slc_beneficiary, slc_funder);    
        _UOAChart.updateUOAChart(result.uoa_counts);
        _funderChart.updateFunderChart(result.funders_counts, color_bar_Funder, slc_numberFundersLimit);    
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
      $('#idGroups').prop("selectedIndex", 0);
      
      _init.setTopicsMenu(initialData);
     
     $("#idTopics .list-group-item").removeClass("active");
     $("#idTopics .list-group-item").first().addClass("active");
     
     $('[data-bs-toggle="tooltip"]').tooltip('hide'); 

     slc_group_ID=0;
     slc_group_Name="All Groups";

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
        _utils.LoadCurrentICSTable(result.ics_table, ICSTable_columns, ICSTable_max_text_length);                   
        _utils.updateLabelsSelectedOptionsBoxs(slc_postcode_area, slc_beneficiary, slc_funder);    
        _UOAChart.updateUOAChart(result.uoa_counts);
        _funderChart.updateFunderChart(result.funders_counts, color_bar_Funder, slc_numberFundersLimit);    
        _GlobalImactMap.updateGlobalImactMap(mapGlobal, layerGlobal, GlobalBoundary, result.countries_counts, palette_colors_GlobalMap);
        _UKMap.updateUKMap(mapUK, layerUK, UKPostCodeAreasBoundary, result.institution_counts, palette_colors_UKMap);
        document.getElementById("reload_selected_options").style.visibility = "hidden";
     }).then(() => {
          _utils.progressMenuOff();
     }).catch(error => {
        console.log('In the catch', error);
     });
} );

 
 
$( "#ics_table_all_btn" ).on( "click", function() {
    $('#ics_table_all_modal').modal('show');
});
 
 
$(document).on('shown.bs.modal', function (e) {
      $.fn.dataTable.tables( {visible: true, api: true} ).columns.adjust();
});


$( "#btnDownlaodICSTable" ).on( "click", function() {
    
 _utils.downloadURI(API_URL, 
                "ICS_table.csv",
                slc_threshold, 
                slc_topic, 
                slc_postcode_area, 
                slc_beneficiary, 
                slc_uoa, 
                slc_funder);
});


$( "#btnViewDetailsInfoBox" ).on( "click", function() {
    $('#idMdViewDetailsInfoBox').modal('show');
});


var FundersChart = echarts.init(document.getElementById('chartContainer_top_left'));

FundersChart.on('click', function(params) {

    slc_funder=params.name;
    _utils.progressMenuOn();
    
    _api.get_ics_data(API_URL, 
                      slc_threshold,
                      slc_topic,
                      slc_postcode_area,
                      slc_beneficiary,
                      slc_uoa,
                      slc_funder).then(result => {
        _utils.LoadCurrentICSTable(result.ics_table, ICSTable_columns, ICSTable_max_text_length);                    
        _utils.updateLabelsSelectedOptionsBoxs(slc_postcode_area, slc_beneficiary, slc_funder);    
        _UOAChart.updateUOAChart(result.uoa_counts);
        _funderChart.updateFunderChart(result.funders_counts, color_bar_Funder, slc_numberFundersLimit);    
        _GlobalImactMap.updateGlobalImactMap(mapGlobal, layerGlobal, GlobalBoundary, result.countries_counts, palette_colors_GlobalMap);
        _UKMap.updateUKMap(mapUK, layerUK, UKPostCodeAreasBoundary, result.institution_counts, palette_colors_UKMap);
     }).then(() => {
          _utils.progressMenuOff();
     }).catch(error => {
        console.log('In the catch', error);
     });     
 
});



$("#numberFundersLimit").change(function(){
    
     slc_numberFundersLimit=$('#numberFundersLimit').children("option:selected").val();
        
    _utils.progressMenuOn();
    
    _api.get_ics_data(API_URL, 
                      slc_threshold,
                      slc_topic,
                      slc_postcode_area,
                      slc_beneficiary,
                      slc_uoa,
                      slc_funder).then(result => {
        _utils.LoadCurrentICSTable(result.ics_table, ICSTable_columns, ICSTable_max_text_length);                    
        _utils.updateLabelsSelectedOptionsBoxs(slc_postcode_area, slc_beneficiary, slc_funder);    
        _UOAChart.updateUOAChart(result.uoa_counts);
        _funderChart.updateFunderChart(result.funders_counts, color_bar_Funder, slc_numberFundersLimit);    
        _GlobalImactMap.updateGlobalImactMap(mapGlobal, layerGlobal, GlobalBoundary, result.countries_counts, palette_colors_GlobalMap);
        _UKMap.updateUKMap(mapUK, layerUK, UKPostCodeAreasBoundary, result.institution_counts, palette_colors_UKMap);
     }).then(() => {
          _utils.progressMenuOff();
     }).catch(error => {
        console.log('In the catch', error);
     });        
});


$('#customRangeThreshold').on('change', function (event) {
    let thresholdValue = event.target.value;
    document.getElementById('idMdSettingsThresholdValue').innerHTML = thresholdValue; 
    slc_threshold = thresholdValue; 
    
    _utils.progressMenuOn();
    
    _api.get_ics_data(API_URL, 
                      slc_threshold,
                      slc_topic,
                      slc_postcode_area,
                      slc_beneficiary,
                      slc_uoa,
                      slc_funder).then(result => {
        _utils.LoadCurrentICSTable(result.ics_table, ICSTable_columns, ICSTable_max_text_length);                    
        _utils.updateLabelsSelectedOptionsBoxs(slc_postcode_area, slc_beneficiary, slc_funder);    
        _UOAChart.updateUOAChart(result.uoa_counts);
        _funderChart.updateFunderChart(result.funders_counts, color_bar_Funder, slc_numberFundersLimit);    
        _GlobalImactMap.updateGlobalImactMap(mapGlobal, layerGlobal, GlobalBoundary, result.countries_counts, palette_colors_GlobalMap);
        _UKMap.updateUKMap(mapUK, layerUK, UKPostCodeAreasBoundary, result.institution_counts, palette_colors_UKMap);
     }).then(() => {
          _utils.progressMenuOff();
     }).catch(error => {
        console.log('In the catch', error);
     });     
});


$('#chCountryLabels').change(function () {
        if ($(this).is(":checked")) {
            mapGlobal.addLayer(cartocdn);
        } else {
            mapGlobal.removeLayer(cartocdn);
        }
});

$( "#btnSettings" ).on( "click", function() {
    $('#idMdSettings').modal('show');
});

$( "#btnContact" ).on( "click", function() {
    $('#idMdContact').modal('show');
});

$( "#btnAbout" ).on( "click", function() {
    $('#idMdAbout').modal('show');
});


$( "#btnGenerateReport" ).on( "click", function() {

                        _utils.progressMenuOn();
                        _generateReport.GenerateReport(
                                                    API_URL, 
                                                    "ICS_table.csv",
                                                    slc_threshold, 
                                                    slc_topic, 
                                                    slc_postcode_area, 
                                                    slc_beneficiary, 
                                                    slc_uoa, 
                                                    slc_funder).then(result => {
                            setTimeout(() => {
                                console.log("report was created");
                                _utils.progressMenuOff();
                            }, 1000);                            
                        }).catch(error => {
                            console.log('In the catch', error);
                            _utils.progressMenuOff();
                        });                  
                
                
});



$("#idGroups").change(function (e) {
    e.preventDefault();
    
    var selectedGroupValue = $('#idGroups').children("option:selected").val();
    slc_group_ID = parseInt(selectedGroupValue);
    let topic_groups = initialData.topic_groups;

    if (slc_group_ID === 0) {
        slc_group_Name = "All Groups";
    } else {
        slc_group_Name = topic_groups.filter(element => (element.group_id === slc_group_ID))[0].topic_group;
    }

   // _utils.updateTopicsMenu(initialData.topics, slc_group_Name);

     $('#Options_of_Assessment').prop("selectedIndex", 0);
     $("#idTopics .list-group-item").removeClass("active");
     $("#idTopics .list-group-item").first().addClass("active");
     
     $('[data-bs-toggle="tooltip"]').tooltip('hide'); 


     slc_postcode_area=null;
     slc_beneficiary=null;
     slc_uoa=null;
     slc_funder=null;
     infoboxSelectedUKmap.remove(mapUK);
    
    _utils.progressMenuOn();
    
    _utils.updateTopicsMenu(initialData.topics, slc_group_Name).then(() => {
        slc_topic = _utils.getActiveTopic();
    }).then(() =>
        _api.get_ics_data(API_URL,
                slc_threshold,
                slc_topic,
                slc_postcode_area,
                slc_beneficiary,
                slc_uoa,
                slc_funder)
    ).then(result => {
        _init.setContactInfo(initialData.website_text.contact);
        _init.setAboutInfo(initialData.website_text.about);
        _utils.updateModalInfoBox(initialData);
        _utils.initialSetLabels(initialData);
        _utils.LoadCurrentICSTable(result.ics_table, ICSTable_columns, ICSTable_max_text_length);
        _UOAChart.updateUOAChart(result.uoa_counts, slc_numberFundersLimit);
        _funderChart.updateFunderChart(result.funders_counts, color_bar_Funder, slc_numberFundersLimit);
        _GlobalImactMap.updateGlobalImactMap(mapGlobal, layerGlobal, GlobalBoundary, result.countries_counts, palette_colors_GlobalMap);
        //console.log(result.institution_counts);
        _UKMap.updateUKMap(mapUK, layerUK, UKPostCodeAreasBoundary, result.institution_counts, palette_colors_UKMap);
        _utils.updateLabelsSelectedOptionsBoxs(slc_postcode_area, slc_beneficiary, slc_funder);    
    }).then(() => {
        document.getElementById('firstloader').style.display = 'none';
    }).catch(error => {
        console.log('In the catch', error);
    });

});