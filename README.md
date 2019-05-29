# Description

This is a package that works with a Raspberry Pi Zero W and provides both a Wifi-to-serial interface and GPS time and location information to a telescope mount. It is based upon the [Raspberry PI wireless Telescope Control][proj-url] project.

Time and location are transferred to the hand controller over USB. The transfer happens automatically when the USB cable between the Pi and the hand controller is plugged in. The display will provide a message when time and location uploads are in progress.

This has been tested with a Celestron Advanced VX equatorial mount with its regular hand controller and the hand controller from a StarSense Auto Align unit.

# Hardware

The included case files assume you're using the following components:  
  
* Raspberry Pi Zero W with a 2x6 header soldered to the top GPIO pads on the front of the board  
* SSD1306 128x32 pixel I2C OLED display (e.g. [this Maker Focus display][oled-url]) with a header soldered on so that the pins are on the back of the board  
* 12V-to-5V converter (e.g. [Pololu D24V10F5][conv-url]) attached to empty GPIO pads at the bottom of the front of the board with double-sided tape  
* Single-board GPS module (e.g. [Gowoops GPS-NEO-6M-001][gps-url] or similar form factor) with a header soldered on so that the pins are on the chip side (not the antenna side)
* Keystone CAT3/RJ12 6P6C modular jack with a maximum body width of 20mm (e.g. [Shaxon BM303W610-B][jack-url])
* Wire and header plugs to electrically connect the components; a 2-pin connector for the power coming from the keystone jack is recommended for ease of assembly
* A case; 3D model files are provided in the [case][case-dir] folder in Fusion 360, STEP, and STL formats for design tweaks and 3D printing

The diagram below shows how I wired up the Pi, OLED, and GPS. I used two 4-position single row female connectors (denoted by the green and red boxes; note that one position in the OLED connector is empty) and wired both modules' Vcc into pin 1 on the Pi using a single terminal and heat shrink tubing (denoted by the cyan box; the terminal was too full to fit in a 1-position housing). I used a header only long enough for the number of GPIB rows affected (six), which allows the header and connectors to fit into the open area designed into the case and the rest of the Pi to lie flat against the posts.
![Wiring diagram](./Module-wiring-diagram.png)
The power from the voltage converter is fed into the solder pads on the bottom of the Pi, under the USB power connector, to take advantage of the fuses in the USB power feed.
![Wiring diagram back](./Module-wiring-diagram-back.png)

# Software Installation

After setting up the wifi in the Pi (editing the wpa_supplicant.conf file), software installation is simple:

1. Download the distribution from GitHub either via a git clone or as a zip file. If downloaded as a zip, unzip it. You will now have an "astro" folder.  
2. Run the following commands:  

	`cd <path-to-astro-folder>`  
	`sudo cp etc /`  
	`sudo cp usr /`  
3. Follow the instructions in the [base project][proj-url] to update the Pi's OS and install/configure the ser2net and gpsd services. The
autohotspot service will be installed by the action in step 2, but if you need to make changes to the network name or WPA passphrase for the hotspot, do it now.
4. Enable the services that were installed in step 2. The sethctimeloc enable will complain of a lack of an installation config: just ignore it because installation is done when the USB cable is plugged in.  

	`sudo systemctl enable autohotspot`  
	`sudo systemctl enable forcetimeupdate`  
	`sudo systemctl enable sethctimeloc`  
	`sudo systemctl enable gpsdisplay`  

Then just reboot and you should have a fully operational system.

[proj-url]: https://hackaday.io/project/162681-raspberry-pi-wireless-telescope-control
[oled-url]: https://smile.amazon.com/gp/product/B079BN2J8V/
[conv-url]: https://www.pololu.com/product/2831
[gps-url]: https://smile.amazon.com/gp/product/B01AW5QYES/
[jack-url]: https://smile.amazon.com/Shaxon-Cat3-Keystone-White-BM303W610-B/dp/B00J8D0LT0/  
[case-dir]: ./case

