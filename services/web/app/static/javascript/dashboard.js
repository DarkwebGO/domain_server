mcw_label = mcw_label.match(/[a-zA-z]+\b/g); //.replace(/&#39;/g, "'")
mcw_count = mcw_count.match(/\d+/g).map(Number);
min_per = Math.round(min_per);
se_per = Math.round(se_per);
yu_per = Math.round(yu_per);

// Slidebar Toggle
var slidebarOpen = false;
var Slidebar = document.getElementById("sidebar");

var openSidebar = () => {
    if (!slidebarOpen) {
        Slidebar.classList.add("slide-responsive");
        slidebarOpen = true;
    }
}

var closeSidebar = () => {
    if (slidebarOpen) {
        Slidebar.classList.remove("slide-responsive");
        slidebarOpen = false;
    }
}

// charts
// angle chart
var angleChartOptions_min = {
    chart: {
        height: 250,
        width: 200,
        type: "radialBar",
    },
    series: [Math.round(min_per)],
    colors: ["#75A47F"],
    plotOptions: {
        radialBar: {
            startAngle: -90,
            endAngle: 90,
            track: {
                background: '#C7C8CC',
                startAngle: -90,
                endAngle: 90,
            },
            dataLabels: {
                name: {
                    show: false,
                },
                value: {
                    fontSize: "19px",
                    offsetY: -5,
                    show: true
                }
            }
        }
    },
    fill: {
        type: "gradient",
        gradient: {
            shade: "dark",
            type: "horizontal",
            gradientToColors: ["#BACD92"],
            stops: [0, 100]
        }
    },
    stroke: {
        lineCap: "butt"
    },
    labels: ["Progress"]
};
var angleChart_min = new ApexCharts(document.querySelector("#angle-chart-min"), angleChartOptions_min);
angleChart_min.render();

var angleChartOptions_se = {
    chart: {
        height: 250,
        width: 200,
        type: "radialBar",
    },
    series: [se_per],
    colors: ["#A79277"],
    plotOptions: {
        radialBar: {
            startAngle: -90,
            endAngle: 90,
            track: {
                background: '#C7C8CC',
                startAngle: -90,
                endAngle: 90,
            },
            dataLabels: {
                name: {
                    show: false,
                },
                value: {
                    fontSize: "19px",
                    offsetY: -5,
                    show: true
                }
            }
        }
    },
    fill: {
        type: "gradient",
        gradient: {
            shade: "dark",
            type: "horizontal",
            gradientToColors: ["#D1BB9E"],
            stops: [0, 100]
        }
    },
    stroke: {
        lineCap: "butt"
    },
    labels: ["Progress"]
};
var angleChart_se = new ApexCharts(document.querySelector("#angle-chart-se"), angleChartOptions_se);
angleChart_se.render();

var angleChartOptions_yu = {
    chart: {
        height: 250,
        width: 200,
        type: "radialBar",
    },
    series: [yu_per],
    colors: ["#80BCBD"],
    plotOptions: {
        radialBar: {
            startAngle: -90,
            endAngle: 90,
            track: {
                background: '#C7C8CC',
                startAngle: -90,
                endAngle: 90,
            },
            dataLabels: {
                name: {
                    show: false,
                },
                value: {
                    fontSize: "19px",
                    offsetY: -5,
                    show: true
                }
            }
        }
    },
    fill: {
        type: "gradient",
        gradient: {
            shade: "dark",
            type: "horizontal",
            gradientToColors: ["#AAD9BB"],
            stops: [0, 100]
        }
    },
    stroke: {
        lineCap: "butt"
    },
    labels: ["Progress"]
};
var angleChart_yu = new ApexCharts(document.querySelector("#angle-chart-yu"), angleChartOptions_yu);
angleChart_yu.render();

// bar-chart
var barChartOptions = {
    series: [{
        data: [...mcw_count]
    }],
    chart: {
        type: 'bar',
        height: 500,
        toolbar: {
            show: false
        }
    },
    colors: [
        "#0C134F",
        "#0E2954",
        "#1F6E8C",
        "#2E8A99",
        "#84A7A1",
    ],
    plotOptions: {
        bar: {
            distributed: true,
            borderRadius: 4,
            horizontal: false,
            columnWidth: '45%',
        }
    },
    dataLabels: {
        enabled: false
    },
    legend: {
        show: false
    },
    xaxis: {
        labels: {
            style: {
                fontSize: '16px',
            },
        },
        categories: [...mcw_label],
    },
    yaxis: {
        title: {
            text: "Count"
        }
    }
};

