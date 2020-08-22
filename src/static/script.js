'use strict';

function plot_graph() {
  const query = document.getElementById("query-input").value;

  var data = new FormData();
  data.append("query",query);

  var xhr = new XMLHttpRequest();
  xhr.addEventListener("readystatechange", function() {
    if(this.readyState === 4) {
      document.getElementById("graph-div").innerHTML = this.response;
      // TODO: INSERT GRAPH.JS GRAPH USING this.response as the data.
      var myChart = document.getElementById("myChart").getContext("2d");
         var chart = new Chart(myChart, {
          type: "line",
          data: {
          labels: states,
          datasets: [
            {
              label: "Confirmed Cases",
              data: confirmed,
              backgroundColor: "#f1c40f",
          
            },
            {
              label: "Recovered",
              data: recovered,
              backgroundColor: "#2ecc71",
            
            },
            {
              label: "Deceased",
              data: deaths,
              backgroundColor: "#e74c3c",
          
            },
          ],
       },
        option: {},
     });
    

  xhr.open("POST", "/graph-data");
  xhr.send(data);
  return true;
}
