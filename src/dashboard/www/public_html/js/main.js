var API_URL = "./api/";
// var API_URL = "http://127.0.0.1:8000/api/";

import * as _api from './api.js?version=2.91'
import * as _init from './init.js?version=4.93'
import * as _utils from './utils.js?version=6.93'
import * as _UOAChart from './uoa_chart.js?version=6.45'
import * as _funderChart from './funder_chart.js?version=3.5'
import * as _GlobalImactMap from './global_impact_map.js?version=3.9'
import * as _UKMap from './UK_map.js?version=6.0'
import * as _ICSTable_columns from './ICSTable_columns.js?version=5.9'
import * as _generateReport from './generate_report.js?version=0.8'
import * as _UKRegionCountsMap from './uk_region_counts_map.js?version=0.21'
import * as _CountryToPC from './country_to_pc.js?version=0.8' 

var slc_postcode_area=null;
var slc_postcode_area_name=null;
var slc_beneficiary=null;
var slc_uoa=null;
var slc_uoa_name=null;
var slc_topic=null;
var slc_threshold=1;
var slc_funder=null;
var slc_numberFundersLimit=10;
var slc_group_ID=0;
var slc_group_Name="All Clusters";
var slc_Impact_Beneficiariest="Global";

let total_rows_pagination_meta=0;

let initialData = _api.getInitData(API_URL);
let GlobalBoundary = _api.getGlobalBoundary();
let UKPostCodeAreasBoundary = _api.getUKPostCodeAreasBoundary();

let palette_colors_GlobalMap = initialData.website_text.global_colourramp;
let palette_colors_UKMap = initialData.website_text.uk_map_colourramp;
let color_bar_Funder = initialData.website_text.funders_bar_colour;

//let ICSTable_columns = null;
let ICSTable_columns = _ICSTable_columns.getICSTable_columns();
let ICSTable_max_text_length = 40;

let CountryToPC=_CountryToPC.getCountryToPC();

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



var clusters_UK_region = L.markerClusterGroup({
        iconCreateFunction: function(cluster) {
            var markers = cluster.getAllChildMarkers();
                var counts = 0
                for (var i = 0; i < markers.length; i++) {

                        counts += markers[i].feature.properties.count;
                        //console.log(counts);
                }    
            var c = 'marker-cluster-';    
            if (counts < 10) {
                c += 'small';
            } else if (counts < 100) {
                c += 'medium';
            } else {
                c += 'large';
            }
            return new L.DivIcon({
                html: '<div><span>' + counts + '</span></div>',
                className: 'marker-cluster ' + c,
                iconSize: new L.Point(40, 40)
            });
            
        }
    });



//******************************************************************************
// start setting a g lobal map 

