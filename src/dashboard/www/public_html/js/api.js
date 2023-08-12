export function getInitData(api_url) {

    if (api_url.substr(-1) !== '/')
        api_url += '/';
    const fullUrl = api_url + 'init';

    var result = "";
    $.ajax({
        url: fullUrl,
        async: false,
        type: 'get',
        dataType: 'json',
        success: function (data) {
            result = data;
        },
        error: function (xhr, ajaxOptions, thrownError) {
            console.log(xhr.status);
            console.log(thrownError);
        }
    });
    return result;
}

export function get_ics_data(api_url,
                             threshold,
                             topic,
                             postcode_area,
                             beneficiary,
                             uoa,
                             funder) {

    if (api_url.substr(-1) !== '/')
        api_url += '/';
    const fullUrl = api_url + 'init';
    
    //const uoa_par = (uoa === "All") ? null : uoa;
    
    let data = {};
    data = {
        threshold: threshold,
        topic: topic,
        postcode_area: postcode_area,
        beneficiary: beneficiary,
        uoa: (uoa === "All") ? null : uoa,
        funder: funder
    };
    $.each(data, function(key, value){
        if (value === "" || value === null){
            delete data[key];
        }
    });    
    

    return new Promise((resolve, reject) => {
        $.ajax({
            url: api_url + "get_ics_data",
            type: 'get',
            data: data,
            beforeSend: function (jqXHR, settings) {
                let url = settings.url + "?" + settings.data;
                //console.log(url);
            },
            success: function (data) {
                resolve(data);
            },
            error: function (error) {
                reject(error);
            }
        });
    });
}


export function getInitData2(api_url) {

    if (api_url.substr(-1) !== '/')
        api_url += '/';
    const fullUrl = api_url + 'init';

    return new Promise((resolve, reject) => {
        $.ajax({
            url: fullUrl,
            async: false,
            type: 'get',
            success: function (data) {
                resolve(data);
            },
            error: function (error) {
                reject(error);
            }
        });
    });

}


export function getGlobalBoundary() {

    var result = "";
    $.ajax({
        url: "./data/global_map.geojson",
        async: false,
        type: 'get',
        dataType: 'json',
        success: function (data) {
            result = data;
        },
        error: function (xhr, ajaxOptions, thrownError) {
            console.log(xhr.status);
            console.log(thrownError);
        }
    });
    return result;
}


export function getUKPostCodeAreasBoundary() {

    var result = "";
    $.ajax({
        url: "./data/UK_postcode_area_v6.geojson",
        async: false,
        type: 'get',
        dataType: 'json',
        success: function (data) {
            result = data;
        },
        error: function (xhr, ajaxOptions, thrownError) {
            console.log(xhr.status);
            console.log(thrownError);
        }
    });
    return result;
}
