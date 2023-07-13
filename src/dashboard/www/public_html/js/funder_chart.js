export function updateFunderChart(data, n=20) {
  
    var nmax = data.length;
    let nuse;
    
    if (nmax < n){
        nuse = nmax ;  
    }else{
        nuse = n;
    }


    var values = [];
    var categories = [];
    for (var i = 0; i < nuse-1; i++) {

        values.push(
                data[i]['funder_count']
                );

        categories.push(
                data[i]['funder']
                );
    }

    var optionFunderChart = {
        grid: {
            left: "10%",
            top: "10%",
            right: "5%",
            bottom: "10%",
            containLabel: true
        },
        toolbox: {
            show: true,
            orient: 'vertical',
            left: 'right',
            top: 'center',
            feature: {
                mark: {show: true},
                dataView: {show: true, readOnly: false},
                magicType: {show: true, type: ['line', 'bar']},
                restore: {show: true},
                saveAsImage: {show: true}
            }
        },

        tooltip: {
            trigger: 'axis'
        },

        xAxis: {
            data: categories,
            axisTick: {show: true},
            axisLabel: { show: false },
            splitLine:{ show: false },
            axisLine: { show: true }            
        },
        yAxis: {

        },
        series: [{
                type: 'bar',
                data: values,
                itemStyle: {
                    normal: {
                        color: '#2171b5',
                        opacity: 0.9,
                        label: {
                            show: true,
                            rotate: 90,
                            align: 'left',
                            verticalAlign: 'middle',
                            position: 'insideBottom',
                            distance: 15,
                            color: "#212529",
                            fontSize: 12,
                            formatter: function (d) {
                                return d.name;
                                //return d.name + ' ' + d.data;
                            }
                        }
                    }
                }
            }]
    };

    let chartDom_top_left = document.getElementById("chartContainer_top_left");
    let echart_top_left = echarts.init(chartDom_top_left);
    echart_top_left.setOption(optionFunderChart);
    new ResizeObserver(() => echart_top_left.resize()).observe(chartDom_top_left);

}


export function getInitFunderData(data) {

    var values = [];
    var categories = [];
    for (var i = 0; i < data.length; i++) {

        values.push(
                data[i]['funder_count']
                );

        categories.push(
                data[i]['funder']
                );
    }

   return { values, categories };
}

