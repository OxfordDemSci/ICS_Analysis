import * as _utils from './utils.js?version=2.5'

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


    for (var i = 0; i < nuse ; i++) {

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


 


    var my_json = JSON.stringify(data);

    var data_json = JSON.parse(JSON.stringify(data));
    let new_array = [];
    let new_series = [];


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
                    data: values_array
                }
        );


    }

    
    var optionUOAChart = {
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                // Use axis to trigger tooltip
                type: 'shadow' // 'shadow' as default; can also be 'line' or 'shadow'
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'value'
        },
        yAxis: {
            type: 'category',
            data: category_assessment
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


    for (var i = 0; i < nuse - 1; i++) {

        values.push(
                {value: data[i]['uoa_count'], name: data[i]['name']}
        );

    }


    var optionUOAChart =
            {
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
                        name: 'UOA',
                        type: 'pie',
                        radius: '50%',
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

