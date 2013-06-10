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
analyzer.py - this module contains the Analyzer class to control an Anritsu generator.
"""

from anritsu import port
from anritsu import stream
from anritsu import error
from anritsu import input_validator
from time import sleep
from sys import stdout
import socket
import texttable

class Analyzer:
	"""Control the analyzer via a TCP socket on port 5001 which subsequently controls the generator.

	"""
	def __init__(self, address, anritsu_type):
		"""Connect to a given analyzer on port 5001, save the given expected Anritsu type. Additionally it waits and cleans old query replies from the Anritsu. This process follows these steps: we start by expecting a reply within 5 seconds. If no reply is received, we assume old queries replies are cleaned. This cleaning process is repeated two times, just to be sure.
	
		:param address: host name or IP address
	
		"""
		self.socket = socket.create_connection((address, 5001))
		self.anritsu_type = str.lower(anritsu_type)
		input_validator.string_set(['md1230b', 'md1260a'], anritsu_type)
		# Cleaning old query replies 
		self.try_count = 2
		while self.try_count != 0:
			try:
				self.socket.settimeout(5)
				self.socket.recv(1024)
			except socket.timeout:
				self.try_count = self.try_count - 1
			else:
				self.try_count = self.try_count - 1
				print('Received old message, retrying ')
		# Setting socket timeout back to 20 seconds
		self.socket.settimeout(20)
	def port_clear_own(self, unit, module, port_number):
		"""Clear the counters and take ownership on the given port.

		:param unit: the unit (generator) number as a string to be selected
		:param module: the module (network card) number as a string to be selected
		:param port_number: the port number as a string to be selected with ownership taken and its counters and streams cleared

		"""
		self.messages = port.initialize(unit, module, port_number)
		self.send_msg(self.messages)
	def stream(self, stream_identification_number, unit, module, port_number):
		"""Create via the stream module a stream and pass the anritsu type to the stream, because the API is different between different Anritsu device types

		:param stream_identification_number: set the stream id, must be unique per port
		:param unit: the unit (generator) number as a string to be selected
		:param module: the module (network card) number as a string to be selected
		:param port_number: the port number as a string to be selected

		"""
		try:
			self.new_stream = stream.Stream(stream_identification_number, unit, module, port_number, self.anritsu_type)
			return self.new_stream
		except:
			self.disconnect()
			raise
	def stream_commit(self, stream_object):
		"""Commit the set stream variables on the Anritsu.
		
		:param stream_object: a stream object

		"""
		self.send_msg(stream_object.port_commands)
		for message, expected_string in stream_object.port_queries.iteritems():
			self.socket.send(message)
			try:
				data = self.socket.recv(1024)
			except socket.timeout:
				raise error.AnritsuTimeout(message)
			if data != expected_string:
				raise error.AnritsuCommandError(message, expected_string, data)
		stream_object.commands.append(':TSTReam:TABLe:WRITe\n')
		self.send_msg(stream_object.commands)
		#First test with queries the variables of the 'stream setting'
		for message, expected_string in stream_object.stream_queries.iteritems():
			self.socket.send(message)
			try:
				data = self.socket.recv(1024)
			except socket.timeout:
				raise error.AnritsuTimeout(message)
			if data != expected_string:
				raise error.AnritsuQueryError(message, expected_string, data)
		#Then tests with queries the variables of the 'frame settings'.
		#This seperation of queries was required, as frame settings can't
		#be tested if the stream setting is untested.
		for message, expected_string in stream_object.frame_queries.iteritems():
			self.socket.send(message)
			try:
				data = self.socket.recv(1024)
			except socket.timeout:
				raise error.AnritsuTimeout(message)
			if data != expected_string:
				raise error.AnritsuQueryError(message, expected_string, data)
	def get_port_counter(self, unit, module, port_number, counter_name):
		"""Get a port counter value
		
		:param unit: the unit (generator) number as a string to be selected
		:param module: the module (network card) number as a string to be selected
		:param port_number: the port number as a string to be selected
		:param counter_name: the counter that needs to be checked

		"""
		self.select = port.select(unit, module, port_number)
		self.send_msg(self.select)
		self.counter = port.read(counter_name)
		data = self.send_recv_msg(self.counter)
		datasplit = str.split(data, ',')
		counter_value = datasplit[1]
		print('requested counter field = ' + counter_value)
		return int(counter_value)
	def test_port_counter(self, unit, module, port_number, counter_name, val1, val2):
		"""Get the port counter values and test if its between the expected range
		
		:param unit: the unit (generator) number as a string to be selected
		:param module: the module (network card) number as a string to be selected
		:param port_number: the port number as a string to be selected
		:param counter_name: the counter that needs to be checked
		:param val1: the value where the range starts
		:param val2: the value where the range ends

		"""
		self.select = port.select(unit, module, port_number)
		self.send_msg(self.select)
		self.counter = port.read(counter_name)
		data = self.send_recv_msg(self.counter)
		datasplit = str.split(data, ',')
		counter_value = datasplit[1]
		if int(counter_value) < val1 or int(counter_value) > val2:
			print('out of range, result = ' + counter_value)
			return False
		else:
			#print('in range, requested counter field = ' + counter_value)
			return True
	def get_port_counter_group(self, unit1, module1, port_number1, unit2, module2, port_number2, counter_group=None):
		"""Get a group of counter values 
		
		:param unit: the unit (generator) number as a string to be selected
		:param module: the module (network card) number as a string to be selected
		:param port_number: the port number as a string to be selected
		:param counter_group: the name of the group of counters

		"""
		description = []
		counter_value1 = []
		counter_value2 = []

		self.select1 = port.select(unit1, module1, port_number1)
		self.send_msg(self.select1)
		try:
			self.messages1 = port.read_group(counter_group, self.anritsu_type)
		except:
			self.disconnect()
			raise
		for message, desc in sorted(self.messages1.iteritems()):
			self.socket.send(message)
			try:
				data = self.socket.recv(1024)
			except socket.timeout:
				raise error.AnritsuTimeout(message)
			datasplit = str.split(data, ',')
			description.append(desc)
			counter_value1.append(datasplit[1])

		self.select2 = port.select(unit2, module2, port_number2)
		self.send_msg(self.select2)
		try:
			self.messages2 = port.read_group(counter_group, self.anritsu_type)
		except:
			self.disconnect()
			raise
		for message, desc in sorted(self.messages2.iteritems()):
			self.socket.send(message)
			try:
				data = self.socket.recv(1024)
			except socket.timeout:
				raise error.AnritsuTimeout(message)
			datasplit = str.split(data, ',')
			counter_value2.append(datasplit[1])

		self.table = texttable.Texttable()
		self.table.set_cols_dtype(['i', 'i', 'i'])
		self.table.header(['Counter', 'Int '+ unit1 +'/'+ module1 +'/'+ port_number1, 'Int '+ unit2 +'/'+ module2 +'/'+ port_number2])
		for teller, i in enumerate(description):
			self.table.add_row([description[teller], counter_value1[teller], counter_value2[teller]])
		self.table.add_row(['Counter', 'Int '+ unit1 +'/'+ module1 +'/'+ port_number1, 'Int '+ unit2 +'/'+ module2 +'/'+ port_number2])
		print(self.table.draw())
	def send_recv_msg(self, messages):
		"""To deduce repetitive code of sending a message and waiting for a reply(socket is of blocking type).
		
		:param messages: the list of query messages

		"""
		for message in messages:
			try:
				self.socket.send(message)
				data = self.socket.recv(1024)
			except socket.timeout:
				raise error.AnritsuTimeout(message)
		return data 
	def send_msg(self, messages):
		"""To deduce repetitive code of sending a message.
		
		:param messages: the list of command messages

		"""
		for message in messages:
			self.socket.send(message)
	def count(self, unit1, module1, port_number1, unit2, module2, port_number2):
		"""Start counting on the port.

		:param selection: a list of messages to select a port

		"""
		self.messages = port.count(unit1, module1, port_number1, unit2, module2, port_number2)
		self.send_msg(self.messages)
	def transmit(self, unit1, module1, port_number1, unit2, module2, port_number2):
		"""Start transmitting on a port.

		:param unit: the unit (generator) number as a string to be selected
		:param module: the module (network card) number as a string to be selected
		:param port_number: the port number as a string to be selected

		"""
		self.messages = port.transmit(unit1, module1, port_number1, unit2, module2, port_number2)
		self.send_msg(self.messages)
	def count_transmit(self, unit1, module1, port_number1, unit2, module2, port_number2):
		"""Deducing two functions(count() and transmit()) as one function.

		:param unit: the unit (generator) number as a string to be selected
		:param module: the module (network card) number as a string to be selected
		:param port_number: the port number as a string to be selected

		"""
		self.message = port.count(unit1, module1, port_number1)
		self.message = self.message + port.count(unit2, module2, port_number2)
		self.message = self.message + port.transmit(unit1, module1, port_number1)
		self.message = self.message + port.transmit(unit2, module2, port_number2)
		self.socket.send(''.join(self.message))
	def capture(self, unit, module, port_number):
		"""Start capturing on the port.

		:param unit: the unit (generator) number as a string to be selected
		:param module: the module (network card) number as a string to be selected
		:param port_number: the port number as a string to be selected

		"""
		self.messages = port.capture(unit, module, port_number)
		self.send_msg(self.messages)
	def stop_all(self, unit, module, port_number, when=None, time=None):
		"""Stop all running actions(i.e. counting, transmitting and capturing) on a port.
		
		:param unit: the unit (generator) number as a string to be selected
		:param module: the module (network card) number as a string to be selected
		:param port_number: the port number as a string to be selected
		:param when: Choose between CONT or STOP. 'CONT' means a continuous stream, a time must be given to the time parameter. 'STOP' means wait for the stream to end, then stop all remaining actions.
		:param time: how many seconds to wait for the continuous stream before ending it

		"""
		self.stop = port.stop_all(unit, module, port_number)
		self.checkstopped = port.transmit_state()
		if when == 'CONT':
			if time == None:
				raise ValueError('no time given') 
			else:
				sleep(int(time))
				send_msg(stop)
		elif when == 'STOP':
			self.stopped = False
			print('waiting for transmission to end on port' + port_number)
			while self.stopped == False:
				self.data = self.send_recv_msg(self.checkstopped)
				if self.data == '0\n':
					print('stopped counters on port ' + port_number)
					self.stopped = True
				elif self.data == '1\n':
					sleep(1)
				elif self.data == '2\n':
					print('starting/halting ' + port_number)
					sleep(1)
			self.send_msg(self.stop)
		elif when == None:
			print('when == None')
		else:
			print(when)
	def wait_for_transmission(self, unit, module, port_number, when=None, time=None):
		"""Wait until a 'Stop'stream is done, or terminate a 'CONT'stream after x seconds on a port.
		
		:param unit: the unit (generator) number as a string to be selected
		:param module: the module (network card) number as a string to be selected
		:param port_number: the port number as a string to be selected
		:param when: Choose between CONT or STOP. 'CONT' means a continuous stream, a time must be given to the time parameter. 'STOP' means wait for the stream to end, then stop all remaining actions.
		:param time: how many seconds to wait for the continuous stream before ending it

		"""
		self.checkstopped = port.transmit_state()
		if when == 'CONT':
			self.stop = port.stop_all(unit, module, port_number)
			if time == None:
				raise ValueError('no time given') 
			else:
				sleep(int(time))
				self.send_msg(self.stop)
		elif when == 'STOP' or when == None:
			#print('waiting for transmission to end on port' + port_number)
			while 1:
				self.data = self.send_recv_msg(self.checkstopped)
				stdout.write('.')
				stdout.flush()
				if self.data == '0\n':
					print '.'
					break
				elif self.data == '1\n':
					sleep(1)
				elif self.data == '2\n':
					print('starting/halting ' + port_number)
					sleep(1)
	def stop_capture(self, unit, module, port_number):
		"""Stop capture on a port.
		
		:param unit: the unit (generator) number as a string to be selected
		:param module: the module (network card) number as a string to be selected
		:param port_number: the port number as a string to be selected

		"""
		self.stop = port.stop_capture(unit, module, port_number)
		self.send_msg(self.stop)
	def stop_counter(self, unit1, module1, port_number1, unit2, module2, port_number2):
		"""Stop count on a port.
		
		:param unit: the unit (generator) number as a string to be selected
		:param module: the module (network card) number as a string to be selected
		:param port_number: the port number as a string to be selected

		"""
		self.message = port.stop_counter(unit1, module1, port_number1)
		self.message = self.message + port.stop_counter(unit2, module2, port_number2)
		self.socket.send(''.join(self.message))
	def stop_stream(self, unit, module, port_number):
		"""Stop stream on a port.
		
		:param unit: the unit (generator) number as a string to be selected
		:param module: the module (network card) number as a string to be selected
		:param port_number: the port number as a string to be selected

		"""
		self.stop = port.stop_stream(unit, module, port_number)
		self.send_msg(self.stop)
	def disconnect(self):
		"""Disconnects the socket, consequently ending the test."""
		try:
			self.socket.close()
		finally:
			return None

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
