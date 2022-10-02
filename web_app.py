import justpy as jp
import pandas
import matplotlib.pyplot as plt
from datetime import datetime
from pytz import utc


data = pandas.read_csv("reviews.csv", parse_dates=["Timestamp"])

data["Day"] = data["Timestamp"].dt.date

day_count = data.groupby(["Day"]).count()

day_average = data.groupby(["Day"]).mean()

# Downsampling by week
data["Week"] = data["Timestamp"].dt.strftime("%Y-%U")
week_average = data.groupby(["Week"]).mean()

# Downsampling by month
data["Month"] = data["Timestamp"].dt.strftime("%Y-%m")
month_average = data.groupby(["Month"]).mean()

# Average by month and course
month_course_average = data.groupby(["Month", "Course Name"]).mean().unstack()
month_course_comment = data.groupby(["Month", "Course Name"])["Comment"].count().unstack()
print(month_course_average)

# The happiest day
data["Weekday"] = data["Timestamp"].dt.strftime("%A")
data["Day Number"] = data["Timestamp"].dt.strftime("%w")
weekday_average = data.groupby(["Weekday", "Day Number"]).mean()
weekday_average = weekday_average.sort_values("Day Number")

# Rating and comments for different courses
course_comment = data.groupby(["Course Name"])["Comment"].count()
course_rating = data.groupby(["Course Name"])["Rating"].count()

# The comment-to-rating ratio for different courses
course_ratio = pandas.merge(course_comment, course_rating, on="Course Name")
course_ratio["Ratio"] = (course_ratio["Comment"] / course_ratio["Rating"])

chart_def = """
{
    chart: {
        type: 'spline',
        inverted: true
    },
    title: {
        text: 'Atmosphere Temperature by Altitude'
    },
    subtitle: {
        text: 'According to the data in reviews.csv'
    },
    xAxis: {
        reversed: false,
        title: {
            enabled: true,
            text: 'Date'
        },
        labels: {
            format: '{value}'
        },
        accessibility: {
            rangeDescription: 'Range: 0 to 80 km.'
        },
        maxPadding: 0.05,
        showLastLabel: true
    },
    yAxis: {
        title: {
            text: 'Average Rating'
        },
        labels: {
            format: '{value}'
        },
        accessibility: {
            rangeDescription: 'Range: -90°C to 20°C.'
        },
        lineWidth: 2
    },
    legend: {
        enabled: false
    },
    tooltip: {
        headerFormat: '<b>{series.name}</b><br/>',
        pointFormat: '{point.x}: {point.y}'
    },
    plotOptions: {
        spline: {
            marker: {
                enable: false
            }
        }
    },
    series: [{}]
}
"""

multi_chart_def = """
 {
    chart: {
        type: 'spline',
    },
    title: {
        text: 'Moose and deer hunting in Norway, 2000 - 2021'
    },
    subtitle: {
        align: 'center',
        text: 'Source: reviews.csv'
    },
    legend: {
        layout: 'vertical',
        align: 'left',
        verticalAlign: 'top',
        x: 120,
        y: 70,
        floating: false,
        borderWidth: 1,
        backgroundColor: '#FFFFFF'
    },
    xAxis: {
        title: {
            enabled: true,
            text: 'Date'
        },
        labels: {
            format: '{value}'
        },
        plotBands: [{ // Highlight the two last years
            from: 2019,
            to: 2020,
            color: 'rgba(68, 170, 213, .2)'
        }]
    },
    yAxis: {
        title: {
            text: 'Quantity'
        }
    },
    tooltip: {
        shared: true,
        headerFormat: '<b>Hunting season starting autumn {point.x}</b><br>'
    },
    credits: {
        enabled: false
    },
    plotOptions: {
        //series: {pointStart: 2000},
        areaspline: {
            fillOpacity: 0.5
        }
    },
    series: [{}]
}
"""

stream_chart_def = """
{

    chart: {
        type: 'streamgraph',
        marginBottom: 30,
        zoomType: 'x'
    },

    title: {
        floating: true,
        align: 'left',
        text: 'Winter Olympic Medal Wins'
    },
    
    subtitle: {
        floating: true,
        align: 'left',
        y: 30,
        text: 'Source: <a href="https://www.sports-reference.com/olympics/winter/1924/">sports-reference.com</a>'
    },

    xAxis: {
        maxPadding: 0,
        type: 'category',
        crosshair: true,
        categories: [],
        labels: {
            align: 'left',
            reserveSpace: false,
            rotation: 270
        },
        lineWidth: 0,
        margin: 20,
        tickWidth: 0
    },

    yAxis: {
        visible: false,
        startOnTick: false,
        endOnTick: false
    },

    legend: {
        enabled: false
    },

    annotations: [{
        labels: [{
            point: {
                x: 5.5,
                xAxis: 0,
                y: 30,
                yAxis: 0
            },
            text: 'Cancelled<br>during<br>World War II'
        }, {
            point: {
                x: 18,
                xAxis: 0,
                y: 90,
                yAxis: 0
            },
            text: 'Soviet Union fell,<br>Germany united'
        }],
        labelOptions: {
            backgroundColor: 'rgba(255,255,255,0.5)',
            borderColor: 'silver'
        }
    }],

    plotOptions: {
        series: {
            label: {
                minFontSize: 5,
                maxFontSize: 15,
                style: {
                    color: 'rgba(255,255,255,0.75)'
                }
            },
            accessibility: {
                exposeAsGroupOnly: true
            }
        }
    },

    // Data parsed with olympic-medals.node.js
    series: [{}],

    exporting: {
        sourceWidth: 800,
        sourceHeight: 600
    }

}
"""

