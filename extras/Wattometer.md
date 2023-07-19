---
layout: plugin

id: Wattometer
title: Wattometer
description: Get an overview of the used power for a print via FRITZ!DECT 200.
authors:
- Pascal Witt
license: AGPLv3

date: 2023-07-17

homepage: https://github.com/RealTryZ/Wattometer
source: https://github.com/RealTryZ/Wattometer
archive: https://github.com/RealTryZ/Wattometer/archive/master.zip

# TODO
# Set this to true if your plugin uses the dependency_links setup parameter to include
# library versions not yet published on PyPi. SHOULD ONLY BE USED IF THERE IS NO OTHER OPTION!
#follow_dependency_links: false


tags:
- watt measurement
- fritz
- fritz dect
- power measurement


# TODO
# When registering a plugin on plugins.octoprint.org, all screenshots should be uploaded not linked from external sites.
screenshots:
- url: url of a screenshot, /assets/img/...
  alt: alt-text of a screenshot
  caption: caption of a screenshot
- url: url of another screenshot, /assets/img/...
  alt: alt-text of another screenshot
  caption: caption of another screenshot
- ...

# TODO
featuredimage: url of a featured image for your plugin, /assets/img/...


compatibility:

  octoprint:
  - 1.4.0

  os:
  - linux
  - windows
  - macos
  - freebsd

  python: ">=3,<4"

---

# Plugin Setup
Once the plugin is installed, you will have to enter your FRITZ username and password in the settings tab.
If you don't habe an account yet, the following [guide](https://en.avm.de/service/knowledge-base/dok/FRITZ-Box-7590/966_Creating-a-MyFRITZ-account-and-setting-it-up-in-the-FRITZ-Box/) will help you to create one. 
For security reasons, it is recommended to create a dedicated user account on your FRITZ!Box with *only* Smart Home privileges.

Furthermore you will have to enter the AIN of your FRITZ smart plug. This [tutorial](https://en.avm.de/service/knowledge-base/dok/FRITZ-DECT-200/3269_Setting-up-the-switch-on-sound-function-for-FRITZ-DECT-smart-plug/) will help you to find the AIN of your device.

# Plugin Description
Wattometer displays the measured power usage of your FRITZ!Dect 200 device in OctoPrint.
It displays watt measurements for up to a minute in a graph and sums up the total watt usage.


