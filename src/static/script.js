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
      //Clear the previous graph.
      document.getElementById('myChart').remove();
    //   document.getElementById('graph-div').append('<canvas id="myChart"><canvas>');
        $('#graph-div').append('<canvas id="myChart"><canvas>');
      var myChart = document.getElementById("myChart").getContext("2d");
      var datasets = this.response.datalist.slice();
      // Add random color to each graph.
      datasets.forEach(item => {
          item.borderColor = getRandomColor();
          item.backgroundColor = item.borderColor;
          item.fill = false;
      });

      // Add new chart to the canvas
      var chart = new Chart(myChart, {
        type: "line",
        data: {
          labels: this.response.dates_array,
          datasets: datasets,
        },
        option: {},
      });
      $('html,body').animate({scrollTop: document.body.scrollHeight},2000);
    }
  });
    
  xhr.open("POST", "/graph-data");
  xhr.send(data);
  return true;
}
