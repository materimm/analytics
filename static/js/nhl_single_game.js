function get_game_stats(game_stats) {
      team1 = game_stats[0];
      team2 = game_stats[1];

      t1_final_stats = team1.periods[team1.periods.length - 1];
      t2_final_stats = team2.periods[team2.periods.length - 1];


      let datasets = [];
      datasets.push({
        label: team1.name,
        data: [t1_final_stats.cf, t1_final_stats.xgf, t1_final_stats.hdcf],
        backgroundColor: hexToRgbA(team1.colors[0], 0.6),
        borderColor: team1.colors[0],
        borderWidth: 2
      });
      datasets.push({
        label: team2.name,
        data: [t2_final_stats.cf, t2_final_stats.xgf, t2_final_stats.hdcf],
        backgroundColor: hexToRgbA(team2.colors[0], 0.6),
        borderColor: team2.colors[0],
        borderWidth: 2
      });

      let overall_stats_chart = stacked_bar_chart('overall_stats',
                                          'horizontalBar',
                                          datasets,
                                          ['Shot Share (CF%)', 'Expected Goal Differential (xGF%)', 'High Danger Shot Share (HDCF%)'],
                                          team1.name + ' vs ' + team2.name,
                                          '5v5',
                                          'Natural Stat Trick (@natstattrick)');

      let scatter_ds = [];
      for(let i=0; i<team1.skaters.xgf.length; i++) {
          let data = {
            x: team1.name,
            y: team1.skaters.xgf[i]
          };
          scatter_ds.push({
            label: team1.skaters.names[i],
            pointRadius: 5,
            borderColor: team1.colors[0],
            backgroundColor: team1.colors[0],
            data: [data]
          });
      }
      for(let i=0; i<team2.skaters.xgf.length; i++) {
          let data = {
            x: team2.name,
            y: team2.skaters.xgf[i]
          };
          scatter_ds.push({
            label: team2.skaters.names[i],
            pointRadius: 5,
            borderColor: team2.colors[0],
            backgroundColor: team2.colors[0],
            data: [data]
          });
      }

      let threshold = Array(4).fill(50);
      scatter_ds.push({
        label: "Threshold Line",
        fill: false,
        borderColor: "#000",
        backgroundColor: "#000",
        pointRadius: 0,
        data: threshold
      });

      x = {
        scaleLabel: {
          display: true,
          labelString: 'Team',
        }
      };

      y = {
        scaleLabel: {
          display: true,
          labelString: 'xGF%',
        }
      };
      line_chart_with_point_labels('xgf%',
                ["", team1.name, team2.name, ""],
                scatter_ds,
                'On Ice xGF%',
                '5v5',
                x, y,
                'Natural Stat Trick (@natstattrick)')


      //skater stats
      let t1_toi = bar_chart('t1_skaters_toi',
                              'bar',
                              team1.skaters.toi,
                              "Time on Ice",
                              team1.skaters.names,
                              [team1.colors[0]],
                              team1.name + " Time on Ice",
                              '5v5',
                              'Natural Stat Trick (@natstattrick)');
      let t2_toi = bar_chart('t2_skaters_toi',
                              'bar',
                              team2.skaters.toi,
                              "Time on Ice",
                              team2.skaters.names,
                              [team2.colors[0]],
                              team2.name + " Time on Ice",
                              '5v5',
                              'Natural Stat Trick (@natstattrick)');

      let t1_cf = bar_chart('t1_skaters_cf',
                              'bar',
                              team1.skaters.cf,
                              "Shot Share",
                              team1.skaters.names,
                              [team1.colors[0]],
                              team1.name + " Shot Share",
                              '5v5',
                              'Natural Stat Trick (@natstattrick)');
      let t2_cf = bar_chart('t2_skaters_cf',
                              'bar',
                              team2.skaters.cf,
                              "Shot Share",
                              team2.skaters.names,
                              [team2.colors[0]],
                              team2.name + " Shot Share",
                              '5v5',
                              'Natural Stat Trick (@natstattrick)');

      let t1_xgf = bar_chart('t1_skaters_xgf',
                              'bar',
                              team1.skaters.xgf,
                              "Expected Goal Differential",
                              team1.skaters.names,
                              [team1.colors[0]],
                              team1.name + " Expected Goal Differential",
                              '5v5',
                              'Natural Stat Trick (@natstattrick)');
      let t2_xgf = bar_chart('t2_skaters_xgf',
                              'bar',
                              team2.skaters.xgf,
                              "Expected Goal Differential",
                              team2.skaters.names,
                              [team2.colors[0]],
                              team2.name + " Expected Goal Differential",
                              '5v5',
                              'Natural Stat Trick (@natstattrick)');

      //Line stats
      let t1_lines_toi = bar_chart('t1_lines_toi',
                              'horizontalBar',
                              team1.lines.toi,
                              "Time on Ice",
                              team1.lines.names,
                              [team1.colors[0]],
                              team1.name + " Time on Ice",
                              '5v5',
                              'Natural Stat Trick (@natstattrick)');
      let t2_lines_toi = bar_chart('t2_lines_toi',
                              'horizontalBar',
                              team2.lines.toi,
                              "Time on Ice",
                              team2.lines.names,
                              [team2.colors[0]],
                              team2.name + " Time on Ice",
                              '5v5',
                              'Natural Stat Trick (@natstattrick)');

      let t1_lines_cf = bar_chart('t1_lines_cf',
                              'horizontalBar',
                              team1.lines.cf,
                              "Shot Share",
                              team1.lines.names,
                              [team1.colors[0]],
                              team1.name + " Shot Share",
                              '5v5',
                              'Natural Stat Trick (@natstattrick)');
      let t2_lines_cf = bar_chart('t2_lines_cf',
                              'horizontalBar',
                              team2.lines.cf,
                              "Shot Share",
                              team2.lines.names,
                              [team2.colors[0]],
                              team2.name + " Shot Share",
                              '5v5',
                              'Natural Stat Trick (@natstattrick)');

      let t1_lines_xgf = bar_chart('t1_lines_xgf',
                              'horizontalBar',
                              team1.lines.xgf,
                              "Expected Goal Differential",
                              team1.lines.names,
                              [team1.colors[0]],
                              team1.name + " Expected Goal Differential",
                              '5v5',
                              'Natural Stat Trick (@natstattrick)');
      let t2_lines_xgf = bar_chart('t2_lines_xgf',
                              'horizontalBar',
                              team2.lines.xgf,
                              "Expected Goal Differential",
                              team2.lines.names,
                              [team2.colors[0]],
                              team2.name + " Expected Goal Differential",
                              '5v5',
                              'Natural Stat Trick (@natstattrick)');



}