var mapGlobalOptions = {
        zoomControl: true,
        attributionControl: false,
        center: [40, 25],
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
                        _utils.updateLabelsSelectedOptionsBoxs(slc_postcode_area_name, slc_beneficiary, slc_funder, slc_uoa_name);
                        _utils.progressMenuOn();
                         slc_topic = _utils.getActiveTopic();
                        _api.get_ics_data(API_URL, 
                                        slc_threshold,
                                        slc_topic,
                                        slc_postcode_area,
                                        slc_beneficiary,
                                        slc_uoa,
                                        slc_uoa_name,
                                        slc_funder).then(result => {
                            infoboxSelectedUKmap.remove(mapUK);                               
                            _UKMap.updateUKMap(mapUK, layerUK, UKPostCodeAreasBoundary, result.institution_counts, palette_colors_UKMap);   
                            if (slc_uoa_name === null){
                                _UOAChart.updateUOAChart(result.uoa_counts);
                            }
                            _funderChart.updateFunderChart(result.funders_counts, color_bar_Funder, slc_numberFundersLimit);    
                            _GlobalImactMap.updateGlobalImactMap(mapGlobal, layerGlobal, GlobalBoundary, result.countries_counts, palette_colors_GlobalMap);
                            _utils.updateTopicsMenuAvailable(initialData, result.topics_available);       
                            total_rows_pagination_meta=result.table_pagination_meta.total_rows;
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
        center: [54.5, -3],
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
                         slc_postcode_area_name = slc_postcode_area;
                         _utils.updateLabelsSelectedOptionsBoxs(slc_postcode_area_name, slc_beneficiary, slc_funder, slc_uoa_name);
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
                                        slc_uoa_name,
                                        slc_funder).then(result => {
                            if ( document.getElementById('chKeepPOSTarea').checked === false ){    
                                _UKMap.updateUKMap(mapUK, layerUK, UKPostCodeAreasBoundary, result.institution_counts, palette_colors_UKMap);                    
                            }                            
                            if (slc_uoa_name === null){
                                _UOAChart.updateUOAChart(result.uoa_counts);
                            }
                            _funderChart.updateFunderChart(result.funders_counts, color_bar_Funder,  slc_numberFundersLimit);  
                            
                            if (slc_Impact_Beneficiariest === "Global") {
                                _GlobalImactMap.updateGlobalImactMap(mapGlobal, layerGlobal, GlobalBoundary, result.countries_counts, palette_colors_GlobalMap);
                            } else {
                                _UKRegionCountsMap.updateUKregion_counts_map(mapGlobal, clusters_UK_region, result.uk_region_counts);
                            }
                            total_rows_pagination_meta=result.table_pagination_meta.total_rows;
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
            slc_uoa_name,
            slc_funder)
).then(result => {
    _init.setUK_Country_names_menu(CountryToPC);
    _init.setContactInfo(initialData.website_text.contact);
    _init.setAboutInfo(initialData.website_text.about);
    _init.setTeamInfo(initialData.website_text.team);
    _init.setHelpInfo(initialData.website_text.instructions);
    _utils.updateModalInfoBox(initialData);
    //_utils.initialSetLabels(initialData);
    if (slc_uoa_name === null) {
        _UOAChart.updateUOAChart(result.uoa_counts);
    }
    _funderChart.updateFunderChart(result.funders_counts, color_bar_Funder, slc_numberFundersLimit);
    _GlobalImactMap.updateGlobalImactMap(mapGlobal, layerGlobal, GlobalBoundary, result.countries_counts, palette_colors_GlobalMap);
    _UKMap.updateUKMap(mapUK, layerUK, UKPostCodeAreasBoundary, result.institution_counts, palette_colors_UKMap);
    total_rows_pagination_meta = result.table_pagination_meta.total_rows;
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

    //slc_postcode_area=null;
    //slc_beneficiary=null;
    //slc_funder=null;
    //slc_uoa=null;
    
    //mapUK.setView(mapUK.options.center, mapUK.options.zoom);
    //mapGlobal.setView(mapGlobal.options.center, mapGlobal.options.zoom);
    
    _utils.progressMenuOn();
    
    _api.get_ics_data(API_URL,
            slc_threshold,
            slc_topic,
            slc_postcode_area,
            slc_beneficiary,
            slc_uoa,
            slc_uoa_name,
            slc_funder).then(result => {
        infoboxSelectedUKmap.remove(mapUK);
        _utils.updateLabelsSelectedOptionsBoxs(slc_postcode_area_name, slc_beneficiary, slc_funder, slc_uoa_name);
        _utils.updateInfoBox(initialData);
        _utils.updateModalInfoBox(initialData);
        if (slc_uoa_name === null) {
            _UOAChart.updateUOAChart(result.uoa_counts);
        }
        _funderChart.updateFunderChart(result.funders_counts, color_bar_Funder, slc_numberFundersLimit);

        if (slc_Impact_Beneficiariest === "Global") {
            _GlobalImactMap.updateGlobalImactMap(mapGlobal, layerGlobal, GlobalBoundary, result.countries_counts, palette_colors_GlobalMap);
        } else {
            _UKRegionCountsMap.updateUKregion_counts_map(mapGlobal, clusters_UK_region, result.uk_region_counts);
        }

        _UKMap.updateUKMap(mapUK, layerUK, UKPostCodeAreasBoundary, result.institution_counts, palette_colors_UKMap);
        total_rows_pagination_meta = result.table_pagination_meta.total_rows;
    }).then(() => {
        _utils.progressMenuOff();
    }).catch(error => {
        console.log('In the catch', error);
    });

});

$("#Options_of_Assessment").change(function () {
    var selectedAssessment = $('#Options_of_Assessment').children("option:selected").val();
    slc_uoa = selectedAssessment;

    _utils.progressMenuOn();

    _api.get_ics_data(API_URL,
            slc_threshold,
            slc_topic,
            slc_postcode_area,
            slc_beneficiary,
            slc_uoa,
            slc_uoa_name,
            slc_funder).then(result => {
        infoboxSelectedUKmap.remove(mapUK);         
        _utils.updateTopicsMenuAvailable(initialData, result.topics_available);
        _utils.updateLabelsSelectedOptionsBoxs(slc_postcode_area_name, slc_beneficiary, slc_funder, slc_uoa_name);
        _UOAChart.updateUOAChart(result.uoa_counts);
        _funderChart.updateFunderChart(result.funders_counts, color_bar_Funder, slc_numberFundersLimit);
        if (slc_Impact_Beneficiariest === "Global") {
            _GlobalImactMap.updateGlobalImactMap(mapGlobal, layerGlobal, GlobalBoundary, result.countries_counts, palette_colors_GlobalMap);
        } else {
            _UKRegionCountsMap.updateUKregion_counts_map(mapGlobal, clusters_UK_region, result.uk_region_counts);
        }
        _UKMap.updateUKMap(mapUK, layerUK, UKPostCodeAreasBoundary, result.institution_counts, palette_colors_UKMap);
        total_rows_pagination_meta=result.table_pagination_meta.total_rows;
    }).then(() => {
        _utils.progressMenuOff();
    }).catch(error => {
        console.log('In the catch', error);
    });
});
 
function resetSelectionUKmap() {

    $('[data-bs-toggle="tooltip"]').tooltip('hide');

    let selected_country_name = $('#Options_of_Country_Names').children("option:selected").val();
    slc_postcode_area = CountryToPC[selected_country_name];
    slc_postcode_area_name = selected_country_name;

    _utils.progressMenuOn();

    _api.get_ics_data(API_URL,
            slc_threshold,
            slc_topic,
            slc_postcode_area,
            slc_beneficiary,
            slc_uoa,
            slc_uoa_name,
            slc_funder).then(result => {
        infoboxSelectedUKmap.remove(mapUK);
        _utils.updateTopicsMenuAvailable(initialData, result.topics_available);
        _utils.updateLabelsSelectedOptionsBoxs(slc_postcode_area_name, slc_beneficiary, slc_funder, slc_uoa_name);
        if (slc_uoa_name === null) {
            _UOAChart.updateUOAChart(result.uoa_counts);
        }
        _funderChart.updateFunderChart(result.funders_counts, color_bar_Funder, slc_numberFundersLimit);
        if (slc_Impact_Beneficiariest === "Global") {
            _GlobalImactMap.updateGlobalImactMap(mapGlobal, layerGlobal, GlobalBoundary, result.countries_counts, palette_colors_GlobalMap);
        } else {
            _UKRegionCountsMap.updateUKregion_counts_map(mapGlobal, clusters_UK_region, result.uk_region_counts);
        }
        _UKMap.updateUKMap(mapUK, layerUK, UKPostCodeAreasBoundary, result.institution_counts, palette_colors_UKMap);
        total_rows_pagination_meta = result.table_pagination_meta.total_rows;
    }).then(() => {
        _utils.progressMenuOff();
    }).catch(error => {
        console.log('In the catch', error);
    });
}  

    
$( "#reload_selected_options" ).on( "click", function() {

     $('#Options_of_Assessment').prop("selectedIndex", 0);
     $('#Options_of_Impact_Beneficiariest').prop("selectedIndex", 0);
     $('#Options_of_Country_Names').prop("selectedIndex", 0);
     
      $('#idGroups').prop("selectedIndex", 0);
      
      _init.setTopicsMenu(initialData);
     
     $("#idTopics .list-group-item").removeClass("active");
     $("#idTopics .list-group-item").first().addClass("active");
     
     $('[data-bs-toggle="tooltip"]').tooltip('hide'); 

     slc_group_ID=0;
     slc_group_Name="All Clusters";

     slc_topic=null;
     slc_postcode_area=null;
     slc_postcode_area_name="All";
     slc_beneficiary=null;
     slc_uoa=null;
     slc_uoa_name=null;
     slc_funder=null;
     
    _utils.progressMenuOn();
    
    if (mapGlobal.hasLayer(clusters_UK_region)) {
        mapGlobal.removeLayer(clusters_UK_region);
        mapGlobal.addLayer(layerGlobal);
        mapGlobal.addControl(legendMapGlobal);   
        slc_Impact_Beneficiariest="Global";
        mapGlobal.setView(mapGlobal.options.center, mapGlobal.options.zoom);
    }
    
    mapUK.setView(mapUK.options.center, mapUK.options.zoom);
 
    _api.get_ics_data(API_URL, 
                      slc_threshold,
                      slc_topic,
                      slc_postcode_area,
                      slc_beneficiary,
                      slc_uoa,
                      slc_uoa_name,
                      slc_funder).then(result => {
        infoboxSelectedUKmap.remove(mapUK);                  
        //_init.setTopicsMenu(initialData);                                 
        _utils.updateLabelsSelectedOptionsBoxs(slc_postcode_area_name, slc_beneficiary, slc_funder, slc_uoa_name);    
        _UOAChart.updateUOAChart(result.uoa_counts);
        _funderChart.updateFunderChart(result.funders_counts, color_bar_Funder, slc_numberFundersLimit);    
        if (slc_Impact_Beneficiariest === "Global") {
            _GlobalImactMap.updateGlobalImactMap(mapGlobal, layerGlobal, GlobalBoundary, result.countries_counts, palette_colors_GlobalMap);
        } else {
            _UKRegionCountsMap.updateUKregion_counts_map(mapGlobal, clusters_UK_region, result.uk_region_counts);
        }
        _UKMap.updateUKMap(mapUK, layerUK, UKPostCodeAreasBoundary, result.institution_counts, palette_colors_UKMap);
        document.getElementById("reload_selected_options").style.visibility = "hidden";
        total_rows_pagination_meta=result.table_pagination_meta.total_rows;
     }).then(() => {
          _utils.progressMenuOff();
     }).catch(error => {
        console.log('In the catch', error);
     });
} );

 
 
$( "#ics_table_all_btn" ).on( "click", function() {
    _utils.progressMenuOn();    
    _api.get_ics_data(API_URL, 
                      slc_threshold,
                      slc_topic,
                      slc_postcode_area,
                      slc_beneficiary,
                      slc_uoa,
                      slc_uoa_name,
                      slc_funder,
                      1,
                      total_rows_pagination_meta).then(result => {
        $('#ics_table_all_modal').modal('show');                  
        _utils.LoadCurrentICSTable(result.ics_table, ICSTable_columns, ICSTable_max_text_length);
     }).then(() => {
          _utils.progressMenuOff();
     }).catch(error => {
        console.log('In the catch', error);
     });       
});
 
// Clear tabel after closing the window to free up memory 
$("#ics_table_all_modal").on("hide.bs.modal", function () {
    if ($.fn.DataTable.isDataTable('#tblReportResultsICSTabl')) {
        $('#tblReportResultsICSTabl').dataTable().fnClearTable();
        $('#tblReportResultsICSTabl').dataTable().fnDestroy();
    }
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
                slc_uoa_name,
                slc_funder);
});


//$( "#btnViewDetailsInfoBox" ).on( "click", function() {
//    $('#idMdViewDetailsInfoBox').modal('show');
//});

$( "#label_Topic_Description_expand" ).on( "click", function() {
    $('#idMd_Topic_description_expand').modal('show');
});

$( "#label_Example_Impact_Case_Studies_expand" ).on( "click", function() {
    $('#idMd_Example_Impact_Case_Studies_expand').modal('show');
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
                      slc_uoa_name,
                      slc_funder).then(result => {
        infoboxSelectedUKmap.remove(mapUK);                   
        _utils.updateTopicsMenuAvailable(initialData, result.topics_available);                                      
        _utils.updateLabelsSelectedOptionsBoxs(slc_postcode_area_name, slc_beneficiary, slc_funder, slc_uoa_name);    
        if (slc_uoa_name === null){
           _UOAChart.updateUOAChart(result.uoa_counts);
        }
        _funderChart.updateFunderChart(result.funders_counts, color_bar_Funder, slc_numberFundersLimit);    
        if (slc_Impact_Beneficiariest === "Global") {
            _GlobalImactMap.updateGlobalImactMap(mapGlobal, layerGlobal, GlobalBoundary, result.countries_counts, palette_colors_GlobalMap);
        } else {
            _UKRegionCountsMap.updateUKregion_counts_map(mapGlobal, clusters_UK_region, result.uk_region_counts);
        }
        _UKMap.updateUKMap(mapUK, layerUK, UKPostCodeAreasBoundary, result.institution_counts, palette_colors_UKMap);
        total_rows_pagination_meta=result.table_pagination_meta.total_rows;
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
                      slc_uoa_name,
                      slc_funder).then(result => {
        _utils.updateTopicsMenuAvailable(initialData, result.topics_available);                               
        _utils.updateLabelsSelectedOptionsBoxs(slc_postcode_area_name, slc_beneficiary, slc_funder, slc_uoa_name);    
        if (slc_uoa_name === null){
           _UOAChart.updateUOAChart(result.uoa_counts);
        }
        _funderChart.updateFunderChart(result.funders_counts, color_bar_Funder, slc_numberFundersLimit);    
        if (slc_Impact_Beneficiariest === "Global") {
            _GlobalImactMap.updateGlobalImactMap(mapGlobal, layerGlobal, GlobalBoundary, result.countries_counts, palette_colors_GlobalMap);
        } else {
            _UKRegionCountsMap.updateUKregion_counts_map(mapGlobal, clusters_UK_region, result.uk_region_counts);
        }
        _UKMap.updateUKMap(mapUK, layerUK, UKPostCodeAreasBoundary, result.institution_counts, palette_colors_UKMap);
        total_rows_pagination_meta=result.table_pagination_meta.total_rows;
     }).then(() => {
          _utils.progressMenuOff();
     }).catch(error => {
        console.log('In the catch', error);
     });        
});


//  Threshold option  ****
//  **********************
//$('#customRangeThreshold').on('change', function (event) {
//    let thresholdValue = event.target.value;
//    document.getElementById('idMdSettingsThresholdValue').innerHTML = thresholdValue; 
//    slc_threshold = thresholdValue; 
//    
//    _utils.progressMenuOn();
//    
//    _api.get_ics_data(API_URL, 
//                      slc_threshold,
//                      slc_topic,
//                      slc_postcode_area,
//                      slc_beneficiary,
//                      slc_uoa,
//                      slc_uoa_name,
//                      slc_funder).then(result => {
//        _utils.updateTopicsMenuAvailable(initialData, result.topics_available);                  
//        _utils.LoadCurrentICSTable(result.ics_table, ICSTable_columns, ICSTable_max_text_length);                    
//        _utils.updateLabelsSelectedOptionsBoxs(slc_postcode_area, slc_beneficiary, slc_funder, slc_uoa_name);    
//        _UOAChart.updateUOAChart(result.uoa_counts);
//        _funderChart.updateFunderChart(result.funders_counts, color_bar_Funder, slc_numberFundersLimit);    
//        if (slc_Impact_Beneficiariest === "Global") {
//            _GlobalImactMap.updateGlobalImactMap(mapGlobal, layerGlobal, GlobalBoundary, result.countries_counts, palette_colors_GlobalMap);
//        } else {
//            _UKRegionCountsMap.updateUKregion_counts_map(mapGlobal, clusters_UK_region, result.uk_region_counts);
//        }
//        _UKMap.updateUKMap(mapUK, layerUK, UKPostCodeAreasBoundary, result.institution_counts, palette_colors_UKMap);
//     }).then(() => {
//          _utils.progressMenuOff();
//     }).catch(error => {
//        console.log('In the catch', error);
//     });     
//});


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

$( "#btnTeam" ).on( "click", function() {
    $('#idMdTeam').modal('show');
});

$( "#btnHelp" ).on( "click", function() {
    $('#idMdHelp').modal('show');
});

$( "#label_Assessment_question" ).on( "click", function() {
    $('#idMdAssessmentQuestion').modal('show');
});

$( "#label_Funders_question" ).on( "click", function() {
    $('#idMdFundersQuestion').modal('show');
});

$( "#label_Institutions_question" ).on( "click", function() {
    $('#idMdInstitutionsQuestion').modal('show');
});

$( "#label_Beneficiaries_question" ).on( "click", function() {
    $('#idMdBeneficiariesQuestion').modal('show');
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
                                                    slc_uoa_name,
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
        slc_group_Name = "All Clusters";
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
                slc_uoa_name,
                slc_funder)
    ).then(result => {
        infoboxSelectedUKmap.remove(mapUK); 
        _utils.updateInfoBox(initialData);
        _utils.updateModalInfoBox(initialData);        
        _init.setContactInfo(initialData.website_text.contact);
        _init.setAboutInfo(initialData.website_text.about);
        _utils.updateModalInfoBox(initialData);
        _utils.initialSetLabels(initialData);
        if (slc_uoa_name === null){
           _UOAChart.updateUOAChart(result.uoa_counts);
        }
        _funderChart.updateFunderChart(result.funders_counts, color_bar_Funder, slc_numberFundersLimit);
        if (slc_Impact_Beneficiariest === "Global") {
            _GlobalImactMap.updateGlobalImactMap(mapGlobal, layerGlobal, GlobalBoundary, result.countries_counts, palette_colors_GlobalMap);
        } else {
            _UKRegionCountsMap.updateUKregion_counts_map(mapGlobal, clusters_UK_region, result.uk_region_counts);
        }
        _UKMap.updateUKMap(mapUK, layerUK, UKPostCodeAreasBoundary, result.institution_counts, palette_colors_UKMap);
        _utils.updateLabelsSelectedOptionsBoxs(slc_postcode_area_name, slc_beneficiary, slc_funder, slc_uoa_name);
        total_rows_pagination_meta=result.table_pagination_meta.total_rows;
    }).then(() => {
        document.getElementById('firstloader').style.display = 'none';
    }).catch(error => {
        console.log('In the catch', error);
    });

});

