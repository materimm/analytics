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


function line_chart(id, labels, datasets, title, situation ,xAxis, yAxis, data_from) {
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


function scatter_chart(id, data, title, situation, xLabel, yLabel, imgs) {
  let ctx = document.getElementById(id).getContext("2d");
  let scatter = new Chart(ctx, {
      type: 'scatter',
      data: data,
      plugins: {
        afterUpdate: chart => {
          for(let i=0; i<data.datasets.length; i++) {
            const img = new Image();
            let l = data.datasets[i].label;
            img.src = imgs[l];
            img.width=50;
            img.height=50;
            chart.getDatasetMeta(i).data.forEach((d, j) => d._model.pointStyle = img);
          }
        }
      },
      options: {
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
              let len = colors.length - 1;
              if(index > len) {
                console.log(hexToRgbA(colors[len], 0.6));
                return hexToRgbA(colors[len], 0.6);
              }
              return hexToRgbA(colors[index], 0.6);
          },
          borderColor: colors,
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
