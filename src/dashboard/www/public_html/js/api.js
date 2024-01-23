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
        uoa_name,
        funder,
        table_page,
        items_per_page) {

    if (api_url.substr(-1) !== '/')
        api_url += '/';
    const fullUrl = api_url + 'init';

    //const uoa_par = (uoa === "All") ? null : uoa;

    var blCountries_specific = true;
    var elementCountries_specific = document.getElementById('chCountries_specific_extracted');
    if (typeof (elementCountries_specific) !== 'undefined' && elementCountries_specific !== null)
    {
        blCountries_specific = $("#chCountries_specific_extracted").is(":checked");
    }

    var blCountries_union = true;
    var elementCountries_union = document.getElementById('chCountries_union_extracted');
    if (typeof (elementCountries_union) !== 'undefined' && elementCountries_union !== null)
    {
        blCountries_union = $("#chCountries_union_extracted").is(":checked");
    }

    var blCountries_region = true;
    var elementCountries_region = document.getElementById('chCountries_region_extracted');
    if (typeof (elementCountries_region) !== 'undefined' && elementCountries_region !== null)
    {
        blCountries_region = $("#chCountries_region_extracted").is(":checked");
    }

    var blCountries_global = true;
    var elementCountries_global = document.getElementById('chCountries_global_extracted');
    if (typeof (elementCountries_global) !== 'undefined' && elementCountries_global !== null)
    {
        blCountries_global = $("#chCountries_global_extracted").is(":checked");
    }


    let data = {};
    data = {
        threshold: threshold,
        countries_specific_extracted: blCountries_specific,
        countries_union_extracted: blCountries_union,
        countries_region_extracted: blCountries_region,
        countries_global_extracted: blCountries_global,
        topic: topic,
        postcode_area: postcode_area,
        beneficiary: beneficiary,
        uoa: (uoa === "All") ? null : uoa,
        uoa_name: uoa_name,
        funder: funder,
        table_page: table_page,
        items_per_page: items_per_page
    };

    $.each(data, function (key, value) {
        if (value === "" || value === null) {
            delete data[key];
        }
    });


    return new Promise((resolve, reject) => {
        $.ajax({
            url: api_url + "get_ics_data",
            type: 'get',
            data: data,
            traditional: true,
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
        url: "./data/UK_postcode_area_v7.geojson",
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
