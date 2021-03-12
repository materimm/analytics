//draw charts on page load
$(function () {
  $("#drawTeamChartsButton").click();
});

function flipCards(team_stats) {
  let button = document.getElementById("flipCardsButton");
  if(button.innerHTML == "Show Ranks") {
    button.innerHTML = "Show Stats";
    document.getElementById("gf").innerHTML = team_stats["gf_rank"];
    document.getElementById("ga").innerHTML = team_stats["ga_rank"];
    document.getElementById("gfp").innerHTML = team_stats["gf_percent_rank"];
    document.getElementById("ppp").innerHTML = team_stats["pp_percent_rank"];
    document.getElementById("pkp").innerHTML = team_stats["pk_percent_rank"];
    document.getElementById("xgf").innerHTML = team_stats["xgf_rank"];
    document.getElementById("xga").innerHTML = team_stats["xga_rank"];
    document.getElementById("xgfp").innerHTML = team_stats["xgf_percent_rank"];
    document.getElementById("gax").innerHTML = team_stats["gax_rank"];
    document.getElementById("gsax").innerHTML = team_stats["gsax_rank"];
    document.getElementById("cfp").innerHTML = team_stats["corsi_rank"];
    document.getElementById("sf").innerHTML = team_stats["sf_rank"];
    document.getElementById("sa").innerHTML = team_stats["sa_rank"];
    document.getElementById("sh_percent").innerHTML = team_stats["shooting_percent_rank"];
    document.getElementById("save_percent").innerHTML = team_stats["save_percent_rank"];
  }
  else if(button.innerHTML == "Show Stats") {
    button.innerHTML = "Show Ranks";
    document.getElementById("gf").innerHTML = team_stats["gf"];
    document.getElementById("ga").innerHTML = team_stats["ga"];
    document.getElementById("gfp").innerHTML = team_stats["gf_percent"] + "%";
    document.getElementById("ppp").innerHTML = team_stats["pp_percent"] + "%";
    document.getElementById("pkp").innerHTML = team_stats["pk_percent"] + "%";
    document.getElementById("xgf").innerHTML = team_stats["xgf"];
    document.getElementById("xga").innerHTML = team_stats["xga"];
    document.getElementById("xgfp").innerHTML = team_stats["xgf_percent"] + "%";
    document.getElementById("gax").innerHTML = team_stats["gax"];
    document.getElementById("gsax").innerHTML = team_stats["gsax"];
    document.getElementById("cfp").innerHTML = team_stats["corsi_percent"] + "%";
    document.getElementById("sf").innerHTML = team_stats["sf"];
    document.getElementById("sa").innerHTML = team_stats["sa"];
    document.getElementById("sh_percent").innerHTML = team_stats["shooting_percent"] + "%";
    document.getElementById("save_percent").innerHTML = team_stats["save_percent"] + "%";
  }
}

function drawTeamCharts(team_stats) {
  let rolling_xgf = team_stats.rolling_xgf;
  let name = team_stats.name;
  let colors = team_stats.colors;
  let logo = team_stats.logo;
  drawRollingxGF(rolling_xgf.dates, rolling_xgf.xgf, name, colors, logo)
}

function drawRollingxGF(dates, xgf, name, colors, logo) {
  let new_dates = [];
  let data = [];
  for(let i=0; i<dates.length; i++) {
    let d = new Date(dates[i])
    new_dates.push(d);
    data.push({
      x: d,
      y: xgf[i]
    });
  }

  let datasets = [];
  datasets.push({
    label: name,
    fill: false,
    borderColor: colors[0],
    backgroundColor: colors[0],
    pointBackgroundColor: colors[0],
    pointBorderColor: colors[0],
    pointRadius: 3,
    data: data
  });

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
            null);

}
