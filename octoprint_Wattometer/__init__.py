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

    def connect(self):
        try:
            self.fc = FritzConnection(address=self._settings.get(["address"]), user=self._settings.get(["username"]), password=self._settings.get(["password"]))
        except:
            self._logger.exception("Failed to initialize connection. Likely incorrect credential or permission of user account.")

    def get_settings_defaults(self):
        return dict(
            address="fritz.box"
        )

    def on_settings_initialized(self):
        self.connect()

    def addWatt(self):
        wattMeasurement = float(self.fc.call_http("getswitchpower", self._settings.get(["ain"]))['content'][:-1]) / 1000
        self.watt = wattMeasurement
        self._plugin_manager.send_plugin_message(self._identifier, self.watt)
        self._logger.info(self.watt)

    def on_event(self, event, payload):
        if event == octoprint.events.Events.PRINT_STARTED:
            self.timer = RepeatedTimer(10, self.addWatt, None, None, True)
            self.timer.start()
        if event == octoprint.events.Events.PRINT_CANCELLED or event == octoprint.events.Events.PRINT_DONE:
            self._plugin_manager.send_plugin_message(self._identifier, "Reset")
            self.timer.cancel()

    def get_assets(self):
        return dict(
            js=["js/Wattometer.js"],
            less=["less/Wattometer.less"]
        )

    def get_template_configs(self):
        return [
            dict(
                type="settings",
                custom_bindings=False
            )
        ]


__plugin_name__ = "Wattometer"
__plugin_pythoncompat__ = ">=3.7,<4"
__plugin_implementation__ = Wattometer()