$("#Options_of_Impact_Beneficiariest").change(function (e) {
    e.preventDefault();

    slc_Impact_Beneficiariest = $('#Options_of_Impact_Beneficiariest').children("option:selected").val();

    if (slc_Impact_Beneficiariest === "UK") {
        if (mapGlobal.hasLayer(layerGlobal)) {
            mapGlobal.removeLayer(layerGlobal);
            mapGlobal.removeControl(legendMapGlobal);
        }
        slc_beneficiary="GBR";
        mapGlobal.addLayer(clusters_UK_region);
    } else {
        if (mapGlobal.hasLayer(clusters_UK_region)) {
            mapGlobal.removeLayer(clusters_UK_region);
        }
        mapGlobal.addLayer(layerGlobal);
        mapGlobal.addControl(legendMapGlobal);
        slc_beneficiary=null;
    }

    mapUK.setView(mapUK.options.center, mapUK.options.zoom);
    mapGlobal.setView(mapGlobal.options.center, mapGlobal.options.zoom);

    _utils.progressMenuOn();

    _api.get_ics_data(API_URL,
            slc_threshold,
            slc_topic,
            slc_postcode_area,
            slc_beneficiary,
            slc_uoa,
            slc_uoa_name,
            slc_funder).then(result => {
         infoboxSelectedUKmap.remove(mapUK);                  
        _utils.updateTopicsMenuAvailable(initialData, result.topics_available);                                    
        _utils.updateLabelsSelectedOptionsBoxs(slc_postcode_area_name, slc_beneficiary, slc_funder, slc_uoa_name);   
        _funderChart.updateFunderChart(result.funders_counts, color_bar_Funder, slc_numberFundersLimit); 
        if (slc_uoa_name === null){
           _UOAChart.updateUOAChart(result.uoa_counts);
        }        
        if (slc_Impact_Beneficiariest === "Global") {
            _GlobalImactMap.updateGlobalImactMap(mapGlobal, layerGlobal, GlobalBoundary, result.countries_counts, palette_colors_GlobalMap);
        } else {
            _UKRegionCountsMap.updateUKregion_counts_map(mapGlobal, clusters_UK_region, result.uk_region_counts);
        }
        
        _UKMap.updateUKMap(mapUK, layerUK, UKPostCodeAreasBoundary, result.institution_counts, palette_colors_UKMap);
        total_rows_pagination_meta=result.table_pagination_meta.total_rows;  
    }).then(() => {
        _utils.progressMenuOff();
    }).catch(error => {
        console.log('In the catch', error);
    });

});


