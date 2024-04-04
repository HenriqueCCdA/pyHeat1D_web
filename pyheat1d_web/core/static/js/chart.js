function plot(data) {

  const ctx = document.getElementById('plot_area');
  const configs = {
    elements: {
      point:{
        radius: 0
      }
    },
    plugins: {
      title: {
        display: true,
        text: 'Temperaturas ao longo de X'
      },
    },
    scales: {
      x: {
        display: true,
        title: {
          display: true,
          text: 'x(m)'
        }
      },
      y: {
        display: true,
        title: {
          display: true,
          text: '°C'
        },
        beginAtZero: true
      },
    }
  }

  const graph_data = {
      labels: data.mesh,
      datasets: data.steps.map(element => {
          return {
            label: `Tempo ${element.t} s`,
            data: element.u,
            borderWidth: 1
          }
      })
    }
  new Chart(ctx, {
    type: 'line',
    data: graph_data,
    options:configs,
  });
}

const endpoint = document.currentScript.dataset.endpoint

$.ajax({
  method: "GET",
  url: endpoint,
  success: function(data) {
    plot(data);
  },
  error: function(error_data) {
    console.log(error_data);
  }
})
