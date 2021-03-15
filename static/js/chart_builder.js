function radar_chart(id, labels, datasets, title, situation) {
  let ctx = document.getElementById(id).getContext("2d");
  let radarChart = new Chart(ctx,  {
    type: "radar",
    data:{
      labels: labels,
      datasets: datasets,
    },
    options: {
      element: {
        line: {
          tension:0,
          borderWidth:3
        }
      },
      title: {
        display: true,
        text: [title,
              'situations: ' + situation,
              'data: Natural Stat Trick (@natstattrick) | chart: @moman939'],
      },
    }
  });
}


function line_chart(id, labels, datasets, title, situation ,xAxis, yAxis, data_from, imgs) {
  let ctx = document.getElementById(id).getContext("2d");
  let lineChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: datasets,
    },
    plugins: {
      afterUpdate: chart => {
        if(imgs != null) {
          for(let i=0; i<datasets.length; i++) {
            const img = new Image();
            let l = datasets[i].label;
            if(l ==  "Threshold Line") {
              continue;
            }
            img.src = imgs[l];
            img.width = 35;
            img.height = (35/3) * 2;
            chart.getDatasetMeta(i).data.forEach((d, j) => d._model.pointStyle = img);
          }
        }
      }
    },
    options: {
      title: {
        display: true,
        text: [title,
              'situations: ' + situation,
              'data: ' + data_from + ' | chart: @moman939'],
      },
      scales: {
        xAxes: [xAxis],
        yAxes: [yAxis]
      },
    }
  });
}

function line_chart_with_point_labels(id, labels, datasets, title, situation ,xAxis, yAxis, data_from) {
  //show all tooltips for single game xGF% charts
  Chart.plugins.register({
    beforeRender: function(chart) {
      if (chart.config.options.showAllTooltips) {
        // create an array of tooltips,
        // we can't use the chart tooltip because there is only one tooltip per chart
        chart.pluginTooltips = [];
        chart.config.data.datasets.forEach(function(dataset, i) {
          chart.getDatasetMeta(i).data.forEach(function(sector, j) {
            chart.pluginTooltips.push(new Chart.Tooltip({
              _chart: chart.chart,
              _chartInstance: chart,
              _data: chart.data,
              _options: chart.options.tooltips,
              _active: [sector]
            }, chart));
          });
        });
        chart.options.tooltips.enabled = false; // turn off normal tooltips
      }
    },
    afterDraw: function(chart, easing) {
      if (chart.config.options.showAllTooltips) {
        if (!chart.allTooltipsOnce) {
          if (easing !== 1) {
            return;
          }
          chart.allTooltipsOnce = true;
        }
        chart.options.tooltips.enabled = true;
        Chart.helpers.each(chart.pluginTooltips, function(tooltip) {
          tooltip.initialize();
          tooltip.update();
          tooltip.pivot();
          tooltip.transition(easing).draw();
        });
        chart.options.tooltips.enabled = false;
      }
    }
  });

  let ctx = document.getElementById(id).getContext("2d");
  let lineChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: datasets,
    },
    options: {
      title: {
        display: true,
        text: [title,
              'situations: ' + situation,
              'data: ' + data_from + ' | chart: @moman939'],
      },
      scales: {
        xAxes: [xAxis],
        yAxes: [yAxis]
      },
      showAllTooltips: true,
      legend: {
        display: false
      }
    }
  });
}


function scatter_chart(id, data, title, situation, xLabel, yLabel, imgs, avg_x, avg_y) {
  let ctx = document.getElementById(id).getContext("2d");
  let scatter = new Chart(ctx, {
      type: 'scatter',
      data: data,
      plugins: {
        beforeDraw: chart => {
          var chartArea = chart.chartArea;
          var ctx = chart.chart.ctx;

          // Replace these IDs if you have given your axes IDs in the config
          var xScale = chart.scales['x-axis-1'];
          var yScale = chart.scales['y-axis-1'];

          var midX = xScale.getPixelForValue(avg_x);
          var midY = yScale.getPixelForValue(avg_y);

          // Top left quadrant
          ctx.fillStyle = "rgba(184, 203, 233, 1)";
          ctx.fillRect(chartArea.left, chartArea.top, midX - chartArea.left, midY - chartArea.top);

          // Top right quadrant
          ctx.fillStyle = "rgba(89, 138, 197, 1)";
          ctx.fillRect(midX, chartArea.top, chartArea.right - midX, midY - chartArea.top);

          // Bottom right quadrant
          ctx.fillStyle = "rgba(250, 220, 222, 1)";
          ctx.fillRect(midX, midY, chartArea.right - midX, chartArea.bottom - midY);

          // Bottom left quadrant
          ctx.fillStyle = "rgba(248, 105, 111, 1)";
          ctx.fillRect(chartArea.left, midY, midX - chartArea.left, chartArea.bottom - midY);
        },
        afterUpdate: chart => {
          for(let i=0; i<data.datasets.length; i++) {
            const img = new Image();
            let l = data.datasets[i].label;
            img.src = imgs[l];
            img.width = 50;
            img.height = 100/3;
            chart.getDatasetMeta(i).data.forEach((d, j) => d._model.pointStyle = img);
          }
        }
      },
      options: {
        legend: {
          display: false
        },
        title: {
          display: true,
          text: [title,
                'situations: ' + situation,
                'data: Natural Stat Trick (@natstattrick) | chart: @moman939'],
        },
        scales: {
          xAxes: [{
            scaleLabel: {
              display: true,
              labelString: xLabel,
            }
          }],
          yAxes: [{
            scaleLabel: {
              display: true,
              labelString: yLabel,
            },
            ticks: {
              reverse: true
            }
          }],
        }
      }
  });
}

