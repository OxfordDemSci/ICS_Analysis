import * as _country_code_lookup from './country_code_lookup.js?version=1.0'

export function removeSelectedLayer(_map, fname) {
  
    if (_map) {

        _map.eachLayer(function (layer) {
            if (layer.feature) {

                let n = layer.feature.properties[fname];

                if( typeof n === 'undefined' || n === null ){

                    _map.removeLayer(layer);

                }
            }
        });
    }
}

export function downloadURI(api_uri, 
                            name, 
                            threshold, 
                            topic, 
                            postcode_area, 
                            beneficiary, 
                            uoa, 
                            funder) 
{
    let uri =  api_uri + "download_csv?threshold="+threshold+"&topic="+topic+"&postcode_area="+postcode_area+"&beneficiary="+beneficiary+"&uoa="+uoa+"&funder="+funder;
    var link = document.createElement("a");
    link.setAttribute('download', name);
    link.href = uri;
    document.body.appendChild(link);
    link.click();
    link.remove();
}

export function GenerateReport(api_uri, 
                            name, 
                            threshold, 
                            topic, 
                            postcode_area, 
                            beneficiary, 
                            uoa, 
                            funder) 
{
    let uri =  api_uri + "download_pdf?threshold="+threshold+"&topic="+topic+"&postcode_area="+postcode_area+"&beneficiary="+beneficiary+"&uoa="+uoa+"&funder="+funder;
    var link = document.createElement("a");
    link.setAttribute('download', name);
    link.href = uri;
    document.body.appendChild(link);
    link.click();
    link.remove();
}

function touchHandler(e) {
    if (!isResizing)
        return;

    var x = e.touches[0].clientX;
    var y = e.touches[0].clientY;

    const container_tbl = $("#tblBottom");
    var container_scrollHead = document.getElementsByClassName('dataTables_scrollHead')[0];
    var container_filter = document.getElementsByClassName('dataTables_filter')[0];

    const height_tbl = $('#topNavbarDiv').outerHeight() + $('#map').height() - container_scrollHead.offsetHeight - container_filter.offsetHeight - y;
    var offsetRight = $('#map').height() + $('#topNavbarDiv').outerHeight() - y;

    $('#tblBottom').DataTable(
            {
                paging: true,
                bInfo: false,
                scrollY: height_tbl,
                bDestroy: true,
                deferRender: true,
                scroller: true,
                "responsive": true,
                "sScrollX": "100%",
                "scrollCollapse": true
            }
    );

    container_table.setAttribute("style", "height:" + offsetRight + "px");
}   

export function ResiseICSTable() {

    const height_tbl = $('#ics_table_all_modal').outerHeight() - 300;
    var oTblReport = $("#tblReportResultsICSTabl");

    if ($.fn.DataTable.isDataTable('#tblReportResultsICSTabl')) {

        oTblReport.DataTable(
                {
                    pageLength: 50,
                    autoWidth: false,
                    paging: true,
                    bInfo: false,
                    scrollY: height_tbl,
                    bDestroy: true,
                    deferRender: true,
                    scroller: true,
                    responsive: true,
                    sScrollX: "100%",
                    "scrollCollapse": false
                }
        );

    }
}


  
export function LoadCurrentICSTable(oResults) {

    var oTblReport = $("#tblReportResultsICSTabl");

    // reinitialize the datatable
    if ($.fn.DataTable.isDataTable('#tblReportResultsICSTabl')) {
        $('#tblReportResultsICSTabl').dataTable().fnClearTable();
        $('#tblReportResultsICSTabl').dataTable().fnDestroy();
    }

    const height_tbl = $('#ics_table_all_modal').outerHeight() - 300;

    oTblReport.DataTable({
        autowidth: false,
        sScrollX: true,
        "pageLength": 50,
        "scrollY": height_tbl,
        "bInfo": false,
        "deferRender": true,
        "scrollCollapse": true,
        "scroller": true,
        "searching": false,
        "paging": true,
        "info": false,
        "columnDefs": [
            {
                render: $.fn.dataTable.render.ellipsis(18),
                targets: "_all"
            },
            {"width": "200px", targets: [0, 1, 2, 3, 26]}],

        "data": oResults,
        "columns": [
            {title: "id", "data": "id"},
            {title: "ics_id", "data": "ics_id"},
            {title: "ukprn", "data": "ukprn"},
            {title: "main_panel", "data": "main_panel"},
            {title: "unit_of_assessment_name", "data": "unit_of_assessment_name"},
            {title: "unit_of_assessment_number", "data": "unit_of_assessment_number"},
            {title: "countries", "data": "countries", width: "200px"},
            {title: "COVID statement", "data": "covid_statement"},
            {title: "cultural", "data": "cultural"},
            {title: "details_of_the_impact", "data": "details_of_the_impact"},
            {title: "economic", "data": "economic"},
            {title: "environmental", "data": "environmental"},
            {title: "formal_partners", "data": "formal_partners"},
            {title: "funders", "data": "funders"},
            {title: "funding_programmes", "data": "funding_programmes"},
            {title: "global_research_identifiers", "data": "global_research_identifiers"},
            {title: "grant_funding", "data": "grant_funding"},
            {title: "health", "data": "health"},
            {title: "id", "data": "id"},
            {title: "inst_postcode", "data": "inst_postcode"},
            {title: "inst_postcode_district", "data": "inst_postcode_district"},
            {title: "institution_name", "data": "institution_name"},
            {title: "is_continued_from_2014", "data": "is_continued_from_2014"},
            {title: "joint_submission", "data": "joint_submission"},
            {title: "legal", "data": "legal"},
            {title: "multiple_submission_letter", "data": "multiple_submission_letter"},
            {title: "multiple_submission_name", "data": "multiple_submission_name"},
            {title: "political", "data": "political"},
            {title: "postcode", "data": "postcode"},
            {title: "references_to_the_research", "data": "references_to_the_research"},
            {title: "researcher_orcids", "data": "researcher_orcids"},
            {title: "societal", "data": "societal"},
            {title: "sources_to_corroborate_the_impact", "data": "sources_to_corroborate_the_impact"},
            {title: "summary_impact_type", "data": "summary_impact_type"},
            {title: "summary_of_the_impact", "data": "summary_of_the_impact"},
            {title: "summary_of_the_impact_topic", "data": "summary_of_the_impact_topic"},
            {title: "technological", "data": "technological"},
            {title: "title", "data": "title"},
            {title: "uoa", "data": "uoa"}
        ]
    });

    $($.fn.dataTable.tables(true)).DataTable().columns.adjust();
}


