#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#	Copyright 2013, AMS-IX
#	Original author: Sean Rijs
#	Current maintainer: Stefan Plug
#	Contact: stefan.plug@ams-ix.net
#
#	This library creates an API for Anritsu nework Generators
#
#!/bin/python

"""
iptohex.py - this module is used to convert an IP to an Anritsu hex format.
"""

from netaddr import *

def IPtoHex(ip_input):
    """Takes an IP address as a string and returns it in a uppercase hexadecimal with a syntax prefix (as required by the Anritsu).

    :param ip_input: a string that represents an IP address (e.g. IPv6: 'fe80::dead:beef/64' or IPv4: '127.0.0.1/24')

    """
    ip = IPNetwork(ip_input)
    ip_return_list = [] 
    ip_address = hex(ip.ip)
    ip_netmask = hex(ip.netmask)
    ip_address = ip_address.replace("0x", "")
    ip_address = [ip_address]
    ip_address.insert(0, '#H')
    ip_address = ''.join(ip_address)
    ip_return_list.append(str.upper(ip_address))
    ip_netmask = ip_netmask.replace("0x", "")
    ip_netmask = [ip_netmask]
    ip_netmask.insert(0, '#H')
    ip_netmask = ''.join(ip_netmask)
    ip_return_list.append(str.upper(ip_netmask))
    return ip_return_list 

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