var barChart = new ApexCharts(document.querySelector("#bar-chart"), barChartOptions);
barChart.render();

// area chart
var areaChartOptions = {
    series: [{
        name: 'Purchars Orders',
        // type: 'area',
        data: [69, 50, 45, 44, 55, 77]
    }, {
        name: 'Sales Orders',
        // type: 'line',
        data: [1, 5, 2, 10, 6, 25]
    }],
    chart: {
        height: 350,
        type: 'area',
        toolbar: {
            show: false
        }
    },
    colors: ["#345252", "#456123"],
    stroke: {
        curve: 'smooth'
    },
    fill: {
        type: 'solid',
        opacity: [0.35, 1],
    },
    labels: ['A', 'B', 'C', 'D', 'E', 'F'],
    markers: {
        size: 0
    },
    yaxis: [{
            title: {
                text: 'Purchars Orders',
            },
        },
        {
            opposite: true,
            title: {
                text: 'Sales Orders',
            },
        },
    ],
    tooltip: {
        shared: true,
        intersect: false,
        y: {
            formatter: function(y) {
                if (typeof y !== "undefined") {
                    return y.toFixed(0) + " points";
                }
                return y;
            }
        }
    }
};

var areaChart = new ApexCharts(document.querySelector("#area-chart"), areaChartOptions);
// areaChart.render();

// pie chart
var pieChartOptions = {
series: [...mcw_count],
    chart: {
        height: '90%',
        width: '90%',
        type: 'pie',
    },
    labels: [...mcw_label],
    legend: {
        fontSize: '18px',
        // horizontalAlign: 'center'
        // position: 'bottom'
    },
    colors: ["#3B185F", "#711A75","#3F0071", "#5B4B8A","#7858A6",],
    dataLabels: {
        style: {
            fontSize: '15px',
        },
    },
    responsive: [{
        breakpoint: 480,
        options: {
            chart: {
                width: 200
            },
        }
    }]
};

var piechart = new ApexCharts(document.querySelector("#pie-chart"), pieChartOptions);
piechart.render();


// circle chart-1
var circleChartOptions_1 = {
    chart: {
        height: 300,
        type: 'radialBar',
    },
    colors: ["#abbe21"],
    series: [70],
    labels: ['Sales'],
}

var circleChart_1 = new ApexCharts(document.querySelector("#circle-chart-1"), circleChartOptions_1);
// circleChart_1.render();

// radar chart
var radarChartOptions = {
    series: [{
        name: 'Series 1',
        data: [0],
    }],
    fill: {
        opacity: 0.4,
        colors: ["#711A75"]
    },
    stroke: {
        show: true,
        width: 3,
        colors: ["#5B4B8A"],
    },
    markers: {
        size: 3,
        colors: ["#5B4B8A"],
        hover: {
            size: 7
        }
    },
    chart: {
        height: 490,
        type: 'radar',
    },
    title: {
        style: {
            fontSize: '20px',
        },
        text: 'Onion Domain Num : None'
    },
    yaxis: {
        stepSize: 5
    },
    xaxis: {
        categories: ['None']
    }
};

var radarchart = new ApexCharts(document.querySelector("#radar-chart"), radarChartOptions);
// radarchart.render();

// Treemap chart
var treemapChartOptions = {
    series: [{
        data: [{
                x: 'Keywords',
                y: 1
            },
        ],
    }],
    legend: {
        show: false
    },
    chart: {
        height: '100%',
        width: '100%',
        type: 'treemap'
    },
    title: {
        style: {
            fontSize: '20px',
        },
        text: 'Onion Domain Num : None'
    },
    dataLabels: {
        enabled: true,
        style: {
        fontSize: '20px',
        },
        formatter: function(text, op) {
        return [text, op.value]
        },
        offsetY: -4
    },
    plotOptions: {
        treemap: {
        enableShades: true,
        shadeIntensity: 0.3,
        reverseNegativeShade: true,
        colorScale: {
            ranges: [
            {
                from: 0,
                to: 20,
                color: '#000'
            },
            {
                from: 20.1,
                to: 100,
                color: '#000'
            }
            ]
        }
        }
    },
};

var treemapchart = new ApexCharts(document.querySelector("#treemap-chart"), treemapChartOptions);
treemapchart.render();