export function updateUOAChart(data, n=20) {
    
    var values = [];
    var nmax = data.length;
    let nuse;
    
    if (nmax < n){
        nuse = nmax ;  
    }else{
        nuse = n;
    }

    
    for (var i = 0; i < nuse-1; i++) {

        values.push(
            {value: data[i]['uoa_count'], name: data[i]['name']}    
        );

    }


    var optionUOAChart = {
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
echart_bottom_left.setOption(optionUOAChart);
new ResizeObserver(() => echart_bottom_left.resize()).observe(chartDom_bottom_left);

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

