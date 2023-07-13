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
    $("#info_box").height(h - 300);
    $("#chart_cardbox_top_left").height(h / 2 - 94);
    $("#chart_cardbox_bottom_left").height(h / 2 - 94);
    $("#map_cardbox_top_right").height(h / 2 - 94);
    $("#map_cardbox_bottom_right").height(h / 2 - 94);


}

export function updateInfoBox(d) {

    return new Promise(function(resolve, reject) {

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
//            $("#info_box_topic_description").text(d.website_text.all_topics_description);
//            $("#info_box_topic_example").text(d.website_text.instructions);
            $("#info_box_topic_title").text("");
            $("#info_box_topic_description").text("Of resolve to gravity thought my prepare chamber so. Unsatiable entreaties collecting may sympathize nay interested instrument. If continue building numerous of at relation in margaret. Lasted engage roused mother an am at. Other early while if by do to. Missed living excuse as be. Cause heard fat above first shall for. My smiling to he removal weather on anxious.");
            $("#info_box_topic_example").text("Of resolve to gravity thought my prepare chamber so. Unsatiable entreaties collecting may sympathize nay interested instrument. If continue building numerous of at relation in margaret. Lasted engage roused mother an am at. Other early while if by do to. Missed living excuse as be. Cause heard fat above first shall for. My smiling to he removal weather on anxious.");
        } else {
            $("#info_box_topic_title").text(found.topic_name);
            $("#info_box_topic_description").html(found.desciption);
            $("#info_box_topic_example").html(found.narrative);
        }
        resolve(true);
    });

}

export function progressMenuOn() {
        document.getElementById("firstloader").style.visibility = 'visible';
        document.getElementById("firstloader").style.display = 'block';
}

export function progressMenuOff() {
        document.getElementById("firstloader").style.visibility = 'hidden';
        document.getElementById("firstloader").style.display = 'none';
}