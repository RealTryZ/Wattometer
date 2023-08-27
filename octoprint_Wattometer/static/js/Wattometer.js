$(function() {
    function WattometerViewModel(parameters) {
      var self = this;

      self.connectionError = ko.observable("");

      self.time = 0;

      self.allWatt = 0;
      self.isPrintStarted == false;
      self.isPrintDone;

      self.settings = parameters[0];
      self.labels = [];
      self.watt = ko.observableArray();
      self.totalWatt = ko.observable(0.0);

      self.onAfterBinding = function(){
        var ctx = document.getElementById('myChart').getContext('2d')
        self.chart = new Chart(ctx, {
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
      
      self.onBeforeBinding = function(){
        var existingProgressBar = $("#job_progressBar");
        var parentDivProgressBar = existingProgressBar.parent();
        if(parentDivProgressBar.length) {
          var wattElement = $("<div><span title='Total power-usage of current print'>Power-Usage</span>: " +
          "<strong id='power_usage' data-bind='text: totalWatt'></strong><strong> Wh</strong></div>");
          wattElement.insertBefore(parentDivProgressBar);
        }
      }

      self.onDataUpdaterPluginMessage = function(plugin, data) {
        if(plugin !== "Wattometer") return;

        if(data == true) {
          self.connectionError("Failed to initialize connection. Likely incorrect credential or permission of user account.")
          console.log(self.connectionError())
          return
        } else if(data == false) {
          self.connectionError("")
          console.log(self.connectionError())
          return
        } else if (data == "Reset"){
          self.allWatt = 0
          self.totalWatt(0.0);
          return
        } else if (data == "Print_Done" || data == "Print_Cancelled") {
          self.isPrintDone = true
          return
        } else if (data == "Print_Started") {
          self.isPrintStarted = true
          self.isPrintDone = false
          console.log("Data:" + data, "PrintStarted: " + self.isPrintStarted + " ,PrintDone: " + !self.isPrintDone)
          return
        };

        

        if(!self.isPrintDone && self.isPrintStarted) {
          self.allWatt += (parseFloat(data) * (parseInt(self.settings.settings.plugins.Wattometer.intervall()) / 3600)); 
          self.totalWatt(self.allWatt.toFixed(2)); 
        }

        self.watt.push(parseFloat(data));

        if (self.time >= -parseInt(self.settings.settings.plugins.Wattometer.displaytime())) {
          self.labels.unshift(self.time);
          self.time -= parseInt(self.settings.settings.plugins.Wattometer.intervall());
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
    }

    // This is how our plugin registers itself with the application, by adding some configuration
    // information to the global variable OCTOPRINT_VIEWMODELS
    OCTOPRINT_VIEWMODELS.push([
        WattometerViewModel,

        ["settingsViewModel", "printerStateViewModel"],

        ["#tab_plugin_Wattometer", "#power_usage"]
    ]);
});