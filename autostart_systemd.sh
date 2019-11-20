#!/bin/bash
cp bt_monitor@pi.service /etc/systemd/system/bt_monitor@${SUDO_USER:-${USER}}.service
sed -i "s?/home/pi/bt_monitor?`pwd`?" /etc/systemd/system/bt_monitor@${SUDO_USER:-${USER}}.service
systemctl --system daemon-reload
systemctl enable bt_monitor@${SUDO_USER:-${USER}}.service
systemctl start bt_monitor@pi