pie_chart_def = """
{
    chart: {
        type: 'pie'
    },
    title: {
        text: 'Browser market shares in May, 2020'
    },
    tooltip: {
        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
    },
    accessibility: {
        point: {
            valueSuffix: '%'
        }
    },
    plotOptions: {
        pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
                enabled: true,
                format: '<b>{point.name}</b>: {point.percentage:.1f} %'
            }
        }
    },
    series: [{
        name: 'Brands',
        colorByPoint: true,
        data: [{
            name: 'Chrome',
            y: 70.67,
            sliced: true,
            selected: true
        }, {
            name: 'Edge',
            y: 14.77
        },  {
            name: 'Firefox',
            y: 4.86
        }, {
            name: 'Safari',
            y: 2.63
        }, {
            name: 'Internet Explorer',
            y: 1.53
        },  {
            name: 'Opera',
            y: 1.40
        }, {
            name: 'Sogou Explorer',
            y: 0.84
        }, {
            name: 'QQ',
            y: 0.51
        }, {
            name: 'Other',
            y: 2.6
        }]
    }]
}
"""

def app():
    wp = jp.QuasarPage()
    h1 = jp.Div(a=wp, text="Analysis of Course Reviews", classes="text-h1 text-center q-pa-md")
    h1 = jp.Div(a=wp, text="Course Review Analysis")

    hc_0 = jp.HighCharts(a=wp, options=chart_def)
    hc_0.options.chart.inverted = False
    hc_0.options.title.text = "Average Rating by Day"
    hc_0.options.xAxis.categories = list(day_average.index)
    hc_0.options.series[0].data = list(day_average['Rating'])

    hc_1 = jp.HighCharts(a=wp, options=chart_def)
    hc_1.options.chart.inverted = False
    hc_1.options.title.text = "Average Rating by Week"
    hc_1.options.xAxis.categories = list(week_average.index)
    hc_1.options.series[0].data = list(week_average['Rating'])

    hc_2 = jp.HighCharts(a=wp, options=chart_def)
    hc_2.options.chart.inverted = False
    hc_2.options.title.text = "Average Rating by Month"
    hc_2.options.xAxis.categories = list(month_average.index)
    hc_2.options.series[0].data = list(month_average['Rating'])

    hc_data = [{"name": v1, "data": [v2 for v2 in month_course_average[v1]]} for v1 in month_course_average.columns]
    hc_3 = jp.HighCharts(a=wp, options=multi_chart_def)
    hc_3.options.title.text = "Rating for different courses by month"
    hc_3.options.xAxis.categories = list(month_course_average.index)
    hc_3.options.yAxis.title.text = "Average Rating"
    hc_3.options.series = hc_data
    hc_3.options.tooltip.headerFormat = '<b>Rating for different courses by month {point.x}</b><br>'

    hc_data = [{"name": v1, "data": [v2 for v2 in course_ratio[v1]]} for v1 in course_ratio.columns]
    hc_4 = jp.HighCharts(a=wp, options=multi_chart_def)
    hc_4.options.title.text = "The comment-to-rating ratio for different courses"
    hc_4.options.xAxis.categories = list(course_ratio.index)
    hc_4.options.yAxis.title.text = ""
    hc_4.options.series = hc_data
    hc_4.options.tooltip.headerFormat = '<b>The comment-to-rating ratio for different courses {point.x}</b><br>'

    hc_data = [{"name": v1, "data": [v2 for v2 in month_course_comment[v1]]} for v1 in month_course_comment.columns]
    hc_5 = jp.HighCharts(a=wp, options=stream_chart_def)
    hc_5.options.title.text = "Rating for different courses by month"
    hc_5.options.xAxis.categories = list(month_course_comment.index)
    hc_5.options.yAxis.title.text = "Average Rating"
    hc_5.options.series = hc_data
    hc_5.options.tooltip.headerFormat = '<b>Rating for different courses by month {point.x}</b><br>'

    hc_6 = jp.HighCharts(a=wp, options=chart_def)
    hc_6.options.chart.inverted = False
    hc_6.options.title.text = "The happiest day"
    hc_6.options.xAxis.categories = list(weekday_average.index)
    hc_6.options.series[0].data = list(weekday_average['Rating'])

    hc_data = [{"name": v1, "y": v2} for v1, v2 in zip(course_comment.index, course_comment)]
    hc_7 = jp.HighCharts(a=wp, options=pie_chart_def)
    hc_7.options.title.text = "Comments for different courses"
    hc_7.options.xAxis.categories = list(course_comment.index)
    hc_7.options.series[0].data = hc_data

    return wp


jp.justpy(app)
