#!/bin/bash
echo Performing an apt-get update
apt-get update
echo Performing an apt-get upgrade
apt-get upgrade -y
echo installing pi-bluetooth
apt-get install pi-bluetooth
echo installing mosquitto v1.6.4-0
# get repo key
wget http://repo.mosquitto.org/debian/mosquitto-repo.gpg.key
#download appropriate lists file 
cd /etc/apt/sources.list.d/
wget http://repo.mosquitto.org/debian/mosquitto-stretch.list
#update caches and install 
apt-cache search mosquitto
sudo apt-get update
sudo apt-get install -f libmosquitto-dev=1.6.4-0 mosquitto=1.6.4-0 mosquitto-clients=1.6.4-0 libmosquitto1=1.6.4-0
echo holding mosquitto version at 1.6.4-0
sudo apt-mark hold libmosquitto-dev mosquitto mosquitto-clients libmosqu
echo installing required python packages
pip3 install -r requirements.txt
echo setting up bt_monitor to run as a service
sudo bash /home/pi/bt_monitor/autostart_systemd.sh 
