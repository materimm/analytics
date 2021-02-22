function get_rolling_epa_and_cpoe(qb_stats) {
  let d1 = [];
  let d2 = [];
  d1.push({
    label: 'EPA',
    fill: false,
    borderColor: qb_stats.colors[0],
    backgroundColor: qb_stats.colors[0],
    pointRadius: 3,
    data: qb_stats.epa
  });

  d2.push({
    label: 'CPOE',
    fill: false,
    borderColor: qb_stats.colors[0],
    backgroundColor: qb_stats.colors[0],
    pointRadius: 3,
    data: qb_stats.cpoe
  });


  var epa_threshold = Array(qb_stats.games.length).fill(qb_stats.league_avg_epa);
  epaT = {
    label: "League Average EPA per Game",
    fill: false,
    borderColor: "#ff0000",
    backgroundColor: "#ff0000",
    pointRadius: 0,
    data: epa_threshold
  };

  var cpoe_threshold = Array(qb_stats.games.length).fill(qb_stats.league_avg_cpoe);
  cpoeT = {
    label: "League Average CPOE per Game",
    fill: false,
    borderColor: "#ff0000",
    backgroundColor: "#ff0000",
    pointRadius: 0,
    data: cpoe_threshold
  };

  d1.push(epaT);
  d2.push(cpoeT);


  let rolling_epa_avg = line_chart('rolling_epa_avg',
                                qb_stats.games,
                                d1,
                                qb_stats.name + ' Rolling 5 game EPA Average',
                                'regular season only',
                                {}, {},
                                'NFLFastR')
  let rolling_cpoe_avg = line_chart('rolling_cpoe_avg',
                                qb_stats.games,
                                d2,
                                qb_stats.name + ' Rolling 5 game CPOE Average',
                                'regular season only',
                                {}, {},
                                'NFLFastR')
}