var UOAChart = echarts.init(document.getElementById('chartContainer_bottom_left'));

UOAChart.on('click', function(params) {
    
    var selectedAssessment = $('#Options_of_Assessment').children("option:selected").val();
    if (selectedAssessment === "All") return null;

    if (params.name === slc_uoa_name) {
        slc_uoa_name = null;
    }else{
        slc_uoa_name = params.name;
    }
    
        _utils.progressMenuOn();
        
        _api.get_ics_data(API_URL, 
                      slc_threshold,
                      slc_topic,
                      slc_postcode_area,
                      slc_beneficiary,
                      slc_uoa,
                      slc_uoa_name,
                      slc_funder).then(result => {
         infoboxSelectedUKmap.remove(mapUK);                  
        _utils.updateTopicsMenuAvailable(initialData, result.topics_available);                                    
        _utils.updateLabelsSelectedOptionsBoxs(slc_postcode_area_name, slc_beneficiary, slc_funder, slc_uoa_name);   
        _funderChart.updateFunderChart(result.funders_counts, color_bar_Funder, slc_numberFundersLimit); 
        
        if (slc_Impact_Beneficiariest === "Global") {
            _GlobalImactMap.updateGlobalImactMap(mapGlobal, layerGlobal, GlobalBoundary, result.countries_counts, palette_colors_GlobalMap);
        } else {
            _UKRegionCountsMap.updateUKregion_counts_map(mapGlobal, clusters_UK_region, result.uk_region_counts);
        }
        
        _UKMap.updateUKMap(mapUK, layerUK, UKPostCodeAreasBoundary, result.institution_counts, palette_colors_UKMap);
        total_rows_pagination_meta=result.table_pagination_meta.total_rows;        
     }).then(() => {
          _utils.progressMenuOff();
     }).catch(error => {
        console.log('In the catch', error);
     });
    
    
 
});




