#!/bin/bash

# Monitor CPU and memory usage
top -b -d 1 >> /var/log/myapp-top.log

# Analyze network traffic
tcpdump -i eth0 -w /var/log/myapp-traffic.pcap