function doughnut(id, data, data_label, labels, colors, title, situation) {
  let config = {
      type: 'doughnut',
      data: {
        datasets: [{
          data: data,
          backgroundColor: colors,
          label: data_label
        }],
        labels: labels,
      },
      options: {
        responsive: true,
        legend: {
          position: 'top',
        },
        title: {
          display: true,
          text: [title,
                'situation: ' + situation,
                'data: Natural Stat Trick (@natstattrick) | chart: @moman939'],
        },
        animation: {
          animateScale: true,
          animateRotate: true
        }
      }
    };

    let ctx = document.getElementById(id).getContext('2d');
    let doughnut = new Chart(ctx, config);
}

function bar_chart(id, type, data, data_label, labels, colors, title, situation, data_from) {
  let config = {
      type: type,
      data: {
        datasets: [{
          data: data,
          backgroundColor: function(context) {
            let index = context.dataIndex;
            let team = context.chart.config.data.labels[index];
            return hexToRgbA(colors[team][0], 0.7);
          },
          // backgroundColor: function(context) {
          //     let index = context.dataIndex;
          //     let len = colors.length - 1;
          //     if(index > len) {
          //       console.log(hexToRgbA(colors[len], 0.6));
          //       return hexToRgbA(colors[len], 0.6);
          //     }
          //     return hexToRgbA(colors[index], 0.6);
          // },
          borderColor: function(context) {
            let index = context.dataIndex;
            let team = context.chart.config.data.labels[index];
            return hexToRgbA(colors[team][0], 1);
          },
          borderWidth: 2,
          label: data_label
        }],
        labels: labels,
      },
      options: {
        responsive: true,
        legend: {
          position: 'top',
        },
        title: {
          display: true,
          text: [title,
                'Situation: ' + situation,
                'data: ' + data_from + ' | chart: @moman939'],
        },
        scales: {
          xAxes: [{
            ticks: {
                beginAtZero: true
            }
          }],
          yAxes: [{
            ticks: {
                beginAtZero: true
            }
          }]
        }
      }
    };

    let ctx = document.getElementById(id).getContext('2d');
    let bar = new Chart(ctx, config);
}

function stacked_bar_chart(id, type, datasets, labels, title, situation, data_from) {
  let config = {
      type: type,
      data: {
        labels: labels,
        datasets: datasets,
      },
      options: {
        responsive: true,
        legend: {
          position: 'top',
        },
        title: {
          display: true,
          text: [title,
                'Situation: ' + situation,
                'data: ' + data_from + ' | chart: @moman939'],
        },
        scales: {
          xAxes: [{
							stacked: true,
						}],
						yAxes: [{
							stacked: true
						}]
        }
      }
    };

    let ctx = document.getElementById(id).getContext('2d');
    let bar = new Chart(ctx, config);
}

function resizeImg() {
    let maxWidth = 35; // Max width for the image
    let maxHeight = 35;    // Max height for the image
    let ratio = 0;  // Used for aspect ratio
    let width = 150;    // Current image width
    let height = 100;  // Current image height

    // Check if the current width is larger than the max
    if(width > maxWidth){
        ratio = maxWidth / width;   // get ratio for scaling image
        //$(this).css("width", maxWidth); // Set new width
        //$(this).css("height", height * ratio);  // Scale height based on ratio
        height = height * ratio;    // Reset height to match scaled image
        width = width * ratio;    // Reset width to match scaled image
    }

    // Check if current height is larger than max
    if(height > maxHeight){
        ratio = maxHeight / height; // get ratio for scaling image
        //$(this).css("height", maxHeight);   // Set new height
        //$(this).css("width", width * ratio);    // Scale width based on ratio
        width = width * ratio;    // Reset width to match scaled image
        height = height * ratio;    // Reset height to match scaled image
    }

    return [width, height];
}
