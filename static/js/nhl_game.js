/**
*
**/
function shot_flow_chart(game_obj) {
  Chart.defaults.NegativeTransparentLine = Chart.helpers.clone(Chart.defaults.line);
  Chart.controllers.NegativeTransparentLine = Chart.controllers.line.extend({
    update: function() {
      // get the min and max values
      var min = Math.min.apply(null, this.chart.data.datasets[0].data);
      var max = Math.max.apply(null, this.chart.data.datasets[0].data);
      var yScale = this.getScaleForId(this.getDataset().yAxisID);

      // figure out the pixels for these and the value 0
      var top = yScale.getPixelForValue(max);
      var zero = yScale.getPixelForValue(0);
      var bottom = yScale.getPixelForValue(min);

      // build a gradient that switches color at the 0 point
      var ctx = this.chart.chart.ctx;
      var gradient = ctx.createLinearGradient(0, top, 0, bottom);
      var ratio = Math.min((zero - top) / (bottom - top), 1);
      gradient.addColorStop(0, 'rgba(0, 45, 128, 0.6)');
      gradient.addColorStop(ratio, 'rgba(0, 45, 128, 0.6)');
      gradient.addColorStop(ratio, 'rgba(247, 73, 2, 0.6)');
      gradient.addColorStop(1, 'rgba(247, 73, 2, 0.6)');
      this.chart.config.data.datasets[0].backgroundColor = gradient;

      return Chart.controllers.line.prototype.update.apply(this, arguments);
    }
  });

  var ctx = document.getElementById("shot_flow_chart").getContext("2d");

  var myLineChart = new Chart(ctx, {
    type: 'NegativeTransparentLine',
    data: {
      labels: game_obj.shot_flow_time,
      datasets: [{
        label: "Shot Flow",
        yAxisID : 'y-axis-0',
        strokeColor: "rgba(60,91,87,1)",
        pointColor: "rgba(60,91,87,1)",
        pointStrokeColor: "#58606d",
        data: game_obj.shot_flow,
      }]
    }
  });

}

/**
*
**/
function shots_per_60_chart(shots_per_60_obj) {
  var ctx = document.getElementById("shots_per_60_chart").getContext("2d");

  var myLineChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: shots_per_60_obj.home_shots_per_60_time,
      datasets: [{
        label: "Home Team Shot Pressure",
        strokeColor: "rgba(0, 45, 128, 1)",
        pointColor: "rgba(0, 45, 128, 1)",
        backgroundColor: "rgba(0, 45, 128, 0.6)",
        pointStrokeColor: "#002D80",
        data: shots_per_60_obj.home_shots_per_60,
      }]
    }
  });
}

function shots_pie_chart(shots) {
  var config = {
			type: 'doughnut',
			data: {
				datasets: [{
					data: [
						shots.home.shots,
						shots.away.shots
					],
					backgroundColor: [
            hexToRgbA(shots.home.colors[0], 0.7),
						hexToRgbA(shots.away.colors[0], 0.7)
					],
          // borderColor: [
          //   shots.home.colors[0],
					// 	shots.away.colors[0],
          // ],
					label: 'Home vs Away shots'
				}],
				labels: [
          shots.home.name,
          shots.away.name,
				]
			},
			options: {
				responsive: true,
				legend: {
					position: 'top',
				},
				title: {
					display: true,
					text: 'Shots'
				},
				animation: {
					animateScale: true,
					animateRotate: true
				}
			}
		};

		var ctx = document.getElementById('shots_chart').getContext('2d');
		window.myDoughnut = new Chart(ctx, config);
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
