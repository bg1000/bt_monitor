#!/bin/bash


sudo systemctl stop monitor
sudo systemctl disble monitor
git clone https://github.com/bg1000/bt_monitor.git

cd /home/pi/bt_monitor
pip3 install requirements.txt
scp pi@192.168.2.223:/home/pi/bt_monitor/config.yaml config.yaml
nano config.yaml
sudo bash /home/pi/bt_monitor/autostart_systemd.sh 
