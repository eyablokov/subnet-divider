#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Show subnets information.

This script gets IP network and network mask pair in CIDR notation, divides
them to a predefined number of parts and shows Network Address, Netmask,
Broadcast, Gateway, Host Range and Host Count information.

Example:
    $ ./subnet-divider.py 200.100.33.65/26 3
"""

from __future__ import print_function
import sys
import ipaddress

# Get the number of parts to which the network will be divided
parts = sys.argv[2]

# Get the main network, to divide onto predefined parts
pair = ipaddress.ip_network(sys.argv[1], strict=False)

# Get subnets of the main network, as a list
subnets = list(pair.subnets())

for subnet in subnets:
    sub = str(subnet)

    # Get address string and CIDR string from command line
    (addr_string, cidr_string) = sub.split('/')

    # Split address into octets and turn CIDR into int
    addr = addr_string.split('.')
    cidr = int(cidr_string)

    # Initialize the netmask and calculate based on CIDR mask
    mask = [0, 0, 0, 0]
    for i in range(cidr):
        mask[i//8] = mask[i//8] + (1 << (7 - i % 8))

    # Initialize net and binary and netmask with addr to get network
    net = []
    for i in range(4):
        net.append(int(addr[i]) & mask[i])

    # Duplicate net into broad array, gather host bits, and generate broadcast
    broad = list(net)
    brange = 32 - cidr
    for i in range(brange):
        broad[3-i//8] = broad[3-i//8] + (1 << (i % 8))

    # Locate usable IPs
    hosts = {"first":list(net), "last":list(broad)}
    hosts["first"][3] += 1
    hosts["last"][3] -= 1

    # Locate network gateway
    gateway = hosts["first"]

    # Count the difference between first and last host IPs
    hosts["count"] = 0
    for i in range(4):
        hosts["count"] += (hosts["last"][i] - hosts["first"][i]) * 2**(8*(3-i))

    # Print information, mapping integer lists to strings for easy printing
    print(("CIDR:       "), str(addr_string) + "/" + str(cidr))
    print(("Netmask:    "), ".".join(map(str, mask)))
    print(("Network:    "), ".".join(map(str, net)))
    print(("Gateway:    "), ".".join(map(str, gateway)))
    print(("Broadcast:  "), ".".join(map(str, broad)))
    print(("Host Range: "), ".".join(map(str, hosts["first"])), "-", ".".join(map(str, hosts["last"])))
    print(("Host Count: "), hosts["count"])
