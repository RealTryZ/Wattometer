import octoprint.plugin
import octoprint.events
import octoprint.logging
import octoprint.events
from octoprint.util import RepeatedTimer

from fritzconnection import FritzConnection


class Wattometer(octoprint.plugin.StartupPlugin,
                 octoprint.plugin.TemplatePlugin,
                 octoprint.plugin.SettingsPlugin,
                 octoprint.plugin.AssetPlugin,
                 octoprint.plugin.EventHandlerPlugin):

    def __init__(self):
        self.fc = None
        self.watt = 0
        self.printRunning = False
        self.printDone = False

    def get_settings_defaults(self):
        return dict(
            address="fritz.box",
            displaytime=60,
            intervall=5
        )

    def on_settings_initialized(self):
        octoprint.plugin.SettingsPlugin.on_settings_initialized(self)
        self.connect()

    def on_settings_save(self, data):
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
        self.connect()

    def connect(self):
        self.fc = FritzConnection(address=self._settings.get(["address"]), user=self._settings.get(["username"]), password=self._settings.get(["password"]))
        self.testConnection()

    def testConnection(self):
        try:
            self.fc.call_http("getswitchpower", self._settings.get(["ain"]))
            self.timer = RepeatedTimer(float(self._settings.get(["intervall"])), self.addWatt, None, None, True)
            self.timer.start()
            self.setConnectionError(False)
        except:
            self.setConnectionError(True)

    def setConnectionError(self, conError):
        self._plugin_manager.send_plugin_message(self._identifier, conError)

    def addWatt(self):
        wattMeasurement = float(self.fc.call_http("getswitchpower", self._settings.get(["ain"]))['content'][:-1]) / 1000
        self.watt = wattMeasurement
        totalWatt = self.addWattToFile(wattMeasurement)
        self._plugin_manager.send_plugin_message(self._identifier, str(self.watt) + "|" + str(totalWatt))

    def addWattToFile(self, watt):
        with open("saveFile.txt", "r+") as file:
            fileContent = file.readline()
            if fileContent == "":
                fileContent = 0
            if self.printDone:
                return float(fileContent)
            if self.printRunning:
                self._plugin_manager.send_plugin_message(self._identifier, "Print_Started")
                wattToWrite = float(fileContent) + watt
                file.seek(0)
                file.write(str(wattToWrite))
                file.truncate()
                return float(fileContent) + watt
            return 0
        
    def resetFile(self):
        with open("saveFile.txt", "w") as file:
            file.write("0")

    def on_event(self, event, payload):
        if event == octoprint.events.Events.PRINT_STARTED:
            self.resetFile()
            self.printRunning = True
            self.printDone = False
        if event == octoprint.events.Events.PRINT_CANCELLING:
            self._plugin_manager.send_plugin_message(self._identifier, "Print_Cancelled")
            self.resetFile()
            self.printRunning = False
            self.printDone = False
        if event == octoprint.events.Events.PRINT_DONE:
            self._plugin_manager.send_plugin_message(self._identifier, "Print_Done")
            self.printRunning = False
            self.printDone = True

    def get_assets(self):
        return dict(
            js=[
                "js/Wattometer.js",
                "js/Chart.js"
            ],
            css=["css/Wattometer.css"]
        )

    def get_template_configs(self):
        return [
            dict(type="tab", template="wattometer_tab.jinja2", custom_bindings=True),
            dict(type="settings", template="wattometer_settings.jinja2", custom_bindings=False)
        ]

    def get_update_information(self):
        return dict(
            Wattometer=dict(
                displayName=self._plugin_name,
                displayVersion=self._plugin_version,

                type="github_release",
                current=self._plugin_version,
                user="RealTryZ",
                repo="Wattometer",

                pip="https://github.com/RealTryZ/Wattometer/archive/{target}.zip"
            )
        )


__plugin_name__ = "Wattometer"
__plugin_pythoncompat__ = ">=3.7,<4"
__plugin_implementation__ = Wattometer()
__plugin_hooks__ = {
    "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
}
