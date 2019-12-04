## Description

bt_monitor is a python application that receives scan requests for specific bluetooth devices via MQTT, completes the scans and returns the results via MQTT. This project was inspired by [Andrew Freyer's montor script](https://github.com/andrewjfreyer/monitor) and makes use of the confidence concept introduced there as well as well as some of the Raspberry Pi and home assistant setup instructions. The overall structure and method of deployment of this program was adapted from [GarageQTPi](https://github.com/Jerrkawz/GarageQTPi)

## Hardware

This application is intended to run on a pi-zero W (or a raspberry pi). Dedicating use of the bluetooth interface to this application is recommended.

## Installation Instructions for Raspberry Pi Zero W
### Setup of SD Card
1. Download latest version of raspbian buster lite [here](https://www.raspberrypi.org/downloads/raspbian/)

2. Download etcher from [etcher.io](https://www.balena.io/etcher/)

3. Image raspbian buster to SD card. Instructions [here] (https://magpi.raspberrypi.org/articles/pi-sd-etcher).

4. Mount boot partition of imaged SD card (unplug it and plug it back in)

5. To enable ssh, create blank file, without any extension, in the root directory called ssh

6. To setup Wi-Fi, create wpa_supplicant.conf file in root directory and add Wi-Fi details for home Wi-Fi:

```
country=US
    ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
    update_config=1

network={
    ssid="Your Network Name"
    psk="Your Network Password"
    key_mgmt=WPA-PSK
}
```
7. On the first startup, insert SD card and power on Raspberry Pi Zero W. On first boot, the newly-created wpa_supplicant.conf file and ssh will be moved to appropriate directories. Find the IP address of the Pi via your router.
## Configuration and Setup
1. SSH into the Raspberry Pi (default password: raspberry):
```ssh pi@theipaddress```
2. Change the default password:
``` sudo passwd pi```
3. Download bt_monitor
```git clone https://github.com/bg1000/bt_monitor.git```
4. Change to the monitor directory and run the update and install script
```cd bt_monitor
sudo bash deploy_bt_monitor.sh
```
The install script performs the following tasks:
- performs an update & upgrade (this may take a while on a pi-zero)
- installs the required bluetooth tools
- installs the mosquitto mqtt client - note: vxxx is installed due to this issue.
- installs the required python libraries (see requirements.txt for details)
- opens the configuration file in the nano editor.  This is a yaml file and each line may you need to change is commented.  When you are done editing the file. ``` ctrl-x, y, enter```
- set up bt_monitor to run as a service and to start automatically when the system is booted
5. Once the install script is complete reboot with ```$sudo reboot```
## Testing and Troubleshooting
1. After startup you can verify that bt_monitor is running with ```sudo systemctl status bt_monitor@pi```
2. bt_monitor usese the standard python logging utility.  The default setting is WARNING which will only print messages when something goes wrong.  You can change this setting by editing the config file ```/home/pi/bt_monitor/vinfig.yaml```.  Chaning WARNING to INFO will show more messages and changing it to DEBUG will show the most.
3. To activate changes to the config file there are two options: 
- option 1: Restart the service with ```sudo systemctl restart bt_monitor@pi```.  The messages will show up in /var/log/syslog
- option 2: Atop the service with ```sudo systemctl stop bt_monitor@pi```. Run the application interactively with ```$python3 /home/pi/bt_monitor/main.py```. Message will not print to the console.  When you are done you can restart the serviec e






