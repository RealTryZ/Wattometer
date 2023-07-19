$(function() {
    function WattometerViewModel(parameters) {
      var self = this;

      self.time = 0;

      self.allWatt = 0;

      self.settings = parameters[0];
      self.labels = [];
      self.watt = ko.observableArray();
      self.totalWatt = ko.observable();

      self.totalWatt(0);

      self.onDataUpdaterPluginMessage = function(plugin, data) {
        if(plugin !== "Wattometer") return;
        if(data == "Reset"){
          self.totalWatt(0.0);
          self.watt().length = 0;
          self.labels.length = 0;
          addData(self.chart, self.labels, self.watt());
          return
        }

        self.allWatt += (parseFloat(data) * (5 / 3600)); 
        self.totalWatt(self.allWatt.toFixed(2));
        
        self.watt.push(parseFloat(data));

        if (self.time >= -60) {
          self.labels.unshift(self.time);
          self.time -= 5;
          console.log(self.watt)
        } else {
          self.watt.shift();
        }
        addData(self.chart, self.labels, self.watt());
      }

      function addData(chart, label, data) {
        chart.data.labels = label;
        chart.data.datasets.forEach((dataset) => {
            dataset.data = data;
        });
        chart.update();
      }


      self.chart = new Chart("myChart", {
        type: "line",
        data: {
          labels: [],
          datasets: [{
            label: "Watt",
            backgroundColor:"rgba(0,0,255,1.0)",
            borderColor: "rgba(0,10,255,1.0)",
            fill: false,
            data: []
          }]
        },
        options:{
          bezierCurve : false,
          title:{
            display: true,
            text: "Wattometer"
          }
        }
      });
    }

    // This is how our plugin registers itself with the application, by adding some configuration
    // information to the global variable OCTOPRINT_VIEWMODELS
    OCTOPRINT_VIEWMODELS.push([
        // This is the constructor to call for instantiating the plugin
        WattometerViewModel,

        // This is a list of dependencies to inject into the plugin, the order which you request
        // here is the order in which the dependencies will be injected into your view model upon
        // instantiation via the parameters argument
        ["settingsViewModel"],

        // Finally, this is the list of selectors for all elements we want this view model to be bound to.
        ["#tab_plugin_Wattometer"]
    ]);
});