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
      gradient.addColorStop(0, 'rgba(0, 45, 128, 0.4)');
      gradient.addColorStop(ratio, 'rgba(0, 45, 128, 0.4)');
      gradient.addColorStop(ratio, 'rgba(247, 73, 2, 0.4)');
      gradient.addColorStop(1, 'rgba(247, 73, 2, 0.4)');
      this.chart.data.datasets[0].backgroundColor = gradient;

      return Chart.controllers.line.prototype.update.apply(this, arguments);
    }
  });

  var ctx = document.getElementById("myChart").getContext("2d");

  var myLineChart = new Chart(ctx, {
    type: 'NegativeTransparentLine',
    data: {
      labels: game_obj.shot_flow_time,
      datasets: [{
        label: "My First dataset",
        yAxisID : 'y-axis-0',
        strokeColor: "rgba(60,91,87,1)",
        pointColor: "rgba(60,91,87,1)",
        pointStrokeColor: "#58606d",
        data: game_obj.shot_flow,
      }]
    }
  });

}

function shots_pie_chart(shots) {
  // set the dimensions and margins of the graph
  var width = 450
      height = 450
      margin = 40

  // The radius of the pieplot is half the width or half the height (smallest one). I subtract a bit of margin.
  var radius = Math.min(width, height) / 2 - margin

  // append the svg object to the div called 'my_dataviz'
  var svg = d3.select("#shots")
    .append("svg")
      .attr("width", width)
      .attr("height", height)
    .append("g")
      .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

  // Create dummy data
  //var data = {a: 9, b: 20, c:30, d:8, e:12}
  h_name = shots.home.name
  a_name = shots.away.name
  var data = {}
  data[h_name] = shots.home.shots
  data[a_name] = shots.away.shots

/*
  $.getJSON('./../json/team_abbrevs.json', function(json) {
    console.log(json); // this will show the info it in firebug console
});

  nhl_abbrevs = require('./../json/team_abbrevs.json')
  nhl_colors = require('./../json/nhl_team_colors.json')
  h_shorthand = nhl_abbrevs[h_name]
  a_shorthand = nhl_abbrevs[a_name]
  h_colors = nhl_colors[h_shorthand]
  a_colors = nhl_colors[a_shorthand]
  console.log(h_shorthand + "|" + h_colors)
  console.log(a_shorthand + "|" + a_colors)
*/

  // set the color scale
  var color = d3.scaleOrdinal()
    .domain(data)
    .range(["#002D80", "#F47D30"])

  // Compute the position of each group on the pie:
  var pie = d3.pie()
    .value(function(d) {return d.value; })
  var data_ready = pie(d3.entries(data))

  // shape helper to build arcs:
  var arcGenerator = d3.arc()
    .innerRadius(0)
    .outerRadius(radius)

  // Build the pie chart: Basically, each part of the pie is a path that we build using the arc function.
  svg
    .selectAll('mySlices')
    .data(data_ready)
    .enter()
    .append('path')
    .attr('d', arcGenerator)
    .attr('fill', function(d){ return(color(d.data.key)) })
    .attr("stroke", "black")
    .style("stroke-width", "2px")
    .style("opacity", 0.7)

  // Now add the annotation. Use the centroid method to get the best coordinates
  svg
    .selectAll('mySlices')
    .data(data_ready)
    .enter()
    .append('text')
    .text(function(d){ return d.data.key + " shots: " + d.data.value})
    .attr("transform", function(d) { return "translate(" + arcGenerator.centroid(d) + ")";  })
    .style("text-anchor", "middle")
    .style("font-size", 13)
}
