'use strict';

function getRandomColor() {
  var letters = '0123456789ABCDEF';
  var color = '#';
  for (var i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}

function plot_graph() {
  const query = document.getElementById("query-input").value;

  var data = new FormData();
  data.append("query",query);

  var xhr = new XMLHttpRequest();
  xhr.responseType = 'json';
  xhr.addEventListener("readystatechange", function() {
    if(this.readyState === 4) {
      var myChart = document.getElementById("myChart").getContext("2d");
      // Add random color to each graph.
      this.response.datalist.forEach( item => {
        item.borderColor = getRandomColor();
        item.fill = false;
      });
      var chart = new Chart(myChart, {
        type: "line",
        data: {
          labels: this.response.dates_array,
          datasets: this.response.datalist,
        },
        option: {},
      });
    }
  });
    
  xhr.open("POST", "/graph-data");
  xhr.send(data);
  return true;
}
