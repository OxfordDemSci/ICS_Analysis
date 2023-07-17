import * as _country_code_lookup from './country_code_lookup.js?version=1.0'

export function getColor(v, palette) {
    
    if (v === undefined || v === null) {
        return "#EBEBE4";
    }
 
    let xcase = false;
    let color;
    let breaks = palette["breaks"];
    let colors = palette["colors"];
    let lp = breaks.length;

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
    $("#info_box").height(h - 420);
    $("#chart_cardbox_top_left").height(h / 2 - 94);
    $("#chart_cardbox_bottom_left").height(h / 2 - 94);
    $("#map_cardbox_top_right").height(h / 2 - 94);
    $("#map_cardbox_bottom_right").height(h / 2 - 94);
    
}

export function updateLabelsSelectedOptionsBoxs(Institutions, Beneficiaries) {

    let ch_Institutions = true;

    if (typeof Institutions === 'undefined' || Institutions === null) {
        ch_Institutions = false;
    }
    let ch_Beneficiaries = true;

    if (typeof Beneficiaries === 'undefined' || Beneficiaries === null) {
        ch_Beneficiaries = false;
    }


    var eUOA = document.getElementById("Options_of_Assessment");
    var valueUOA = eUOA.options[eUOA.selectedIndex].value;

//
// let label='';
// let label_UOA='UOA';
// let label_Funders='Funders';
//
// 
    if (ch_Institutions || ch_Beneficiaries) {
        document.getElementById("reload_selected_options").style.visibility = "visible";
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
    return new Promise(function(resolve, reject) {
            let rnd_txt = "Some quick example text to build on the card title and make up the bulk of the card's content. Some quick example text to build on the card title and make up the bulk of the card's content.";
            rnd_txt += rnd_txt;
            rnd_txt += rnd_txt;
            $("#dv_startup").html(d.website_text.instructions + rnd_txt);
        resolve(true);
    });

}


export function updateInfoBox(d) {

    return new Promise(function(resolve, reject) {
        
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


