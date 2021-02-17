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
      // scale: {
      //   ticks: {
      //     beginAtZero: true,
      //     max: 60
      //   }
      // }
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
