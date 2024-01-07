$(function () {
  // =====================================
  // Profit
  // =====================================

  function fetchData() {
    $.ajax({
      url: "/transactions/sales-data", // Replace with your actual Flask route
      method: "GET",
      dataType: "json",
      success: function (response) {
        var data = response.data;
        if (Array.isArray(data)) {
          var earningsData = data.map(function (item) {
            return item.total_transactions;
          });

          // Get only the first 6 elements
          var truncatedData = earningsData.slice(0, 6);

          console.log("test", truncatedData);

          // Update the chart series with the fetched data
          chart.updateSeries([
            {
              name: "Earnings this month:",
              data: truncatedData,
            },
          ]);
        } else {
          console.error(
            "Invalid data structure received from the server:",
            data
          );
        }
      },
      error: function (xhr, status, error) {
        console.error("Error fetching data:", error);
      },
    });
  }

  var chartOptions = {
    series: [
      {
        name: "Earnings this month:",
        data: [],
        // data: [355, 390, 300, 350, 390, 180],
      },
      // { name: "Expense this month:", data: [280, 250, 325, 215, 250, 310, 280, 250] },
    ],

    chart: {
      type: "bar",
      height: 345,
      offsetX: -15,
      toolbar: { show: true },
      foreColor: "#adb0bb",
      fontFamily: "inherit",
      sparkline: { enabled: false },
    },

    colors: ["#5D87FF", "#49BEFF"],

    plotOptions: {
      bar: {
        horizontal: false,
        columnWidth: "35%",
        borderRadius: [6],
        borderRadiusApplication: "end",
        borderRadiusWhenStacked: "all",
      },
    },
    markers: { size: 0 },

    dataLabels: {
      enabled: false,
    },

    legend: {
      show: false,
    },

    grid: {
      borderColor: "rgba(0,0,0,0.1)",
      strokeDashArray: 3,
      xaxis: {
        lines: {
          show: false,
        },
      },
    },

    xaxis: {
      type: "category",
      categories: ["Mei", "Juni", "Juli", "Agustus", "September", "Oktober"],
      labels: {
        style: { cssClass: "grey--text lighten-2--text fill-color" },
      },
    },

    yaxis: {
      show: true,
      min: 0,
      max: 16000,
      tickAmount: 4,
      labels: {
        style: {
          cssClass: "grey--text lighten-2--text fill-color",
        },
      },
    },
    stroke: {
      show: true,
      width: 3,
      lineCap: "butt",
      colors: ["transparent"],
    },

    tooltip: { theme: "light" },

    responsive: [
      {
        breakpoint: 600,
        options: {
          plotOptions: {
            bar: {
              borderRadius: 3,
            },
          },
        },
      },
    ],
  };

  var chart = new ApexCharts(document.querySelector("#chart"), chartOptions);
  chart.render();

  fetchData();

  setInterval(fetchData, 60000);
});
