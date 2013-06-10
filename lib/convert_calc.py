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
convert_calc.py - this module is used to convert an IP to an Anritsu hex format, and varius other calculations.
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

def MactoHex(dec_mac, unit=None, module=None, port=None):
	"""Takes a MAC address as a string and returns it in uppercase a hexadecimal form with a prefix (as required by the Anritsu). When only the last 2 octects of a MAC address is given, the unit, module and port number is used as the prefix. This should only be used for the source address.

	:param dec_mac: a string that represents a MAC address (e.g. '00-00-00-FF-FF-FF' or 'FF-FF')
	:param unit: the unit (generator) number as a string to be selected
	:param module: the module (network card) number as a string to be selected
	:param port: the port number as a string to be selected

	"""
	dec_octets = str.split(dec_mac, '-')
	hex_octets = []
	
	if len(dec_octets) == 2:
		for dec_octet in dec_octets:
			if int(dec_octet, base=16) < int(16):
				hex_octets.append('0' + hex(int(dec_octet, base=16))[2:])
			else:
				hex_octets.append(hex(int(dec_octet, base=16))[2:])
		hex_octets.insert(0, port)
		hex_octets.insert(0, '0')
		hex_octets.insert(0, module)
		hex_octets.insert(0, '0')
		hex_octets.insert(0, unit)
		hex_octets.insert(0, '0')
		hex_octets.insert(0, '00')
		hex_octets.insert(0, '#H')
		hex_mac = ''.join(hex_octets)
		return str.upper(hex_mac)
	elif len(dec_octets) == 6:
		for dec_octet in dec_octets:
			if int(dec_octet, base=16) < int(16):
				hex_octets.append('0' + hex(int(dec_octet, base=16))[2:])
			else:
				hex_octets.append(hex(int(dec_octet, base=16))[2:])
		hex_octets.insert(0, '#H')
		hex_mac = ''.join(hex_octets)
		return str.upper(hex_mac)
	else:
		raise ValueError('Not a valid MAC address, it must be 2 or 6 octets')

def calculate_inter_frame_gap(speed, preamble, frame_size, Gbps):
	bpns = Gbps / 10
	procent = 100.0 / speed
	B_frame = frame_size + preamble + 12
	total_frame = B_frame * procent
	total_frame = int(total_frame)
	B_IFG = (total_frame - frame_size) - preamble
	b_IFG = B_IFG * 8
	nsIFG = b_IFG / bpns
	IFG = [B_IFG, int(nsIFG)]
	return IFG

def calculate_frames(sec, preamble, B_IFG, frame_size, Gbps):
	bps = Gbps * 1000000000.0
	Bps = bps / 8
	B_per_frame = frame_size + preamble + B_IFG
	frames_per_sec = Bps / B_per_frame
	frames = frames_per_sec * sec
	return int(frames)
