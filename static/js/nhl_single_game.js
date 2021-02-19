function get_game_stats(game_stats) {
      team1 = game_stats[0];
      team2 = game_stats[1];

      //team stats
      let cf_chart = doughnut('corsi',
                              [team1.cf, team2.cf],
                              'Shot Share',
                              [team1.name, team2.name],
                              [hexToRgbA(team1.colors[0], 1),hexToRgbA(team2.colors[0], 1)],
                              'Shot Share',
                              '5v5');

      let xgf_chart = doughnut('xgf',
                              [team1.xgf, team2.xgf],
                              'Expected Goal Differential',
                              [team1.name, team2.name],
                              [hexToRgbA(team1.colors[0], 1),hexToRgbA(team2.colors[0], 1)],
                              'Expected Goal Differential',
                              '5v5');

      let hdcf_chart = doughnut('hdcf',
                              [team1.hdcf, team2.hdcf],
                              'High Danger Shot Share',
                              [team1.name, team2.name],
                              [hexToRgbA(team1.colors[0], 1),hexToRgbA(team2.colors[0], 1)],
                              'High Danger Shot Share',
                              '5v5');

      //skater stats
      let t1_toi = bar_chart('t1_skaters_toi',
                              'bar',
                              team1.skaters.toi,
                              "Time on Ice",
                              team1.skaters.names,
                              team1.colors[0],
                              team1.name + " Time on Ice",
                              '5v5');
      let t2_toi = bar_chart('t2_skaters_toi',
                              'bar',
                              team2.skaters.toi,
                              "Time on Ice",
                              team2.skaters.names,
                              team2.colors[0],
                              team2.name + " Time on Ice",
                              '5v5');

      let t1_cf = bar_chart('t1_skaters_cf',
                              'bar',
                              team1.skaters.cf,
                              "Shot Share",
                              team1.skaters.names,
                              team1.colors[0],
                              team1.name + " Shot Share",
                              '5v5');
      let t2_cf = bar_chart('t2_skaters_cf',
                              'bar',
                              team2.skaters.cf,
                              "Shot Share",
                              team2.skaters.names,
                              team2.colors[0],
                              team2.name + " Shot Share",
                              '5v5');

      let t1_xgf = bar_chart('t1_skaters_xgf',
                              'bar',
                              team1.skaters.xgf,
                              "Expected Goal Differential",
                              team1.skaters.names,
                              team1.colors[0],
                              team1.name + " Expected Goal Differential",
                              '5v5');
      let t2_xgf = bar_chart('t2_skaters_xgf',
                              'bar',
                              team2.skaters.xgf,
                              "Expected Goal Differential",
                              team2.skaters.names,
                              team2.colors[0],
                              team2.name + " Expected Goal Differential",
                              '5v5');

      //Line stats
      let t1_lines_toi = bar_chart('t1_lines_toi',
                              'horizontalBar',
                              team1.lines.toi,
                              "Time on Ice",
                              team1.lines.names,
                              team1.colors[0],
                              team1.name + " Time on Ice",
                              '5v5');
      let t2_lines_toi = bar_chart('t2_lines_toi',
                              'horizontalBar',
                              team2.lines.toi,
                              "Time on Ice",
                              team2.lines.names,
                              team2.colors[0],
                              team2.name + " Time on Ice",
                              '5v5');

      let t1_lines_cf = bar_chart('t1_lines_cf',
                              'horizontalBar',
                              team1.lines.cf,
                              "Shot Share",
                              team1.lines.names,
                              team1.colors[0],
                              team1.name + " Shot Share",
                              '5v5');
      let t2_lines_cf = bar_chart('t2_lines_cf',
                              'horizontalBar',
                              team2.lines.cf,
                              "Shot Share",
                              team2.lines.names,
                              team2.colors[0],
                              team2.name + " Shot Share",
                              '5v5');

      let t1_lines_xgf = bar_chart('t1_lines_xgf',
                              'horizontalBar',
                              team1.lines.xgf,
                              "Expected Goal Differential",
                              team1.lines.names,
                              team1.colors[0],
                              team1.name + " Expected Goal Differential",
                              '5v5');
      let t2_lines_xgf = bar_chart('t2_lines_xgf',
                              'horizontalBar',
                              team2.lines.xgf,
                              "Expected Goal Differential",
                              team2.lines.names,
                              team2.colors[0],
                              team2.name + " Expected Goal Differential",
                              '5v5');



}
