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

export function get_ics_data(api_url, topic = "All Topics", threshold = 0.5, postcode_area = null) {

    if (api_url.substr(-1) !== '/')
        api_url += '/';
    const fullUrl = api_url + 'init';

    let data = {};
    if (postcode_area === undefined || postcode_area === null) {
        data = {
            topic: topic,
            threshold: threshold
        };
    } else {
        data = {
            topic: topic,
            threshold: threshold,
            postcode_area: postcode_area
        };
    }


    return new Promise((resolve, reject) => {
        $.ajax({
            url: api_url + "get_ics_data",
            type: 'get',
            data: data,
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
        url: "./data/UK_postcode_area_v2.geojson",
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
