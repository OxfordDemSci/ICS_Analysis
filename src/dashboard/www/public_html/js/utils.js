import * as _country_code_lookup from './country_code_lookup.js?version=1.0'

export function updateTotalImpactCaseStudies(t) {

 document.getElementById('label_total_impact_case_studies').innerHTML = t;
 
}

export function removeSelectedLayer(_map, fname) {

    if (_map) {
        _map.eachLayer(function (layer) {
            if (layer.feature) {
                let n = layer.feature.properties[fname];
                if (typeof n === 'undefined' || n === null) {
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
                            uoa_name,
                            funder) {
                                
    let uri = api_uri + "download_csv?threshold=" + threshold + "&topic=" + topic + "&beneficiary=" + beneficiary + "&uoa=" + uoa + "&uoa_name=" + uoa_name+ "&funder=" + funder;
    if (postcode_area !== null) {
        if (Array.isArray(postcode_area)){
             for (var i = 0; i < postcode_area.length; i++) {
                 uri = uri + "&postcode_area=" + postcode_area[i];
             }
        }else{
            uri = uri + "&postcode_area=" + postcode_area;
        }
    }

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
                               uoa_name,
                               funder) {
    let uri = api_uri + "download_pdf?threshold=" + threshold + "&topic=" + topic + "&beneficiary=" + beneficiary + "&uoa=" + uoa + "&uoa_name=" + uoa_name+ "&funder=" + funder;

    if (postcode_area !== null) {
        if (Array.isArray(postcode_area)){
             for (var i = 0; i < postcode_area.length; i++) {
                 uri = uri + "&postcode_area=" + postcode_area[i];
             }
        }else{
            uri = uri + "&postcode_area=" + postcode_area;
        }
    }    
    
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


export function LoadCurrentICSTable(oResults, _columns_ntitles, _max_txt_lenght) {

    var oTblReport = $("#tblReportResultsICSTabl");
    var max_txt_lenght = _max_txt_lenght;

    var columns_ntitles = [];

    if (_columns_ntitles == null || _columns_ntitles.length === 0) {

        for (var key in oResults[0]) {
            columns_ntitles.push(
                {
                    title: key,
                    data: key
                }
            );
        }

    } else {
        columns_ntitles = _columns_ntitles;
    }


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
                render: function (data, type, row, meta) {

                    if (typeof data === 'undefined') {
                        return;
                    }
                    if (data == null) {
                        return data;
                    }

                    if (data.length > 40) {
                        if (meta.settings.aoColumns[meta.col].title === 'ics_url') {
                            return ('<a href="' + data.toString() + '" target="_blank">' + data.toString().substr(0, 30) + '...</a>');
                        } else {
                            return ('<span title="' + data.toString().substring(0, 500) + '" style="text-overflow: ellipsis;">' + data.toString().substr(0, 38) + '...</span>');
                        }

                    } else {
                        return data;
                    }

                },
                "defaultContent": "",
                targets: "_all"
            },
            {"width": "200px", targets: [0, 1, 2, 3, 26]}],
        "data": oResults,
        "columns": columns_ntitles
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

    if (lp === 1) {
        return colors[0];
    }

    if (breaks[lp - 2] === breaks[lp - 1]) {
        lp--;
        xcase = true;
    }

    for (let i = 0; i < lp - 1; i++) {

        if (v >= breaks[i] && v <= breaks[i + 1]) {
            color = colors[i];
        }
    }

    if (xcase && v >= breaks[lp - 1]) {
        color = colors[lp - 1];
    }

    if (v < breaks[0]) {
        color = colors[0];
    }

    return color;

}

export function setHightBoxs() {

    var h = window.innerHeight;
    $("#info_box").height(h - 194);
    $("#chart_cardbox_top_left").height(h / 2 - 94);
    $("#chart_cardbox_bottom_left").height(h / 2 - 94);
    $("#map_cardbox_top_right").height(h / 2 - 94);
    $("#map_cardbox_bottom_right").height(h / 2 - 94);
    $("#card_Topic_Description").height(h / 2 - 94);
    $("#card_Topic_Description_overflow").height(h / 2 - 145);
    $("#card_Impact_Case_Studies").height(h / 2 - 94);
    $("#card_Impact_Case_Studies_overflow").height(h / 2 - 145);

}

export function updateLabelsSelectedOptionsBoxs(Institutions, Beneficiaries, Funder, UAO_name) {

    let ActiveAssessment = getActiveAssessment();

    let ch_ActiveAssessment = true;

    if (ActiveAssessment === "SHAPE") {
        ch_ActiveAssessment = false;
    }else{
        document.getElementById("btn_reset_UOA").style.visibility = "visible";
    }

    let ch_Institutions = true;

    if (typeof Institutions === 'undefined' || Institutions === null) {
        ch_Institutions = false;
    }else{
            if (Institutions === "All") {
                document.getElementById("btn_reset_Institutions").style.visibility = "hidden";
            }else{
                document.getElementById("btn_reset_Institutions").style.visibility = "visible";
            } 
    }
    


    let ch_Funder = true;

    if (typeof Funder === 'undefined' || Funder === null) {
        ch_Funder = false;
    }else{
        document.getElementById("btn_reset_Funders").style.visibility = "visible";
    }

    let ch_Beneficiaries = true;

    if (typeof Beneficiaries === 'undefined' || Beneficiaries === null) {
        ch_Beneficiaries = false;
    }else{
        document.getElementById("btn_reset_Beneficiaries").style.visibility = "visible";
    }

    let ch_UAO_name = true;

    if (typeof UAO_name === 'undefined' || UAO_name === null) {
        ch_UAO_name = false;
    }else{
        document.getElementById("btn_reset_UOA").style.visibility = "visible";
    }

    var eUOA = document.getElementById("Options_of_Assessment");
    var valueUOA = eUOA.options[eUOA.selectedIndex].value;


// 
    if (ch_Institutions || ch_Beneficiaries || ch_Funder || ch_ActiveAssessment || ch_UAO_name) {
        document.getElementById("reload_selected_options").style.visibility = "visible";
    }

    if (ch_Funder) {
        let instaTextFunder = (Funder != null && Funder.length > 13) ? Funder.substr(0, 16) + " ..." : Funder == null ? "" : Funder;
        document.getElementById('label_selected_Funder').innerHTML = instaTextFunder;
        const tooltipInstance = bootstrap.Tooltip.getInstance(label_selected_Funder);
        tooltipInstance.setContent({'.tooltip-inner': Funder});
    } else {
        document.getElementById('label_selected_Funder').innerHTML = "All";
        const tooltipInstance = bootstrap.Tooltip.getInstance(label_selected_Funder);
        tooltipInstance.setContent({'.tooltip-inner': "All"});
    }

    if (ch_Institutions) {
        document.getElementById('label_selected_Institutions').innerHTML = (Institutions != null && Institutions.length > 8) ? Institutions.substr(0, 8) + " ..." : Institutions == null ? "" : Institutions
        let link_popover_Institutions = document.getElementById('popover_Institutions');
        document.getElementById('label_selected_Institutions').style.textDecoration = "none";
        document.getElementById('label_selected_Institutions').style.cursor = "pointer";
        const tooltipInstance = bootstrap.Tooltip.getInstance(label_selected_Institutions);
        tooltipInstance.setContent({'.tooltip-inner': Institutions});
    } else {
        document.getElementById('label_selected_Institutions').innerHTML = "All";
        let link_popover_Institutions = document.getElementById('popover_Institutions');
        document.getElementById('label_selected_Institutions').style.textDecoration = "none";
        document.getElementById('label_selected_Institutions').style.cursor = "default";
        const tooltipInstance = bootstrap.Tooltip.getInstance(label_selected_Institutions);
        tooltipInstance.setContent({'.tooltip-inner': 'All'});
    }

    let Impact_Beneficiariest_selected = $('#Options_of_Impact_Beneficiariest').children("option:selected").val();
        
    if (Impact_Beneficiariest_selected === "UK") {
            document.getElementById('label_selected_Beneficiaries').innerHTML = "UK";
            const tooltipInstance = bootstrap.Tooltip.getInstance(label_selected_Beneficiaries);
            tooltipInstance.setContent({'.tooltip-inner': "UK"});
    } else {
        
        if (ch_Beneficiaries) {
            let Beneficiaries_name = _country_code_lookup.searchCountryNamebyISO3("iso3", Beneficiaries);
            let Beneficiaries_name_text = 'undefined';
            if( typeof Beneficiaries_name === 'undefined' || Beneficiaries_name === null ){
                Beneficiaries_name_text = 'undefined';
            }else{
                Beneficiaries_name_text = Beneficiaries_name.country;
            }
            
            //document.getElementById('label_selected_Beneficiaries').innerHTML = (Beneficiaries_name.country.length > 7) ? Beneficiaries_name.country.substr(0, 10)+" ..." : Beneficiaries_name.country;
            //const tooltipInstance = bootstrap.Tooltip.getInstance(label_selected_Beneficiaries);
            //tooltipInstance.setContent({'.tooltip-inner': Beneficiaries_name.country});  
            
            document.getElementById('label_selected_Beneficiaries').innerHTML = (Beneficiaries_name_text.length > 7) ? Beneficiaries_name_text.substr(0, 10)+" ..." : Beneficiaries_name_text;
            const tooltipInstance = bootstrap.Tooltip.getInstance(label_selected_Beneficiaries);
            tooltipInstance.setContent({'.tooltip-inner': Beneficiaries_name_text});     
            
        } else {
            document.getElementById('label_selected_Beneficiaries').innerHTML = 'Global';
        }  
        
    }





    document.getElementById('label_selected_Assessment').innerHTML = valueUOA;

    var active_topic = document.querySelector("#idTopics li.active").getAttribute("data-alias");
    document.getElementById('label_selected_Topics').innerHTML = (active_topic.length > 13) ? active_topic.substr(0, 16) + " ..." : active_topic;
    const tooltipInstance = bootstrap.Tooltip.getInstance(label_selected_Topics);
    tooltipInstance.setContent({'.tooltip-inner': active_topic});
    
    
    if (UAO_name === null) {
        document.getElementById('label_selected_UOA').innerHTML = "All";
    }else{
        document.getElementById('label_selected_UOA').innerHTML = (UAO_name.length > 16) ? UAO_name.substr(0, 16) + " ..." : UAO_name;

        const tooltipInstance = bootstrap.Tooltip.getInstance(label_selected_UOA);
        tooltipInstance.setContent({'.tooltip-inner': UAO_name});
    }

}

export function initialSetInfoBox(d) {
    return new Promise(function (resolve, reject) {
        $("#dv_startup").html(d.website_text.all_topics_description);
        resolve(true);
    });

}

export function initialSetLabels(d) {
    return new Promise(function (resolve, reject) {
        $("#label_Funders").html(d.website_text.label_top_left_box);
        $("#label_Institutions").html(d.website_text.label_top_right_box);
        $("#label_UOA").html(d.website_text.label_bottom_left_box);
        $("#label_Beneficiaries").html(d.website_text.label_bottom_right_box);

        resolve(true);
    });

}

function updateModal_Example_Impact_Case_Studies_expand(d) {

    let contectMd = document.getElementById("content_Modal_Example_Impact_Case_Studies_expand");

    let active_topic = getActiveTopicValue();

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

    contectMd.innerHTML = "";

    if (found.narrative) {
        contectMd.innerHTML = contectMd.innerHTML + "<p>" + found.narrative + "</p>";
    }


}

function updateModal_Topic_description_expand(d) {

    let contectMd = document.getElementById("content_Modal_Topic_description_expand");

    let active_topic = getActiveTopicValue();

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
    contectMd.innerHTML = "";

    if (found.description) {
        contectMd.innerHTML = contectMd.innerHTML + "<h6>" + active_topic + "</h6><p>" + found.description + "</p>";
    }


    if (found.keywords) {
        contectMd.innerHTML = contectMd.innerHTML + "<p>Keywords: " + found.keywords + "</p>";
    }

}


export function updateInfoBox(d) {

    return new Promise(function (resolve, reject) {

        var dvStartup_Box = document.getElementById("dv_startup_box");
        var dvDescription_Narrative = document.getElementById("dv_Description_Narrative");

        if (dvStartup_Box.style.display === "block") {
            dvStartup_Box.style.display = "none";
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

            if (dvStartup_Box.style.display === "none") {
                dvStartup_Box.style.display = "block";
            }

            if (dvDescription_Narrative.style.display === "block") {
                dvDescription_Narrative.style.display = "none";
            }

        } else {

            // let description_final = "<h6>" + active_topic + "</h6><p>" + found.description + "</p><p>Keywords: " + found.keywords + "</p>"
            let description_final = "<h6>" + active_topic + "</h6><p>" + found.description + "</p>"
            $("#info_box_topic_description").html(description_final);
            $("#info_box_topic_example").html(found.narrative);
            $("#info_box_topic_keywords").html(found.keywords);
            updateModal_Topic_description_expand(d);
            updateModal_Example_Impact_Case_Studies_expand(d);
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

        contectMd.innerHTML = "";

        if (active_topic === "All Topics") {

            contectMd.innerHTML = d.website_text.all_topics_description;

        } else {

            if (found.description) {
                contectMd.innerHTML = "<p class='lead mb-1'><strong> Topic Description </strong></p>";
                contectMd.innerHTML = contectMd.innerHTML + "<p>" + found.description + "</p>";
            }

            if (found.narrative) {
                contectMd.innerHTML = contectMd.innerHTML + "<p class='lead mb-1'><strong> Example Impact Case Studies </strong></p>";
                contectMd.innerHTML = contectMd.innerHTML + "<p>" + found.narrative + "</p>";
            }

            if (found.keywords) {
                contectMd.innerHTML = contectMd.innerHTML + "<p class='lead mb-1'><strong> Keywords </strong></p>";
                contectMd.innerHTML = contectMd.innerHTML + "<p>" + found.keywords + "</p>";
            }

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
    } else {
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


export function updateAssessmentSelection(data, n = 20) {
    
    var values_category_assessment = [];
    var nmax = data.length;
    let nuse;

    if (nmax < n) {
        nuse = nmax;
    } else {
        nuse = n;
    }    
    
    for (var i = 0; i < nuse; i++) {

        values_category_assessment.push(
            {
                name: data[i]['name'],
                assessment_panel: data[i]['assessment_panel'],
                uoa_count: data[i]['uoa_count']
            }
        );

    }    

    const d = values_category_assessment
        .map((item) => item.assessment_panel)
        .filter((value, index, self) => self.indexOf(value) === index);

    const Assessment_labels_lookup = [
        {name: "SHAPE", label: "SHAPE by UoA"},
        {name: "A", label: "Panel A: Medicine, Health, and Life Sciences"},
        {name: "B", label: "Panel B: Physical Sciences, Engineering, and Mathematics"},
        {name: "C", label: "Panel C: Social Sciences"},
        {name: "D", label: "Panel D: Arts and Humanities"},
        {name: "STEM", label: "All STEM Disciplines"},
        {name: "All", label: "SHAPE by Panel"}
        
    ];

    const list = document.getElementById('Options_of_Assessment');

    list.innerHTML = "";

    d.sort();
    
    list.innerHTML = list.innerHTML +
        '<option value="SHAPE">' + Assessment_labels_lookup.find(({name}) => name === "SHAPE").label + '</option>';    


    // if (d.includes("C") && d.includes("D")){
    //     list.innerHTML = list.innerHTML +
    //                 '<option value="SHAPE">' + Assessment_labels_lookup.find(({ name }) => name === "SHAPE").label + '</option>';
    // }

    for (var i = 0; i < d.length; i++) {

        if (d[i] === 'B' | d[i] === 'A') continue;

        list.innerHTML = list.innerHTML +
            '<option value="' + d[i] + '">' + Assessment_labels_lookup.find(({name}) => name === d[i]).label + '</option>';

    }
    
        list.innerHTML = list.innerHTML +
        '<option value="All">' + Assessment_labels_lookup.find(({name}) => name === "All").label + '</option>';


    // if (d.includes("A") && d.includes("B")){
    //     list.innerHTML = list.innerHTML +
    //                 '<option value="STEM">' + Assessment_labels_lookup.find(({ name }) => name === "STEM").label + '</option>';
    // }

}


export function updateTopicsMenu_single(d, t) {

    let topics_filted_by_group;
    if (t === "All Clusters") {
        topics_filted_by_group = d;
    } else {
        topics_filted_by_group = d.filter(element => (element.topic_group === t));
    }

    const list = document.getElementById('idTopics');
    list.innerHTML = "";
    for (var i = 0; i < topics_filted_by_group.length; i++) {

        if (i === 0) {
            list.innerHTML = list.innerHTML +
                '<li class="list-group-item active" data-alias="' + topics_filted_by_group[i]['topic_name'] + '" >' + topics_filted_by_group[i]['topic_name'] + '</li>';
        } else {
            list.innerHTML = list.innerHTML +
                '<li class="list-group-item" data-alias="' + topics_filted_by_group[i]['topic_name'] + '">' + topics_filted_by_group[i]['topic_name'] + '</li>';
        }
    }

}

export function updateTopicsMenu(d, t) {

    return new Promise((resolve, reject) => {

        let topics_filted_by_group;
        if (t === "All Clusters") {
            topics_filted_by_group = d;
        } else {
            topics_filted_by_group = d.filter(element => (element.topic_group === t));
        }

        $("#idTopics .list-group-item").removeClass("active");
        const list = document.getElementById('idTopics');
        list.innerHTML = "";
        for (var i = 0; i < topics_filted_by_group.length; i++) {

            if (i === 0) {
                list.innerHTML = list.innerHTML +
                    '<li class="list-group-item active" data-alias="' + topics_filted_by_group[i]['topic_name'] + '" >' + topics_filted_by_group[i]['topic_name'] + '</li>';
            } else {
                list.innerHTML = list.innerHTML +
                    '<li class="list-group-item" data-alias="' + topics_filted_by_group[i]['topic_name'] + '">' + topics_filted_by_group[i]['topic_name'] + '</li>';
            }
        }

        resolve(true);
    });
}


  
export function updateTopicsMenuAvailable(d, b) {
    
        var active_topic = document.querySelector("#idTopics li.active").getAttribute("data-alias");
        if (active_topic !== "All Topics") return(true);
        
        let topics_available=true;
        let g = d.topic_groups;
        const groups = document.getElementById('idGroups');

        groups.innerHTML = "";
        groups.innerHTML = groups.innerHTML +
                '<option value="0">All Clusters</option>';
        for (var i = 0; i < g.length; i++) {

            groups.innerHTML = groups.innerHTML +
                    '<option value="' + g[i]['group_id'] + '" >' + g[i]['topic_group'] + '</option>';

        }

        let t = d.topics;

        t.sort(function (a, b) {
            return a.topic_name < b.topic_name ? -1 : a.topic_name > b.topic_name ? 1 : 0;
        });

        t.forEach(function (item, i) {
            if (item.topic_name === "All Topics") {
                t.splice(i, 1);
                t.unshift(item);
            }
        });

        const list = document.getElementById('idTopics');
        list.innerHTML = "";
        for (var i = 0; i < t.length; i++) {

            let topic_name = t[i]['topic_name'];
            
            // searching for the topic in array "b" to check if 
            // topic available or not 
            if (typeof b[topic_name] === 'undefined'){
                topics_available=true;
            }else{
                topics_available=b[topic_name];
            }

            

            if (i === 0) {
                list.innerHTML = list.innerHTML +
                        '<li class="list-group-item active" data-alias="' + t[i]['topic_name'] + '" >' + t[i]['topic_name'] + '</li>';
            } else {
                
                if (topics_available){
                    list.innerHTML = list.innerHTML +
                        '<li class="list-group-item"  data-alias="' + t[i]['topic_name'] + '">' + t[i]['topic_name'] + '</li>';
                }else{
                    list.innerHTML = list.innerHTML +
                        '<li class="list-group-item disabled"  data-alias="' + t[i]['topic_name'] + '">' + t[i]['topic_name'] + '</li>';
                }
                
                
            }
        }

}


export function hide_all_individual_rest_filter_btn() {
    document.getElementById("btn_reset_Funders").style.visibility = "hidden";
    document.getElementById("btn_reset_Institutions").style.visibility = "hidden";
    document.getElementById("btn_reset_Beneficiaries").style.visibility = "hidden";
    document.getElementById("btn_reset_UOA").style.visibility = "hidden";
}