$("#Options_of_Country_Names").change(function (e) {
    e.preventDefault();
    
    $('[data-bs-toggle="tooltip"]').tooltip('hide'); 
 
    let selected_country_name = $('#Options_of_Country_Names').children("option:selected").val();
    slc_postcode_area = CountryToPC[selected_country_name];
    slc_postcode_area_name = selected_country_name;
    
    _UKMap.reseAllFeatureUKMap(layerUK);

    _utils.progressMenuOn();
    slc_topic = _utils.getActiveTopic();
    _api.get_ics_data(API_URL,
            slc_threshold,
            slc_topic,
            slc_postcode_area,
            slc_beneficiary,
            slc_uoa,
            slc_uoa_name,
            slc_funder).then(result => {
        infoboxSelectedUKmap.remove(mapUK);        
        _UKMap.updateUKMap(mapUK, layerUK, UKPostCodeAreasBoundary, result.institution_counts, palette_colors_UKMap);
        _utils.updateLabelsSelectedOptionsBoxs(slc_postcode_area_name, slc_beneficiary, slc_funder, slc_uoa_name);
        _utils.updateTopicsMenuAvailable(initialData, result.topics_available); 
        
        if (slc_Impact_Beneficiariest === "Global") {
            _GlobalImactMap.updateGlobalImactMap(mapGlobal, layerGlobal, GlobalBoundary, result.countries_counts, palette_colors_GlobalMap);
        } else {
            _UKRegionCountsMap.updateUKregion_counts_map(mapGlobal, clusters_UK_region, result.uk_region_counts);
        }        
        _funderChart.updateFunderChart(result.funders_counts, color_bar_Funder, slc_numberFundersLimit); 
        if (slc_uoa_name === null){
           _UOAChart.updateUOAChart(result.uoa_counts);
        } 
        total_rows_pagination_meta=result.table_pagination_meta.total_rows;
    }).then(() => {
        _utils.progressMenuOff();
    }).catch(error => {
        console.log('In the catch', error);
    });

});


