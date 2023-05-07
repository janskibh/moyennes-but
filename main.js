fetch("notes.json")
  .then(response => response.json())
  .then(data => {
    console.log(data)
    // Récupération des données pour chaque UE
    const ue1 = data.ressources.BRT2UE1;
    const ue2 = data.ressources.BRT2UE2;
    const ue3 = data.ressources.BRT2UE3;

    // Création des graphes
    const chart1 = new ApexCharts(document.querySelector("#chart1"), getChartOptions(ue1, "UE1"));
    const chart2 = new ApexCharts(document.querySelector("#chart2"), getChartOptions(ue2, "UE2"));
    const chart3 = new ApexCharts(document.querySelector("#chart3"), getChartOptions(ue3, "UE3"));
    const chart4 = new ApexCharts(document.querySelector("#chart4"), getChart4Options(data, "Moyennes UES"));
    const chart5 = new ApexCharts(document.querySelector("#chart5"), getChart5Options(data));

    // Affichage des graphes
    chart1.render();
    chart2.render();
    chart3.render();
    chart4.render();
    chart5.render();
  });

function getChartOptions(ue, name) {

  const moyennes = [];
  const labels = [];
  const colors = [];

  // Récupération des moyennes et des labels pour chaque ressource
  for (const ressource in ue) {
    moyennes.push(ue[ressource].moyenne);
    labels.push([`${ue[ressource].titre} (${ue[ressource].coeff})`]);
    colors.push(ue[ressource].couleur)
  }

  // Options pour le graphe
  const options = {
    series: [{
      name: "Moyenne",
      data: moyennes
    },],
    chart: {
      type: 'bar',
      height: 400,
      width: 800,
      background: '#1f1f1f'
    },
    plotOptions: {
      bar: {
        horizontal: false,
        distributed: true,
        borderRadius: 2,
      }
    },
    legend: {
      show: false
    },
    colors: colors,
    annotations: {
      yaxis: [{
        y: 0,
        y2: 8,
        borderColor: '#b62828',
        fillColor: '#b62828',
        opacity: 0.2,
      },{
      y: 8,
      y2: 10,
        borderColor: '#deb62f',
        fillColor: '#deb62f',
        opacity: 0.2,
      }]
    },
    xaxis: {
      categories: labels
    },
    yaxis: {
      max: 20
    },
    title: {
      text: name,
      align: 'center',
      margin: 10,
      offsetX: 0,
      offsetY: 0,
      floating: false,
      style: {
        fontSize:  '20px',
        fontWeight:  'bold',
        fontFamily:  undefined,
        color:  '#fff'
      },
    },  
    theme: {
      mode: 'dark', 
      palette: 'palette6', 
    }
  };

  return options;
}

function getChart4Options(data, name) {

  const moyennes = [];
  const labels = [];
  const colors = [];

  // Récupération des moyennes et des labels pour chaque ressource
  for (const ue in data.ues) {
    moyennes.push(data.ues[ue].moyenne);
    labels.push([`${ue}`]);
    colors.push(data.ues[ue].couleur)
  }

  // Options pour le graphe
  const options = {
    series: [{
      name: "Moyenne",
      data: moyennes
    }],
    chart: {
      type: "bar",
      height: 400,
      width: 800,
      background: '#1f1f1f'
    },
    plotOptions: {
      bar: {
        horizontal: false,
        distributed: true,
        endingShape: 'rounded',
      }
    },
    legend: {
      show: false
    },
    colors: colors,
    annotations: {
      yaxis: [{
        y: 0,
        y2: 8,
        borderColor: '#b62828',
        fillColor: '#b62828',
        opacity: 0.2,
      },{
      y: 8,
      y2: 10,
        borderColor: '#deb62f',
        fillColor: '#deb62f',
        opacity: 0.2,
      }]
    },
    xaxis: {
      categories: labels
    },
    yaxis: {
      max: 20
    },
    title: {
      text: name,
      align: 'center',
      margin: 10,
      offsetX: 0,
      offsetY: 0,
      floating: false,
      style: {
        fontSize:  '20px',
        fontWeight:  'bold',
        fontFamily:  undefined,
        color:  '#fff'
      },
    },  
    theme: {
      mode: 'dark', 
      palette: 'palette1', 
      monochrome: {
          enabled: false,
          color: '#255aee',
          shadeTo: 'dark',
          shadeIntensity: 0.65
      },
    }
  };

  return options;
}

function getChart5Options(data) {

  const absences = data.absences.total;
  const absences_injustifie = data.absences.injustifie;
  const abs_percent = (absences_injustifie/5)*100;
  var color;
  if (absences <= 1) {
    color = "#178100"
  } else if (absences == 2) {
    color = "#00FF00"
  } else if (absences == 3) {
    color = "#FFFF00"
  } else if (absences == 4) {
    color = "#FF7500"
  } else if (absences >= 5) {
    color = "#FF0000"
  };
  const options = {
    chart: {
      height: 200,
      type: "radialBar",
    },
    series: [abs_percent],
    colors: [color],
    plotOptions: {
      radialBar: {
        startAngle: -135,
        endAngle: 135,
        track: {
          background: '#333',
          startAngle: -135,
          endAngle: 135,
        },
        dataLabels: {
          name: {
            offsetY: 10,
            fontSize: "30px",
            show: true,
            label: "Absences"
          },
          value: {
            fontSize: "10px",
            show: false,
            color: "#fff",
          }
        }
      }
    },
    labels: [[`${absences_injustifie}/${absences}`]],
    stroke: {
      lineCap: "round"
    }
  };

  // Options pour le graphe
  
  return options;
}