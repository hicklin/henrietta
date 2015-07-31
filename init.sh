#!/usr/bin/env bash
# Run as root so that arietta can connect to the small black box with a tiny red led...THE INTERNET
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
echo 1 > /proc/sys/net/ipv4/ip_forward