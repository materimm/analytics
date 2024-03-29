//draw charts on page load
$(function () {
  $("#drawLeagueChartsButton").click();
});

function drawCharts(league_stats) {
  let teams = league_stats.teams;
  let colors = league_stats.colors;
  let logos = league_stats.logos;
  drawRollingxGF(league_stats.rolling_xgf, teams, colors, logos);
  drawGoalShare(league_stats.goal_share, teams, colors, logos, false)
  drawGoalShare(league_stats.xgoal_share, teams, colors, logos, true);
}

function drawRollingxGF(rolling_xGF_objs, teams, colors, logos) {
  let all_dates = rolling_xGF_objs.all_dates;

  let new_dates = [];
  for(let i=0; i<all_dates.length; i++) {
    new_dates.push(new Date(all_dates[i]));
  }

  let datasets = [];
  for(let i=0; i<teams.length; i++) {
      let t = teams[i]
      let obj = rolling_xGF_objs[t]
      let data = [];
      for(let j=0; j<obj.dates.length; j++) {
          data.push({
            x: new Date(obj.dates[j]),
            y: obj.xgf[j]
          });
      }

      datasets.push({
        label: t,
        fill: false,
        borderColor: colors[t][0],
        backgroundColor: colors[t][0],
        pointBackgroundColor: colors[t][0],
        pointBorderColor: colors[t][0],
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
    borderDash: [10,5],
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
  line_chart('rolling_xGF_chart',
            new_dates,
            datasets,
            'Rolling 5 game xGF% Average',
            '5v5', x, y,
            'moneypuck.com',
            logos);

}

function drawGoalShare(goal_share, teams, colors, logos, isExpected) {
  let datasets = [];
  for(let i=0; i<teams.length; i++) {
      let t = teams[i];
      let goal_share_obj = goal_share[t];
      let data = {
        x: goal_share_obj.gf60,
        y: goal_share_obj.ga60,
      };
      datasets.push({
        label: t,
        pointRadius: 5,
        borderColor: colors[t][0],
        backgroundColor: colors[t][0],
        data: [data]
      });
  }

  let scatterData = {datasets};
  let avg_x = goal_share["avg"]["gf60"];
  let avg_y = goal_share["avg"]["ga60"];
  if(isExpected) {
    scatter_chart('xgoal_share_chart', scatterData, 'Expected Goal Share', '5v5', 'xGF/60', 'xGA/60', logos, avg_x, avg_y, 'moneypuck.com');
  }
  else {
    scatter_chart('goal_share_chart', scatterData, 'Goal Share', '5v5', 'GF/60', 'GA/60', logos, avg_x, avg_y, 'moneypuck.com');
  }

}
