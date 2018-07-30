PiHud
=====

Configurable heads up display fit for the Raspberry Pi

*Warning: This project is mostly for experimenting with the underlying [OBD library](https://github.com/brendan-w/python-OBD).*

Turning your Pi into a PiHud
----------------------------

For installation instructions on different platforms, see the [GitHub wiki](https://github.com/brendan-w/piHud/wiki)

First, it is recommended that you start with a clean install of [Raspbian](http://www.raspberrypi.org/downloads/). On first boot, it will prompt you with a setup screen. After you have expanded the filesystem and set your password, enter the listing named `Enable Boot to Desktop/Scratch`. In this option, make sure to select the console only option, in order to prevent the Pi from starting its desktop environment on boot `Console Text console, requiring login`. You can now click finish, and boot your Pi.

After loging in, you will be presented with a terminal. Please install the following dependencies, and clone the repo

```shell
sudo apt-get install python-qt4
sudo apt-get install python-pip
git clone https://github.com/jackslegion/piHud.git pihud
cd pihud/
sudo python setup.py install
```

In order to run PiHud on boot, you will need to tweak a few config files (note: most of the following was taken from [this post](http://www.raspberrypi.org/forums/viewtopic.php?p=344408)). Open the file /etc/rc.local in a text editor of your choice. Add the following line just before the exit 0

```shell
su -s /bin/bash -c startx pi &
```

Now, in order to allow X sessions for all users, run the following command, and choose Anybody from the list of options

```shell
sudo dpkg-reconfigure x11-common
```

Finally, create an .xinitrc file (if you don’t have one already), in your home directory

```shell
touch ~/.xinitrc
```

Open it in a text editor of your choice, and add the following line:

```shell
python -m piHud
```

Your done! You can now reboot the Pi with:

```python
sudo shutdown -r 0
```

Configuring
-----------

PiHud is configured by modifying a file named `pihud.rc` in your home directory. This file will be created the first time piHud runs. However, a few settings are accessible through the piHud app itself. To move widgets, simply click and drag them around the screen. Right clicking on widgets will tell you which sensor they are tied to, and allow you to delete them. Right clicking on the black background (not on a widget), will let you add widgets or pages to your HUD. By default, page switching can be done with the `TAB` key.

All other settings are available in the pihud.rc file, which is structured in `json`. A few items of note in this file:

-   The `sensor` field is the string name for any sensor your car supports. A full list can be found in the [python-OBD wiki](http://python-obd.readthedocs.io/en/latest/Command%20Tables/)
-   The `type` field selects the way data is displayed. Values can be: `Gauge`, `Bar`, or `Text`.
-   All color attributes accept CSS color values
-   The `page_adv_pin` setting is used to tie the page cycling to any of the Pi’s GPIO pins. Simply wire a button that grounds the set pin while pressed.
-   The `demo` key is used to feed a sin() curve into all widgets for testing.
-   The `debug` key is used to turn python-OBD's debug printing on and off. If enabled, you will see OBD debug information being printed to `stderr`.
