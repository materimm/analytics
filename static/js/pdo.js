

//document.addEventListener('DOMContentLoaded', function(e) {
function pdo(pdos) {
    console.log(JSON.stringify(pdos));

    // set the dimensions and margins of the graph
    var margin = {top: 30, right: 30, bottom: 70, left: 60},
        width = 460 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var svg = d3.select(".pdo_chart")
      .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")");

    // X axis
    var x = d3.scaleBand()
      .range([ 0, width ])
      .domain(pdos.map(function(d) { return d.team; }))
      .padding(0.2);
    svg.append("g")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x))
      .selectAll("text")
        .attr("transform", "translate(-10,0)rotate(-45)")
        .style("text-anchor", "end");

    // Add Y axis
    var y = d3.scaleLinear()
      .domain([0, 2])
      .range([ height, 0]);
    svg.append("g")
      .call(d3.axisLeft(y));

    // Bars
    svg.selectAll("mybar")
      .data(pdos)
      .enter()
      .append("rect")
        .attr("x", function(d) { return x(d.team); })
        .attr("y", function(d) { return y(d.pdo); })
        .attr("width", x.bandwidth())
        .attr("height", function(d) { return height - y(d.pdo); })
        .attr("fill", "#69b3a2")
/* ---------------------------------------------------------
  var data = [4, 8, 15, 16, 23, 42];

  var x = d3.scale.linear()
      .domain([0, d3.max(data)])
      .range([0, 420]);

  d3.select(".pdo_chart")
      .selectAll("div")
      .data(data)
      .enter().append("div")
      .style("width", function(d) { return x(d) + "px"; })
      .text(function(d) { return d; });
------------------------------------------------------ */
}
