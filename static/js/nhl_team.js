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
  radar_chart('radar_chart', team_obj.stats, datasets, 'Team Play', '5v5');
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

  x = {
    type: 'time',
    time: {
      parser: 'MM/DD/YYYY',
      round: 'day',
    },
    scaleLabel: {
      display: true,
      labelString: 'Date',
    }
  };

  y = {
    scaleLabel: {
      display: true,
      labelString: 'xGF%',
    }
  };
  line_chart('rolling_xGF_chart', new_dates, datasets, 'Rolling 5 game xGF% Average', '5v5', x, y)
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
    scatter_chart('goal_share_chart', scatterData, 'Goal Share', '5v5', 'GF/60', 'GA/60');
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
    scatter_chart('xgoal_share_chart', scatterData, 'Expected Goal Share', '5v5', 'GF/60', 'GA/60');
}
