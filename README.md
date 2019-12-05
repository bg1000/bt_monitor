## Description

bt_monitor is a python application that receives scan requests for specific bluetooth devices via MQTT, completes the scans and returns the results via MQTT. This project was inspired by [Andrew Freyer's montor script](https://github.com/andrewjfreyer/monitor) and makes use of the confidence concept introduced there as well as well as some of the Raspberry Pi and home assistant setup instructions. The overall structure and method of deployment of this program was adapted from [GarageQTPi](https://github.com/Jerrkawz/GarageQTPi)

## Hardware

This application is intended to run on a pi-zero W (or a raspberry pi). Dedicating use of the bluetooth interface to this application is recommended.

## Installation Instructions for Raspberry Pi Zero W
### Setup of SD Card
1. Download latest version of raspbian buster lite [here](https://www.raspberrypi.org/downloads/raspbian/)

2. Download etcher from [etcher.io](https://www.balena.io/etcher/)

3. Image raspbian buster to SD card. Instructions [here](https://magpi.raspberrypi.org/articles/pi-sd-etcher).

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
```$ssh pi@theipaddress```
2. Change the default password:
```$sudo passwd pi```
3. Download bt_monitor
```$git clone https://github.com/bg1000/bt_monitor.git```
4. Change to the monitor directory and run the update and install script
```$cd bt_monitor
$sudo bash 2>&1 deploy_bt_monitor.sh | tee /home/pi/bt_monitor/installation.log
```
*Note: This will show the output of the script on the terminal and store it in a file allowing you to do other things while it's running.  Be sure to check the log file for sucessful completion before proceeding.*

The install script performs the following tasks:
- performs an update & upgrade (this may take a while on a pi-zero)
- installs the required bluetooth tools
- installs the mosquitto mqtt client - note: 1.6.4-0 is installed due to [this](https://github.com/andrewjfreyer/monitor/issues/254) issue. apt-mark hold is used to prevent accidental upgrades.
- installs the required python libraries (see requirements.txt for details)
- opens the configuration file in the nano editor.  This is a yaml file and each line you may need to change is commented.  When you are done editing the file. ``` ctrl-x, y, enter```
- sets up bt_monitor to run as a service and to start automatically when the system is booted
5. Once the install script is complete reboot with ```$sudo reboot```
## Testing and Troubleshooting
1. After startup you can verify that bt_monitor is running with ```$sudo systemctl status bt_monitor@pi```
2. To verify that the pi can see your phone via bluetooth and that you have the name and address correct place your phone near the pi with bluetooth turned on.  Run ```$hcitool -i hci0 name "XX:XX:XX:XX:XX:XX"``` with the address of your phone.  If the hcitool can see your phone it will return your phone's name.  This name and address combination is what you need to use when requesting a scan via MQTT.  If the hcitool returns nothing it can not see your phone.
3. bt_monitor uses the standard python logging utility.  The default setting is WARNING which will only print messages when something goes wrong.  You can change this setting by editing the config file ```$nano /home/pi/bt_monitor/config.yaml```.  Changing WARNING to INFO will show more messages and changing it to DEBUG will show the most.
4. To activate changes to the config file there are two options: 
- option 1: Restart the service with ```$sudo systemctl restart bt_monitor@pi```.  The messages will show up in /var/log/syslog
- option 2: Stop the service with ```$sudo systemctl stop bt_monitor@pi```. Run the application interactively with ```$python3 /home/pi/bt_monitor/main.py```. Messages will now print to the terminal.  When you are done you can ```ctrl-c``` and restart the service with ```$sudo systemctl start bt_monitor@pi```
5. Since all communication to and from bt_monitor is via MQTT it is helpful to monitor the appropriate MQTT topics with an MQTT client.  If you are using home assistant the MQTT tab under Developer Tools works well.  Assumming you have kept the base topics the same in config.yaml, under **Listen to Topic** enter  ```bt_monitor/#``` and click *Start Listening*. Under **Publish a Packet** enter ```bt_monitor/scan``` under the topic and add an appropriate payload which will look like the following:
```
{
    "Adapter": "hci0",
    "cmd": "scan",
    "DeviceName": "My_Phone",
    "Address": "XX:XX:XX:XX:XX:XX",
    "ScansForAway": "2"
}
```
Replace **"My_Phone"** and **"XX:XX:XX:XX:XX:XX"** with the values from the hcitool test above (keep the quotes).
After clicking *Publish* You should see your message go out and then a few seconds later a response that looks something like the following:
```
Message 2 received on bt_monitor/garage/My_Phone at 1:50 PM:
{
    "DeviceName": "My_Phone",
    "DeviceAddress": "XX:XX:XX:XX:XX:XX",
    "Confidence": "0.0",
    "Timestamp": "2019-12-04 13:50:32.634536"
}
```
If bt_scan sees your phone confidence will be "100.0".  If bt-scan doesn't see your phone confidence will = previous_confidence - 100.0/ScansForAway.  bt_monitor will keep scanning until a value of 100.0 or 0.0 is reached.  For example: You request a scan and get a value of 100.0. You then turn off bluetooth on your phone and request another scan with ScansForAway="2".  You will get a result of "50.0" and then a result of "0.0". Once a value of either 100.0 or 0.0 is reached no further scans will be completed until another message is sent.  If you want to scan every X minutes you can accomplish this by creating an automation that sends a request every X minutes.

Scan Order: bt_monitor uses a FIFO request queue (size=30 but can be changed in configuration file) and has 2 threads.  One thread responds to scan requests by putting them in the FIFO queue.  The second thread loops every 5 seconds (can be changed in configuration file) and processes any outstanding scan requests (empties the queue before going to sleep).  If the processing thread calculates a confidence greater than 0.0 and less than 100.0 it will enqueue another request for the scanned device in the request queue. If the queue is full a warning message is logged and the request is discarded.

6. Tip: It took me a bit of time to figure out where to place the pi's for best coverage and also what events I wanted to use to trigger scans.  To make testing easier I created an input_boolean that would request a scan for a particular phone and added it to the UI.  I then built an automation that was triggered by the input boolean, requested a scan via MQTT and reset the input_boolean.  This allows you to easily trigger a scan for testing. Other automations you build can also set this input boolean to trigger a scan rather than having multiple automations that send the same json payload. If you later decide you don't want it in the UI you can simply remove it and leave it "behind the scenes".







