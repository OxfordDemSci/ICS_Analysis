import * as _utils from './utils.js?version=2.6'
import * as _quartile from './quartile.js?version=1'

// let palette_colors = ["#fff5f0", "#fff5f0", "#fee0d2", "#fcbba1", "#fc9272", "#fb6a4a", "#ef3b2c", "#cb181d", "#a50f15", "#67000d"];
// let palette_colors= ["#002147", "#3B6367", "#626142", "#B67831", "#BA472E"];
// let palette_colors = ["#1e466e", "#376795", "#528fad", "#72bcd5", "#aadce0", "#ffe6b7", "#ffd06f", "#f7aa58", "#ef8a47", "#e76254"]
// let palette_colors = ["#e76254", "#aadce0", "#ef8a47", "#72bcd5", "#f7aa58", "#528fad", "#ffd06f", "#376795", "#ffe6b7", "#1e466e"]
let palette_colors = ["#e76254", "#ef8a47", "#f7aa58", "#ffd06f", "#ffe6b7", "#aadce0", "#72bcd5", "#528fad", "#376795", "#1e466e"]

function getMaxOfJson(jsonalreadyparsed, property) {
    var max = null;
    for (var i = 0; i < jsonalreadyparsed.length; i++) {

        if (max == null) {

            max = jsonalreadyparsed[i][property];

        } else {

            if (parseFloat(jsonalreadyparsed[i][property]) > max) {

                max = jsonalreadyparsed[i][property];

            }

        }

    }
    return max;
}

function getMinOfJson(jsonalreadyparsed, property) {
    var min = null;
    for (var i = 0; i < jsonalreadyparsed.length; i++) {

        if (min == null) {

            min = jsonalreadyparsed[i][property];

        } else {

            if (parseFloat(jsonalreadyparsed[i][property]) < min) {

                min = jsonalreadyparsed[i][property];

            }

        }

    }
    return min;
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

function uniqueArray(arr) {
    var a = [];
    for (var i = 0, l = arr.length; i < l; i++)
        if (a.indexOf(arr[i]) === -1 && arr[i] !== '')
            a.push(arr[i]);
    return a;
}

export function getPaletteQuartile(dt, palette_colors) {

    let breaks = [];
    let cont = 1;
    let Quartile;


    for (var i = 0; i < 10; i++) {
        Quartile = Math.round(_quartile.Quartile(dt, cont * 0.1));
        breaks.push(Quartile);
        cont++;
    }

    let breaks_unique = uniqueArray(breaks);

    let palette_final = [];
    let diference = palette_colors.length - breaks_unique.length;
    for (var i = 0; i < breaks_unique.length; i++) {
             palette_final.push(
                    palette_colors[i+diference]
            );
    }  
    let palette = {"breaks":breaks_unique, "colors":palette_final};
    
    //console.log(palette);
   
    return palette;

}

function find_in_object(my_object, my_criteria) {

    return my_object.filter(function (obj) {
        return Object.keys(my_criteria).every(function (c) {
            return obj[c] == my_criteria[c];
        });
    });
}

export function updateUOAChart_all_Assessment(data, n = 20) {

    var values = [];
    var nmax = data.length;
    let nuse;

    if (nmax < n) {
        nuse = nmax;
    } else {
        nuse = n;
    }


//    data = data.filter(value => value.uoa_count > 0);
//    console.log(data); 

    for (var i = 0; i < nuse; i++) {

        values.push(
            {
                name: data[i]['name'],
                assessment_panel: data[i]['assessment_panel'],
                uoa_count: data[i]['uoa_count']
            }
        );

    }


    const category_assessment = values
        .map((item) => item.assessment_panel)
        .filter((value, index, self) => self.indexOf(value) === index);


    const onlyUnique_name = values
        .map((item) => item.name)
        .filter((value, index, self) => self.indexOf(value) === index);

    _utils.updateAssessmentSelection(category_assessment);

    var my_json = JSON.stringify(data);

    var data_json = JSON.parse(JSON.stringify(data));
    let new_array = [];
    let new_series = [];

    var all_values = [];
    for (var i = 0; i < onlyUnique_name.length; i++) {
        for (var j = 0; j < category_assessment.length; j++) {
            var data_filter = data_json.filter(element => (element.name === onlyUnique_name[i] && element.assessment_panel === category_assessment[j]));
            if (data_filter.length > 0) {
                all_values.push(data_filter[0].uoa_count);
            }
        }
    }


    let palette_colors_final = getPaletteQuartile(all_values, palette_colors);


    for (var i = 0; i < onlyUnique_name.length; i++) {

        let values_array = [];
        for (var j = 0; j < category_assessment.length; j++) {

            var data_filter = data_json.filter(element => (element.name === onlyUnique_name[i] && element.assessment_panel === category_assessment[j]));
            if (data_filter.length > 0) {
                values_array.push(data_filter[0].uoa_count);
            } else {
                values_array.push(0);
            }

        }


        new_array.push(
            {category: category_assessment[i], values: values_array}
        );

        new_series.push(
            {
                name: onlyUnique_name[i],
                type: 'bar',
                stack: 'total',
                label: {
                    show: true
                },
                emphasis: {
                    focus: 'series'
                },
                data: values_array.map(function (val, i) {
                    return val === 0 ? null : val;
                }),
                itemStyle: {
                    color: (seriesIndex) => getColor(seriesIndex.value, palette_colors_final)
                }
            }
        );


    }

    var optionUOAChart = {
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                // Use axis to trigger tooltip
                type: 'shadow' // 'shadow' as default; can also be 'line' or 'shadow'
            },
            formatter: function (params) {
                var output = params[0].axisValueLabel + '<br/>';
                
                let cnt = 1;

                output += '<table class="w-full">';
                
                //params.reverse().forEach(function (param) {
                params.forEach(function (param) {
                    
                    if (param.value > 0 && cnt <= 10) {
                        cnt++;
                        output += `<tr>
              <td style="width: 25px;"><span style="background-color: ${param.color};  height: 15px;width: 15px;border-radius: 50%;display: inline-block;"></span></td>
              <td>${param.seriesName}</td>
              <td class="fw-bold" style="padding-left: 15px !important;">${param.value}</td>
            </tr>`;
                    }
                    
                });

                return output + '</table>';
            }
        },
        grid: {
            left: '8%',
            right: '4%',
            bottom: '10%',
            containLabel: true
        },
        xAxis: {
            type: 'value',
            axisLabel: {show: true},
            name: 'Submissions',
            nameLocation: 'middle',
            nameGap: 30
        },
        yAxis: {
            realtimeSort: true,
            type: 'category',
            data: category_assessment,
            axisLabel: {show: true},
            name: 'Main Panel',
            nameLocation: 'middle',
            nameGap: 30
        },
        transform: {
            type: 'sort',
            config: [
                {dimension: 'category', order: 'desc'}
            ]
        },
        series: new_series
    };


    let chartDom_bottom_left = document.getElementById("chartContainer_bottom_left");
    let echart_bottom_left = echarts.init(chartDom_bottom_left);
    echart_bottom_left.setOption(optionUOAChart, true);
    new ResizeObserver(() => echart_bottom_left.resize()).observe(chartDom_bottom_left);

}


