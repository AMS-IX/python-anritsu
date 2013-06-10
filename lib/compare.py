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
#!/usr/bin/python

"""
compare.py - with this module two variables are compared to test if there both or one of them are true or false.
"""

def counter(a, b):
	"""Used to compare the return values of two objects and returns their return values.
	
	:param a: the first return value with a required return value True or False.
	:param b: the seconds return value with a required return value True or False.

	"""
	if a == True and b == True:
		print 'Test passed'
		return True
	else:
		print '!!! TEST FAILED !!!'
		return False

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