export function getColor(v, palette) {
    
    if (v === undefined || v === null) {
        return "#EBEBE4";
    }
 
    let xcase = false;
    let color;
    let breaks = palette["breaks"];
    let colors = palette["colors"];
    let lp = breaks.length;
    
    if (lp === 1){
        return colors[0];
    }

    if (breaks[lp - 2] === breaks[lp - 1]) {
        lp--;
        xcase = true;
    } 

    for (let i = 0; i < lp-1 ; i++) {

            if (v >= breaks[i] && v <= breaks[i + 1]) {
                color = colors[i];
            }
    }

    if (xcase && v >= breaks[lp-1]) {
         color = colors[lp-1];
    }
    
    if (v < breaks[0]) {
         color = colors[0];
    }      

    return color;

}

export function setHightBoxs() {

    var h = window.innerHeight;
    $("#info_box").height(h - 457);
    $("#chart_cardbox_top_left").height(h / 2 - 94);
    $("#chart_cardbox_bottom_left").height(h / 2 - 94);
    $("#map_cardbox_top_right").height(h / 2 - 94);
    $("#map_cardbox_bottom_right").height(h / 2 - 94);
    
}

export function updateLabelsSelectedOptionsBoxs(Institutions, Beneficiaries, Funder) {
    
    let ActiveAssessment = getActiveAssessment();
    
    let ch_ActiveAssessment = true;
    
    if (ActiveAssessment === "All") {
        ch_ActiveAssessment = false;
    }     

    let ch_Institutions = true;

    if (typeof Institutions === 'undefined' || Institutions === null) {
        ch_Institutions = false;
    }
    
    let ch_Funder = true;
    
    if (typeof Funder === 'undefined' || Funder === null) {
        ch_Funder = false;
    }    
    
    let ch_Beneficiaries = true;

    if (typeof Beneficiaries === 'undefined' || Beneficiaries === null) {
        ch_Beneficiaries = false;
    }


    var eUOA = document.getElementById("Options_of_Assessment");
    var valueUOA = eUOA.options[eUOA.selectedIndex].value;


// 
    if (ch_Institutions || ch_Beneficiaries || ch_Funder || ch_ActiveAssessment) {
        document.getElementById("reload_selected_options").style.visibility = "visible";
    }
    
    if (ch_Funder) {
        
        let instaTextFunder = (Funder != null && Funder.length > 13) ? Funder.substr(0, 16)+"..." : Funder == null?"":Funder;
        
        document.getElementById('label_selected_Funder').innerHTML = instaTextFunder;
        
        const tooltipInstance = bootstrap.Tooltip.getInstance(label_selected_Funder);
        tooltipInstance.setContent({ '.tooltip-inner': Funder});         
    }else{
        document.getElementById('label_selected_Funder').innerHTML = "All";
        const tooltipInstance = bootstrap.Tooltip.getInstance(label_selected_Funder);
        tooltipInstance.setContent({ '.tooltip-inner': "All"});           
    }    

    if (ch_Institutions) {
        document.getElementById('label_selected_Institutions').innerHTML = Institutions;
        let link_popover_Institutions = document.getElementById('popover_Institutions');
        document.getElementById('label_selected_Institutions').style.textDecoration = "underline";
        document.getElementById('label_selected_Institutions').style.cursor = "pointer";
    } else {

        document.getElementById('label_selected_Institutions').innerHTML = "All in UK";
        let link_popover_Institutions = document.getElementById('popover_Institutions');
        document.getElementById('label_selected_Institutions').style.textDecoration = "none";
        document.getElementById('label_selected_Institutions').style.cursor = "default";

    }

    if (ch_Beneficiaries) {
        let Beneficiaries_name = _country_code_lookup.searchCountryNamebyISO3("iso3", Beneficiaries);
        document.getElementById('label_selected_Beneficiaries').innerHTML = Beneficiaries_name.country;
    }else{
        document.getElementById('label_selected_Beneficiaries').innerHTML = 'Global';
    }

    document.getElementById('label_selected_Assessment').innerHTML = valueUOA;

    var active_topic = document.querySelector("#idTopics li.active").getAttribute("data-alias");
    document.getElementById('label_selected_Topics').innerHTML = active_topic;

}

