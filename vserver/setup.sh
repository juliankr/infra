#!/bin/sh
set -e
# https://blog.helmutkarger.de/raspberry-pi-vpn-teil-13-ipv4-vpn-mit-trotz-ds-lite/
# socat stands for SOcket CAT. It is a utility for data transfer between two addresses.
apt-get install socat
. ../.env
(crontab -l 2>/dev/null; echo "@reboot socat UDP4-LISTEN:${VPN_PORT},fork,su=nobody UDP6:${VPN_DYNDNS_ADDRESS}:${VPN_PORT}") | crontab -
(crontab -l 2>/dev/null; echo "0     5       *       *       *       /sbin/reboot") | crontab -

