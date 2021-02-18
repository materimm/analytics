function team_radar(team_obj) {
  var datasets = [];
  var teams = team_obj.teams;
  for(var i=0; i<teams.length; i++) {
    var team = teams[i];
    datasets.push({
      label: team.name,
      data: team.data,
      fill: true,
      backgroundColor: hexToRgbA(team.colors[0], 0.2),
      borderColor: team.colors[0],
      pointBackgroundColor: team.colors[0],
      pointBorderColor: "#fff",
      pointHoverBackgroundColor: team.colors[0],
      pointHoverBorderColor: team.colors[0]
    });
  }
  var ctx = document.getElementById("radar_chart").getContext("2d");
  var radarChart = new Chart(ctx,  {
    "type": "radar",
    "data":{
      "labels": team_obj.stats,
      "datasets": datasets,
    },
    "options": {
      "elements": {
        "line": {
          "tension":0,
          "borderWidth":3
        }
      },
      title: {
        display: true,
        text: ['Team Play Percentages', 'data: Natural Stat Trick (@natstattrick) | chart: @moman939'],
      },
      // scale: {
      //   ticks: {
      //     beginAtZero: true,
      //     max: 60
      //   }
      // }
    }
  });
}


function rolling_xGF(rolling_xGF_obj) {
  let team_objs = rolling_xGF_obj.teams;
  let all_dates = rolling_xGF_obj.all_dates;

  let new_dates = [];
  for(let i=0; i<all_dates.length; i++) {
    new_dates.push(new Date(all_dates[i]));
  }

  let datasets = [];
  for(let i=0; i<team_objs.length; i++) {
      let t = team_objs[i];
      let data = [];
      for(let j=0; j<t.dates.length; j++) {
          data.push({
            x: new Date(t.dates[j]),
            y: t.xGFs[j]
          });
      }

      datasets.push({
        label: t.name,
        fill: false,
        borderColor: t.colors[0],
        backgroundColor: t.colors[0],
        pointBackgroundColor: t.colors[0],
        pointBorderColor: t.colors[0],
        pointRadius: 3,
        data: data
      });

  }

  var threshold = Array(new_dates.length).fill(50);
  datasets.push({
    label: "Threshold Line",
    fill: false,
    borderColor: "#000",
    backgroundColor: "#000",
    pointRadius: 0,
    data: threshold
  });

  var ctx = document.getElementById("rolling_xGF_chart").getContext("2d");
  var timeformat = 'MM/DD/YYYY';
  var myLineChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: new_dates,
      datasets: datasets,
    },
    options: {
      title: {
        display: true,
        text: ['Rolling 5 game xGF% Average', 'situations: 5v5', 'data: Natural Stat Trick (@natstattrick) | chart: @moman939'],
      },
      scales: {
        yAxes: [{
          scaleLabel: {
            display: true,
            labelString: 'xGF%',
          }
        }],
        xAxes: [{
          type: 'time',
          time: {
            parser: timeformat,
            round: 'day',
          },
          scaleLabel: {
            display: true,
            labelString: 'Date',
          }
        }],
      }
    }
  });
}

function goal_share(goal_share_obj) {
    let datasets = []
    for(let i=0; i<goal_share_obj.length; i++) {
        let team = goal_share_obj[i];
        let data = {
          x: team.gf60,
          y: team.ga60,
        };
        datasets.push({
          label: team.name,
          pointRadius: 5,
          borderColor: team.colors[0],
          backgroundColor: team.colors[0],
          data: [data]
        });
    }

    let scatterData = {datasets};
    let ctx = document.getElementById("goal_share_chart").getContext("2d");
    let scatter = new Chart(ctx, {
        type: 'scatter',
				data: scatterData,
				options: {
          title: {
            display: true,
            text: ['Goal Share', 'situations: 5v5', 'data: Natural Stat Trick (@natstattrick) | chart: @moman939'],
          },
          scales: {
            xAxes: [{
              scaleLabel: {
                display: true,
                labelString: 'GF/60',
              }
            }],
            yAxes: [{
              scaleLabel: {
                display: true,
                labelString: 'GA/60',
              }
            }],
          }
				}
		});
}

function expected_goal_share(xgoal_share_obj) {
    let datasets = []
    for(let i=0; i<xgoal_share_obj.length; i++) {
        let team = xgoal_share_obj[i];
        let data = {
          x: team.xgf60,
          y: team.xga60,
        };
        datasets.push({
          label: team.name,
          pointRadius: 5,
          borderColor: team.colors[0],
          backgroundColor: team.colors[0],
          data: [data]
        });
    }

    let scatterData = {datasets};
    let ctx = document.getElementById("xgoal_share_chart").getContext("2d");
    let scatter = new Chart(ctx, {
        type: 'scatter',
				data: scatterData,
				options: {
          title: {
            display: true,
            text: ['Expected Goal Share', 'situations: 5v5', 'data: Natural Stat Trick (@natstattrick) | chart: @moman939'],
          },
          scales: {
            xAxes: [{
              scaleLabel: {
                display: true,
                labelString: 'xGF/60',
              }
            }],
            yAxes: [{
              scaleLabel: {
                display: true,
                labelString: 'xGA/60',
              }
            }],
          }
				}
		});
}


function hexToRgbA(hex, a){
    var c;
    if(/^#([A-Fa-f0-9]{3}){1,2}$/.test(hex)){
        c= hex.substring(1).split('');
        if(c.length== 3){
            c= [c[0], c[0], c[1], c[1], c[2], c[2]];
        }
        c= '0x'+c.join('');
        return 'rgba('+[(c>>16)&255, (c>>8)&255, c&255].join(',')+',' + a + ')';
    }
    throw new Error('Bad Hex');
}
