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
    document.getElementById("cfp").innerHTML = team_stats["corsi_rank"];
  }
  else if(button.innerHTML == "Show Stats") {
    button.innerHTML = "Show Ranks";
    document.getElementById("gf").innerHTML = team_stats["gf"];
    document.getElementById("ga").innerHTML = team_stats["ga"];
    document.getElementById("gfp").innerHTML = team_stats["gf_percent"];
    document.getElementById("ppp").innerHTML = team_stats["pp_percent"];
    document.getElementById("pkp").innerHTML = team_stats["pk_percent"];
    document.getElementById("xgf").innerHTML = team_stats["xgf"];
    document.getElementById("xga").innerHTML = team_stats["xga"];
    document.getElementById("xgfp").innerHTML = team_stats["xgf_percent"];
    document.getElementById("cfp").innerHTML = team_stats["corsi_percent"];
  }
}
