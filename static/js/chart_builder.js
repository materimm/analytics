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
      }
    }
  });
}


function scatter_chart(id, data, title, situation, xLabel, yLabel) {
  let ctx = document.getElementById(id).getContext("2d");
  let scatter = new Chart(ctx, {
      type: 'scatter',
      data: data,
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
              var index = context.dataIndex;
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

function stacked_bar_chart(id, datasets, labels, title, situation, data_from) {
  let config = {
      type: 'bar',
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
