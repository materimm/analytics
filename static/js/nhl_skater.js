function get_scoring_chart(stats) {
  let datasets = [];
  for(var i=0; i<stats.data.length; i++) {
    datasets.push({
      label: stats.data_labels[i],
      data: stats.data[i],
      backgroundColor: hexToRgbA(stats.colors[i], 0.6),
      borderColor: stats.colors[i],
      borderWidth: 2
    });
  }

  let scoring_chart = stacked_bar_chart('scoring_locations',
                                      datasets,
                                      stats.labels,
                                      stats.name + " Scoring",
                                      'All | Seasons: ' + stats.seasons,
                                      'moneypuck.com');
}
