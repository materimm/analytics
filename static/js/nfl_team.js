//draw charts on page load
$(function () {
  $("#drawTeamChartsButton").click();
});

function flipCards(team_stats) {
  let button = document.getElementById("flipCardsButton");
  if(button.innerHTML == "Show Ranks") {
    button.innerHTML = "Show Stats";
    document.getElementById("epa").innerHTML = team_stats["epa_rank"];
    document.getElementById("cpoe").innerHTML = team_stats["cpoe_rank"];
    document.getElementById("pepa").innerHTML = team_stats["pass_epa_rank"];
    document.getElementById("repa").innerHTML = team_stats["rush_epa_rank"];
  }
  else if(button.innerHTML == "Show Stats") {
    button.innerHTML = "Show Ranks";
    document.getElementById("epa").innerHTML = team_stats["epa"];
    document.getElementById("cpoe").innerHTML = team_stats["cpoe"] + "%";
    document.getElementById("pepa").innerHTML = team_stats["pass_epa"];
    document.getElementById("repa").innerHTML = team_stats["rush_epa"];
  }
}

function drawTeamCharts(team_stats) {
  console.log(team_stats);
  let gs = team_stats.game_data;
  let colors = team_stats.colors;
  drawEPACharts(gs, colors);
}

function drawEPACharts(game_data, colors) {
  console.log(game_data);
  let dates = game_data.dates;
  let epa = game_data.epa;
  let pass_epa = game_data.pass_epa;
  let rush_epa = game_data.rush_epa;

  let new_dates = [];
  let epa_data = [];
  let pass_epa_data = [];
  let rush_epa_data = [];

  for(let i=0; i<dates.length; i++) {
    let d = new Date(dates[i]);
    new_dates.push(d);
    epa_data.push({
      x: d,
      y: epa[i]
    });
    pass_epa_data.push({
      x: d,
      y: pass_epa[i]
    });
    rush_epa_data.push({
      x: d,
      y: rush_epa[i]
    });
  }

  let datasets = [];
  datasets.push({
    label: 'EPA',
    fill: false,
    borderColor: colors[0],
    backgroundColor: colors[0],
    pointBackgroundColor: colors[0],
    pointBorderColor: colors[0],
    pointRadius: 3,
    data: epa_data
  });
  datasets.push({
    label: 'Passing EPA',
    fill: false,
    borderColor: colors[1],
    backgroundColor: colors[1],
    pointBackgroundColor: colors[1],
    pointBorderColor: colors[1],
    pointRadius: 3,
    data: pass_epa_data
  });
  datasets.push({
    label: 'Rushing EPA',
    fill: false,
    borderColor: colors[2],
    backgroundColor: colors[2],
    pointBackgroundColor: colors[2],
    pointBorderColor: colors[2],
    pointRadius: 3,
    data: rush_epa_data
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
      labelString: 'EPA',
    }
  };

  line_chart('epa_per_game_chart',
            new_dates,
            datasets,
            'EPA per game',
            'Regular Season', x, y,
            'NFLFastR',
            null);

}
