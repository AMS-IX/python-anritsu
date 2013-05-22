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
error.py - the error module contains classes to raise python-anritsu specific errors. 
"""

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class AnritsuCommandError(Error):
    """Exception raised when an expected variable value is not set on a Anritsu after a commit.

    :ivar command: The message which contains the variable
    :ivar sent_value: The value we have sent and expected to be set on the Anritsu
    :ivar anritsu_value: The variable value the Anritsu returns it has set.
    """

    def __init__(self, command, sent_value, anritsu_value):
        self.command = command
        self.sent_value = sent_value
        self.anritsu_value = anritsu_value
    def __str__(self):
        return repr('The command message \"' + self.command + '\" with variable \"' + self.sent_value + '\" was sent, but the Anritsu has set \"' + self.anritsu_value  + '\".')

class AnritsuQueryError(Error):
    """Exception raised when an expected variable value is not set on a Anritsu after a commit.

    :ivar query: The message which contains the variable
    :ivar sent_value: The value we have sent and expected to be set on the Anritsu
    :ivar anritsu_value: The variable value the Anritsu returns it has set.
    """

    def __init__(self, query, sent_value, anritsu_value):
        self.query = query
        self.sent_value = sent_value
        self.anritsu_value = anritsu_value
    def __str__(self):
        return repr('The query message \"' + self.query + '\" was sent, our input for the related command message was \"' + self.sent_value + '\" , but the Anritsu has set \"' + self.anritsu_value  + '\".')

class AnritsuSupported(Error):
    """Exception raised when a requested feature is not supported.

    :ivar command: The message which contains the variable
    :ivar sent_value: The value we have sent and expected to be set on the Anritsu
    :ivar anritsu_value: The variable value the Anritsu returns it has set.
    """

    def __init__(self, command, anritsu_type):
        self.command = command
        self.anritsu_type = anritsu_type
    def __str__(self):
        return repr('The command message \"' + self.command + '\" is not support for Anritsu type \"' + self.anritsu_type  + '\".')

class AnritsuTimeout(Error):
    """Exception raised when an expected variable value is not set on a Anritsu after a commit.

    :ivar command: The message sent before a timeout occurred
    """

    def __init__(self, command):
        self.command = command
    def __str__(self):
        return repr('The query message \"' + self.command + '\" was sent, followed by a timeout, meaning an invalid query or command message was sent or our connect was lost.')

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