function reset_Individual_Filter(d) {

    if (d === "UOA") {
        //console.log("UOA");
        slc_uoa = null;
        slc_uoa_name = null;
        $('#Options_of_Assessment').prop("selectedIndex", 0);
        document.getElementById("btn_reset_UOA").style.visibility = "hidden";
    } else if (d === "Beneficiaries") {
        //console.log("Beneficiaries");
        slc_beneficiary = null;
        if (mapGlobal.hasLayer(clusters_UK_region)) {
            mapGlobal.removeLayer(clusters_UK_region);
            mapGlobal.addLayer(layerGlobal);
            mapGlobal.addControl(legendMapGlobal);
            slc_Impact_Beneficiariest = "Global";
            mapGlobal.setView(mapGlobal.options.center, mapGlobal.options.zoom);
        }
        $('#Options_of_Impact_Beneficiariest').prop("selectedIndex", 0);
        document.getElementById("btn_reset_Beneficiaries").style.visibility = "hidden";
    } else if (d === "Institutions") {
        //console.log("Institutions");
        infoboxSelectedUKmap.remove(mapUK);
        _UKMap.reseAllFeatureUKMap(layerUK);
        slc_postcode_area = null;
        slc_postcode_area_name = null;
        $('#Options_of_Country_Names').prop("selectedIndex", 0);
        mapUK.setView(mapUK.options.center, mapUK.options.zoom);
        document.getElementById("btn_reset_Institutions").style.visibility = "hidden";
    } else if (d === "Funders") {
        //console.log("Funders");
        slc_funder = null;
        document.getElementById("btn_reset_Funders").style.visibility = "hidden";
    } else {
        return null;
    }

    _utils.progressMenuOn();

    _api.get_ics_data(API_URL,
            slc_threshold,
            slc_topic,
            slc_postcode_area,
            slc_beneficiary,
            slc_uoa,
            slc_uoa_name,
            slc_funder).then(result => {
        infoboxSelectedUKmap.remove(mapUK);
        _utils.updateTopicsMenuAvailable(initialData, result.topics_available); 
        _utils.updateLabelsSelectedOptionsBoxs(slc_postcode_area_name, slc_beneficiary, slc_funder, slc_uoa_name);
        if (slc_uoa_name === null){
           _UOAChart.updateUOAChart(result.uoa_counts);
        } 
        _funderChart.updateFunderChart(result.funders_counts, color_bar_Funder, slc_numberFundersLimit);
        if (slc_Impact_Beneficiariest === "Global") {
            _GlobalImactMap.updateGlobalImactMap(mapGlobal, layerGlobal, GlobalBoundary, result.countries_counts, palette_colors_GlobalMap);
        } else {
            _UKRegionCountsMap.updateUKregion_counts_map(mapGlobal, clusters_UK_region, result.uk_region_counts);
        }
        _UKMap.updateUKMap(mapUK, layerUK, UKPostCodeAreasBoundary, result.institution_counts, palette_colors_UKMap);
        total_rows_pagination_meta = result.table_pagination_meta.total_rows;
    }).then(() => {
        _utils.progressMenuOff();
    }).catch(error => {
        console.log('In the catch', error);
    });


}


$( "#btn_reset_Funders" ).on( "click", function() {
      reset_Individual_Filter("Funders");
});
$( "#btn_reset_Institutions" ).on( "click", function() {
      reset_Individual_Filter("Institutions");
});
$( "#btn_reset_UOA" ).on( "click", function() {
      reset_Individual_Filter("UOA");
});
$( "#btn_reset_Beneficiaries" ).on( "click", function() {
      reset_Individual_Filter("Beneficiaries");
});