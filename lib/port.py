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
port.py - this module is contains funtions to create port read messages.
"""

from anritsu import error
from anritsu import input_validator

def initialize(unit, module, port):
	"""Creates messages to initialize a port for first use, more specifically: set port to default settings, clear/take ownership, clear/stop counters, clear streams

	:param unit: the unit (generator) number as a string to be selected
	:param module: the module (network card) number as a string to be selected
	:param port: the port number as a string to be selected with ownership taken and its counters and streams cleared

	"""
	init = []
	init.append(':UENTry:ID ' + str(unit) + '\n')
	init.append(':MODule:ID ' + str(module) + '\n')
	init.append(':PORT:ID ' + str(port) + '\n')
	init.append(':PORT:DEFault\n')
	init.append(':PORT:OWNership:CLEar\n')
	init.append(':PORT:OWNership:TAKE\n')
	init.append(':COUNter:CLEar\n')
	init.append(':TSTReam:TABLe:ACLear\n')
	init.append(':COUNter:STOP\n')
	return init

def select(unit, module, port):
	"""Creates messages to select a port

	:param unit: the unit (generator) number as a string to be selected
	:param module: the module (network card) number as a string to be selected
	:param port: the port number as a string to be selected

	"""
	select = []
	select.append(':UENTry:ID ' + str(unit) + '\n')
	select.append(':MODule:ID ' + str(module) + '\n')
	select.append(':PORT:ID ' + str(port) + '\n')
	return select 

def read(counter_name):
	"""Creates messages to read a port its amount of transmitted frames

	:param socket: the socket which controls the analyzer

	"""
	queries = []
	if counter_name == 'txframes':
		queries.append(':COUNter:TRANsmitted:FRAMes?\n')
	elif counter_name == 'rxframes':
		queries.append(':COUNter:RECeived:FRAMes?\n')
	elif counter_name == 'txtestframes':
		queries.append(':COUNter:TRANsmitted:TFRames?\n')
	elif counter_name == 'rxtestframes':
		queries.append(':COUNter:RECeived:TFRames?\n')
	elif counter_name =='BIP':
		# Anritsu MD1230B doesn't support BIP, if the variable is requested anyway, raise an error
		if anritsu_type == 'md1230b':
			raise error.AnritsuSupported(counter_name, anritsu_type)
		else:
			queries.append(':COUNter:SON:ERRor:BIP2?\n')
	elif counter_name == None:
		print('empty counter counter_name')
	else:
		print('unkown counter counter_name')
	return queries

def read_group(counter_group_name, anritsu_type):
	queries = {}
	queries[':COUNter:TRANsmitted:BYTEs?\n'] = str('Transmitted bytes')
	#queries[':COUNter:TRANsmitted:BYTEs:BPS?\n'] = str('Transmitted bytes per second')
	queries[':COUNter:RECeived:BYTEs?\n'] = str('Received bytes')
	#queries[':COUNter:RECeived:BYTEs:BPS?\n'] = str('Received bytes per second')
	queries[':COUNter:TRANsmitted:FRAMes?\n'] = str('Transmitted frames')
	queries[':COUNter:TRANsmitted:FRAMes:FPS?\n'] = str('Transmitted frames per second')
	queries[':COUNter:RECeived:FRAMes?\n'] = str('Received frames')
	queries[':COUNter:RECeived:FRAMes:FPS?\n'] = str('Received frames per second')
	queries[':COUNter:ERRor:FCS?\n'] = str('FCS errors')
	queries[':COUNter:ERRor:OVERsize?\n'] = str('Oversized errors')
	queries[':COUNter:ERRor:OAFerror?\n'] = str('Oversized with FCS errors')
	queries[':COUNter:ERRor:UNDersize?\n'] = str('Undersized errors')
	if counter_group_name == 'test_and_IPV4':
		#queries[':COUNter:TRANsmitted:TFRames?\n'] = str('Transmitted test frame')
		#queries[':COUNter:RECeived:TFRames?\n'] = str('Received test frame')
		queries[':COUNter:ERRor:SEQuence?\n'] = str('Sequence error')
		queries[':COUNter:ERRor:PRBS:BIT?\n'] = str('PRBS bit error count')
		queries[':COUNter:ERRor:PRBS:FRAMes?\n'] = str('PRBS frame error count')
		queries[':COUNter:IP:ERRor:CHECksum?\n'] = str('IPv4 header checksum error')
		queries[':COUNter:IP:RECeived:PACKets?\n'] = str('IPv4 received packets')
		queries[':COUNter:IP:RECeived:PACKets:PPS?\n'] = str('IPv4 received packets per second')
		queries[':COUNter:IP:TRANsmitted:PACKets?\n'] = str('IPv4 transmitted packets')
		queries[':COUNter:IP:TRANsmitted:PACKets:PPS?\n'] = str('IPv4 transmitted packets per second')
	if counter_group_name == 'test':
		queries[':COUNter:TRANsmitted:TFRames?\n'] = str('Transmitted test frame')
		queries[':COUNter:RECeived:TFRames?\n'] = str('Received test frame')
		queries[':COUNter:ERRor:SEQuence?\n'] = str('Sequence error')
		queries[':COUNter:ERRor:PRBS:BIT?\n'] = str('PRBS bit error count')
		queries[':COUNter:ERRor:PRBS:FRAMes?\n'] = str('PRBS frame error count')
	elif counter_group_name == 'ARP':
		# Anritsu MD1260A doesn't support ARP, if the variable is requested anyway, raise an error
		if anritsu_type == 'md1260a':
			raise error.AnritsuSupported(counter_group_name, anritsu_type)
		else:
			queries[':COUNter:ARP:RECeived:AREQuest?\n'] = str('Received ARP request')
			queries[':COUNter:ARP:RECeived:AREPly?\n'] = str('Received ARP reply')
			queries[':COUNter:ARP:TRANsmitted:AREPly?\n'] = str('Transmitted ARP reply')
			queries[':COUNter:ARP:TRANsmitted:AREQuest?\n'] = str('Transmitted ARP reply')
	elif counter_group_name == 'IPV4':
		queries[':COUNter:IP:ERRor:CHECksum?\n'] = str('IPv4 header checksum error')
		queries[':COUNter:IP:RECeived:PACKets?\n'] = str('IPv4 received packets')
		queries[':COUNter:IP:RECeived:PACKets:PPS?\n'] = str('IPv4 received packets per second')
		queries[':COUNter:IP:TRANsmitted:PACKets?\n'] = str('IPv4 transmitted packets')
		queries[':COUNter:IP:TRANsmitted:PACKets:PPS?\n'] = str('IPv4 transmitted packets per second')
	elif counter_group_name == 'IPV6':
		queries[':COUNter:IPV6:RECeived:PACKets?\n'] = str('IPv6 received packets')
		queries[':COUNter:IPV6:RECeived:PACKets:PPS?\n'] = str('IPv6 received packets per second')
		queries[':COUNter:IPV6:TRANsmitted:PACKets?\n'] = str('IPv6 transmitted packets')
		queries[':COUNter:IPV6:TRANsmitted:PACKets:PPS?\n'] = str('IPv6 transmitted packets per second')
	return queries

def transmit(unit_number, module_number, port_number):
	"""Start transmitting on the port.

	:param unit: the unit (generator) number as a string to be selected
	:param module: the module (network card) number as a string to be selected
	:param port: the port number as a string to be selected with ownership taken and its counters and streams cleared

	"""
	messages = []
	messages.append(':UENTry:ID ' + str(unit_number) + '\n')
	messages.append(':MODule:ID ' + str(module_number) + '\n')
	messages.append(':PORT:ID ' + str(port_number) + '\n')
	messages.append(':TSTReam:STARt\n')
	return messages    

def count(unit_number, module_number, port_number):
	"""Creates messages to start counting on a port.

	:param unit: the unit (generator) number as a string to be selected
	:param module: the module (network card) number as a string to be selected
	:param port: the port number as a string to be selected with ownership taken and its counters and streams cleared

	"""
	messages = []
	messages.append(':UENTry:ID ' + str(unit_number) + '\n')
	messages.append(':MODule:ID ' + str(module_number) + '\n')
	messages.append(':PORT:ID ' + str(port_number) + '\n')
	#messages.append(':COUNter:STARt\n')
	messages.append(':COUNter:STARt\n')
	return messages

def capture(unit_number, module_number, port_number):
	"""Creates messages to start counting on a port.

	:param unit: the unit (generator) number as a string to be selected
	:param module: the module (network card) number as a string to be selected
	:param port: the port number as a string to be selected with ownership taken and its counters and streams cleared

	"""
	messages = []
	messages.append(':UENTry:ID ' + str(unit_number) + '\n')
	messages.append(':MODule:ID ' + str(module_number) + '\n')
	messages.append(':PORT:ID ' + str(port_number) + '\n')
	messages.append(':CAPTure:STARt\n')
	return messages

def stop_all(unit_number, module_number, port_number):
	stop = []
	stop.append(':UENTry:ID ' + str(unit_number) + '\n')
	stop.append(':MODule:ID ' + str(module_number) + '\n')
	stop.append(':PORT:ID ' + str(port_number) + '\n')
	stop.append(':CAPTure:STOP\n')
	stop.append(':COUNter:STOP\n')
	stop.append(':TSTReam:STOP\n')
	return stop

def stop_capture(unit_number, module_number, port_number):
	stop = []
	stop.append(':UENTry:ID ' + str(unit_number) + '\n')
	stop.append(':MODule:ID ' + str(module_number) + '\n')
	stop.append(':PORT:ID ' + str(port_number) + '\n')
	stop.append(':CAPTure:STOP\n')
	return stop

def stop_counter(unit_number, module_number, port_number):
	stop = []
	stop.append(':UENTry:ID ' + str(unit_number) + '\n')
	stop.append(':MODule:ID ' + str(module_number) + '\n')
	stop.append(':PORT:ID ' + str(port_number) + '\n')
	stop.append(':COUNter:STOP\n')
	return stop

def stop_stream(unit_number, module_number, port_number):
	stop = []
	stop.append(':UENTry:ID ' + str(unit_number) + '\n')
	stop.append(':MODule:ID ' + str(module_number) + '\n')
	stop.append(':PORT:ID ' + str(port_number) + '\n')
	stop.append(':TSTReam:STOP\n')
	return stop

def transmit_state():
	checkstopped = []
	checkstopped.append(':TSTReam:STATe?\n')
	return checkstopped

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
