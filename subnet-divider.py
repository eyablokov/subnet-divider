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
import math
import sys
import ipaddress


def power_log(x):
    """ Get smallest power of 2 greater than (or equal to) a given x. """
    return 2**(math.ceil(math.log(x, 2)))

def isqrt(n):
    """ Newton's method for calculating square roots. """
    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x


# Get the main network, to divide onto predefined parts
pair = ipaddress.ip_network(sys.argv[1], strict=False)

# Get the require number of subnets to which the network will be divided
parts = sys.argv[2]

# Extracting netmask of the main network in CIDR
prefix = pair.prefixlen

# Awareness of subnets' prefix, to divide main network onto
subnet_diff = isqrt(power_log(float(parts)))

# Get subnets of the main network, as a list
subnets = list(pair.subnets(prefixlen_diff=subnet_diff))

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
