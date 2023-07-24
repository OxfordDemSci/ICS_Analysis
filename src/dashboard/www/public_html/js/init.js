export function setTopicsMenu(t) {

    return new Promise((resolve, reject) => {
        const list = document.getElementById('idTopics');
        list.innerHTML = "";
        for (var i = 0; i < t.length; i++) {

            if (i === 0) {
                list.innerHTML = list.innerHTML +
                        '<li class="list-group-item active" data-alias="' + t[i]['topic_name'] + '" >' + t[i]['topic_name'] + '</li>';
            } else {
                list.innerHTML = list.innerHTML +
                        '<li class="list-group-item" data-alias="' + t[i]['topic_name'] + '">' + t[i]['topic_name'] + '</li>';
            }
        }
        resolve(true);
    });
}

export function setContactInfo(t) {
   
    document.getElementById('lblContact').innerHTML = t;

}

export function setAboutInfo(t) {
   
    document.getElementById('contentAbout').innerHTML = t;

}

export function setTopicsMenu2(t) {

    const list = document.getElementById('idTopics');
    list.innerHTML = "";
    for (var i = 0; i < t.length; i++) {

        if (i === 0) {
            list.innerHTML = list.innerHTML +
                    '<li class="list-group-item active" data-alias="' + t[i]['topic_name'] + '" >' + t[i]['topic_name'] + '</li>';
        } else {
            list.innerHTML = list.innerHTML +
                    '<li class="list-group-item" data-alias="' + t[i]['topic_name'] + '">' + t[i]['topic_name'] + '</li>';
        }
    }


}


