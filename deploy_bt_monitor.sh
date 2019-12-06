#!/bin/bash
echo Performing an apt-get update
apt-get update
echo Performing an apt-get upgrade
apt-get upgrade -y
echo installing pi-bluetooth
apt-get install pi-bluetooth
echo installing mosquitto v1.6.4-0
#get repo key
wget http://repo.mosquitto.org/debian/mosquitto-repo.gpg.key
#download appropriate lists file 
cd /etc/apt/sources.list.d/
wget http://repo.mosquitto.org/debian/mosquitto-buster.list
#update caches and install 
apt-cache search mosquitto
sudo apt-get update
sudo apt-get install -f libmosquitto-dev mosquitto mosquitto-clients libmosquitto1 -y
# echo holding mosquitto version at 1.5.7-1
# sudo apt-mark hold libmosquitto-dev mosquitto mosquitto-clients libmosqu
echo installing pip for python 3
apt-get install python3-pip -y
echo installing required python packages
pip3 install -r /home/pi/bt_monitor/requirements.txt
echo setting up bt_monitor to run as a service
cp bt_monitor@pi.service /etc/systemd/system/bt_monitor@pi.service
systemctl --system daemon-reload
systemctl enable bt_monitor@${SUDO_USER:-${USER}}.service

