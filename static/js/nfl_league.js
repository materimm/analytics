//draw charts on page load
$(function () {
  $("#drawLeagueChartsButton").click();
});

function drawCharts(league_stats) {
  let epa = league_stats.epa;
  let cpoe = league_stats.cpoe;
  let colors = league_stats.colors;
  bar_chart('epa_chart',
            'bar',
            epa.epa,
            'EPA',
            epa.teams,
            colors,
            'Expected Points Added',
            'Regular Season | Season: ' + league_stats.season,
            'NFLFastR');
  bar_chart('cpoe_chart',
            'bar',
            cpoe.cpoe,
            'CPOE',
            cpoe.teams,
            colors,
            'Completion Percentage Over Expected',
            'Regular Season | Season: ' + league_stats.season,
            'NFLFastR');
}