export function initialSetInfoBox(d) {
    return new Promise(function (resolve, reject) {
        let rnd_txt = "";
        //rnd_txt += rnd_txt;
        //rnd_txt += rnd_txt;
        $("#dv_startup").html(d.website_text.instructions + rnd_txt);
        resolve(true);
    });

}


export function updateInfoBox(d) {

    return new Promise(function (resolve, reject) {

        var dvStartup = document.getElementById("dv_startup");
        var dvDescription_Narrative = document.getElementById("dv_Description_Narrative");

        if (dvStartup.style.display === "block") {
            dvStartup.style.display = "none";
        }

        if (dvDescription_Narrative.style.display === "none") {
            dvDescription_Narrative.style.display = "block";
        }

        var active_topic = document.querySelector("#idTopics li.active").getAttribute("data-alias");

        var topics = d.topics;
        var index = 0;
        var found;
        var entry;
        for (index = 0; index < topics.length; ++index) {
            entry = topics[index];
            if (entry.topic_name === active_topic) {
                found = entry;
                break;
            }
        }
        if (active_topic === "All Topics") {

            if (dvStartup.style.display === "none") {
                dvStartup.style.display = "block";
            }

            if (dvDescription_Narrative.style.display === "block") {
                dvDescription_Narrative.style.display = "none";
            }

        } else {

            $("#info_box_topic_description").html(found.desciption);
            $("#info_box_topic_example").html(found.narrative);
        }
        resolve(true);
    });

}