export function updateUOAChart_selected_Assessment(data, n = 20) {

    var values = [];
    var nmax = data.length;
    let nuse;

    if (nmax < n) {
        nuse = nmax;
    } else {
        nuse = n;
    }


    for (var i = 0; i < nuse; i++) {

        values.push(
            {value: data[i]['uoa_count'], name: data[i]['name']}
        );

    }


    var optionUOAChart =
        {
            visualMap: [
                {
                    type: 'continuous',
                    min: getMinOfJson(values, "value"),
                    max: getMaxOfJson(values, "value"),
                    inRange: {
                        color: palette_colors
                    },
                    show: false
                }
            ],
            tooltip: {
                trigger: 'item'
            },
            grid: {
                containLabel: true,
                left: 0,
                top: '50%',
                right: 0,
                bottom: '10%'
            },
            toolbox: {
                show: true,
                orient: 'vertical',
                left: 'right',
                top: 'center',
                feature: {
                    mark: {show: true},
                    dataView: {show: true, readOnly: false},
                    saveAsImage: {show: true}
                }
            },
            labelLine: {
                normal: {
                    show: true
                }
            },
            series: [
                {
                    name: 'Impact Case Studies submitted',
                    type: 'pie',
                    radius: ['40%', '70%'],
                    center: ['50%', '50%'],
                    itemStyle: {
                        borderRadius: 10,
                        borderColor: '#fff',
                        borderWidth: 2
                    },
                    data: values,
                    emphasis: {
                        itemStyle: {
                            shadowBlur: 10,
                            shadowOffsetX: 0,
                            shadowColor: 'rgba(0, 0, 0, 0.5)'
                        }
                    }
                }
            ]
        };

//  color: ["#fff5f0", "#fff5f0", "#fee0d2", "#fcbba1", "#fc9272", "#fb6a4a", "#ef3b2c", "#cb181d", "#a50f15", "#67000d"]

    let chartDom_bottom_left = document.getElementById("chartContainer_bottom_left");
    let echart_bottom_left = echarts.init(chartDom_bottom_left);
    echart_bottom_left.setOption(optionUOAChart, true);
    new ResizeObserver(() => echart_bottom_left.resize()).observe(chartDom_bottom_left);
}


export function updateUOAChart(data, n = 20) {

    let ActiveAssessment = _utils.getActiveAssessment();

    if (ActiveAssessment !== "All") {
        updateUOAChart_selected_Assessment(data, n = 20);
    } else {
        updateUOAChart_all_Assessment(data, n);
    }

}


export function getInitUOAData(data) {

    var values = [];
    for (var i = 0; i < data.length; i++) {

        values.push(
            {value: data[i]['uoa_count'], name: data[i]['name']}
        );

    }

    return values;
}

