# RaspberryPi_Neopixel_HUD
## An experiment in using Neopixel interface as next generation HUD display

The opc.py and color_utils.py are from the openpixelcontrol library. I simply put them here for thoroughness when demoing with Meetup. I will eventually cleanse this repo and hint/point to get the proper libraries installed on host as this project matures. At this point it is standalone, but one should still obtain the openpixelcontrol repo and replace or properly install these files on the host.

** Update the rpm_gauge_obdii.py file with the IP and Port of the target host for fcserver, i.e. the host with Fadecandy**

Once you have the fcserver running on target host for Fadecandy, run the demo program.

```
python rpm_gauge_obdii.py
```

You should see something like this.

```
Connected to 192.168.2.40:7890
```
