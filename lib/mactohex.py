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
mactohex.py - this module is used to convert a MAC address to an Anritsu hex format.
"""

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

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