export function updateModalInfoBox(d) {

    return new Promise(function (resolve, reject) {

        let titleMd = document.getElementById("ModalViewDetailsInfoBoxLabel");
        let contectMd = document.getElementById("contectforViewDetailsInfoBox");

        let active_topic = getActiveTopicValue();

        titleMd.innerText = active_topic;

        var topics = d.topics;
        var index = 0;
        var found;
        var entry;
        for (index = 0; index < topics.length; ++index) {
            entry = topics[index];
            if (entry.topic_name === active_topic) {
                found = entry;
                break;
            }
        }
        if (active_topic === "All Topics") {

            contectMd.innerHTML = d.website_text.instructions;

        } else {
            contectMd.innerHTML = "<p class='lead mb-1'><strong> Description </strong></p>";
            contectMd.innerHTML = contectMd.innerHTML + "<p>" + found.description + "</p>";
            contectMd.innerHTML = contectMd.innerHTML + "<p class='lead mb-1'><strong> Narrative </strong></p>";
            contectMd.innerHTML = contectMd.innerHTML + "<p>" + found.narrative + "</p>";
            contectMd.innerHTML = contectMd.innerHTML + "<p>1. This is instruction ONE; 2. This is instruction TWO; 3. This is instruction N. Some quick example text to build on the card title and make up the bulk of the card's content. Some quick example text to build on the card title and make up the bulk of the card's content.Some quick example text to build on the card title and make up the bulk of the card's content. Some quick example text to build on the card title and make up the bulk of the card's content.Some quick example text to build on the card title and make up the bulk of the card's content. Some quick example text to build on the card title and make up the bulk of the card's content.Some quick example text to build on the card title and make up the bulk of the card's content. Some quick example text to build on the card title and make up the bulk of the card's content.1. This is instruction ONE; 2. This is instruction TWO; 3. This is instruction N. Some quick example text to build on the card title and make up the bulk of the card's content. Some quick example text to build on the card title and make up the bulk of the card's content.Some quick example text to build on the card title and make up the bulk of the card's content. Some quick example text to build on the card title and make up the bulk of the card's content.Some quick example text to build on the card title and make up the bulk of the card's content. Some quick example text to build on the card title and make up the bulk of the card's content.Some quick example text to build on the card title and make up the bulk of the card's content. Some quick example text to build on the card title and make up the bulk of the card's contentThis is instruction ONE; 2. This is instruction TWO; 3. This is instruction N. Some quick example text to build on the card title and make up the bulk of the card's content. Some quick example text to build on the card title and make up the bulk of the card's content.Some quick example text to build on the card title and make up the bulk of the card's content. Some quick example text to build on the card title and make up the bulk of the card's content.Some quick example text to build on the card title and make up the bulk of the card's content. Some quick example text to build on the card title and make up the bulk of the card's content.Some quick example text to build on the card title and make up the bulk of the card's content. Some quick example text to build on the card title and make up the bulk of the card's content.1. This is instruction ONE; 2. This is instruction TWO; 3. This is instruction N. Some quick example text to build on the card title and make up the bulk of the card's content. Some quick example text to build on the card title and make up the bulk of the card's content.Some quick example text to build on the card title and make up the bulk of the card's content. Some quick example text to build on the card title and make up the bulk of the card's content.Some quick example text to build on the card title and make up the bulk of the card's content. Some quick example text to build on the card title and make up the bulk of the card's content.Some quick example text to build on the card title and make up the bulk of the card's content. Some quick example text to build on the card title and make up the bulk of the card's contentThis is instruction ONE; 2. This is instruction TWO; 3. This is instruction N. Some quick example text to build on the card title and make up the bulk of the card's content. Some quick example text to build on the card title and make up the bulk of the card's content.Some quick example text to build on the card title and make up the bulk of the card's content. Some quick example text to build on the card title and make up the bulk of the card's content.Some quick example text to build on the card title and make up the bulk of the card's content. Some quick example text to build on the card title and make up the bulk of the card's content.Some quick example text to build on the card title and make up the bulk of the card's content. Some quick example text to build on the card title and make up the bulk of the card's content.1. This is instruction ONE; 2. This is instruction TWO; 3. This is instruction N. Some quick example text to build on the card title and make up the bulk of the card's content. Some quick example text to build on the card title and make up the bulk of the card's content.Some quick example text to build on the card title and make up the bulk of the card's content. Some quick example text to build on the card title and make up the bulk of the card's content.Some quick example text to build on the card title and make up the bulk of the card's content. Some quick example text to build on the card title and make up the bulk of the card's content.Some quick example text to build on the card title and make up the bulk of the card's content. Some quick example text to build on the card title and make up the bulk of the card's content.</p>";
        }
        resolve(true);
    });

}

export function getActiveAssessment() {
        var eUOA = document.getElementById("Options_of_Assessment");
        var valueUOA = eUOA.options[eUOA.selectedIndex].value;
        return valueUOA;
}

export function getActiveTopic() {
    
        var active_topic = document.querySelector("#idTopics li.active").getAttribute("data-alias");
        
        if (active_topic === "All Topics") {
            return null;
        }else{
            return active_topic;
        }        
}

export function getActiveTopicValue() {
        var active_topic = document.querySelector("#idTopics li.active").getAttribute("data-alias");
        return active_topic;
}

export function progressMenuOn() {
        document.getElementById("firstloader").style.visibility = 'visible';
        document.getElementById("firstloader").style.display = 'block';
}

export function progressMenuOff() {
        document.getElementById("firstloader").style.visibility = 'hidden';
        document.getElementById("firstloader").style.display = 'none';
}


export function updateAssessmentSelection(d) {
  
    const list = document.getElementById('Options_of_Assessment');
    
    list.innerHTML = "";
    
    d.sort();
    
    list.innerHTML = list.innerHTML +
                    '<option value="All">All</option>';
    
    for (var i = 0; i < d.length; i++) {

            list.innerHTML = list.innerHTML +
                    '<option value="' + d[i] + '">' + d[i] + '</option>';
      
    }
      
    if (d.includes("A") && d.includes("B")){
        list.innerHTML = list.innerHTML +
                    '<option value="STEM">STEM</option>';
    }  
 
    if (d.includes("C") && d.includes("D")){
        list.innerHTML = list.innerHTML +
                    '<option value="SHAPE">SHAPE</option>';
    }      
}



