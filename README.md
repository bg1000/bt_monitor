## What is bt_monitor

bt_monitor receives scan requests for specific bluetooth devices via MQTT, completes the scans and returns the results via MQTT. This project was inspired by [Andrew Freyer's montor script](https://github.com/andrewjfreyer/monitor) and makes use of the confidence concept introduced there as well as well as the Raspberry Pi setup instructions and a similar setup for the mqtt topics and home assistant entities. The overall structure and method of deployment of this program was adapted from [GarageQTPi](https://github.com/Jerrkawz/GarageQTPi)

## Hardware

This application is intended to run on a dedicated pi-zero W (or a raspberry pi).

## Installation Instructions for Raspberry Pi Zero W
### Setup of SD Card
1. Download latest version of raspbian buster lite [here](https://www.raspberrypi.org/downloads/raspbian/)

2. Download etcher from [etcher.io](https://www.balena.io/etcher/)

3. Image raspbian buster to SD card. Instructions [here] (https://magpi.raspberrypi.org/articles/pi-sd-etcher).

4. Mount boot partition of imaged SD card (unplug it and plug it back in)

5. To enable ssh, create blank file, without any extension, in the root directory called ssh

6. To setup Wi-Fi, create wpa_supplicant.conf file in root directory and add Wi-Fi details for home Wi-Fi:

```country=US
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
sudo bash deploy bt_monitor
```





### bt_monitor setup
1. `git clone https://github.com/Jerrkawz/GarageQTPi.git`
2. `pip install -r requirements.txt`
3. edit the configuration.yaml to set up mqtt (See below)
4. `python main.py` 
5. To start the server on boot run `sudo bash autostart_systemd.sh`


## API Reference

The server works with the Home Assisant MQTT Cover component out of the box but if you want to write your own MQTT client you need to adhere to the following API:

Publish one of the following UPPER CASE strings to the command_topic in your config:

`OPEN | CLOSE | STOP`

Subscribe to the state_topic in your config and you will recieve one of these lower case strings when the state pin changes:

`open | closed`

Thats it!

## Sample Configuration

config.yaml:
```
mqtt:
    host: m10.cloudmqtt.com
    port: *
    user: *
    password: *
doors:
    -
        id: 'left'
        relay: 23
        state: 17
        state_topic: "home-assistant/cover/left"
        command_topic: "home-assistant/cover/left/set"
    -
        id: 'right'
        relay: 24
        state: 27
        state_topic: "home-assistant/cover/right"
        command_topic: "home-assistant/cover/right/set"
```

