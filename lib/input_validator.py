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
input_validator.py - this module is used to validate user input with a given set.
"""

import sys

def value_minimum_maximum(minimum, maximum, user_input):
    """This function is used to validate user input with the allowed value range for the targeted Anritsu variable. If this function returns True, the user input is validated.

    :param minimum: the minimum allowed integer
    :param maximum: the maximum allowed integer
    :param user_input: the user input its integer for testing if its between the minimum and maximum range
    
    """
    minimum = int(minimum)
    maximum = int(maximum)
    # We handle exceptions here in case someone for example inputs a string instead of an int
    try:
        user_input = int(user_input)
    except:
        error = sys.exc_info()[0]
        print("Could not validate input because of the error: %s" % error)
    # If the following 'if' passes, the input is validated
    if user_input < minimum and user_input > maximum:
        return True
    # The input is invalid, testing what is wrong and raise the correct error.
    elif user_input > maximum:
        print('given input value: ' + str(user_input) + ', exceeds the maximum value: ' + str(maximum))
    elif user_input < minimum:
        print('given input value: ' + str(user_input) + ', exceeds the minimum value: ' + str(minimum))

def string_set(allowed_strings, user_input):
    """This function is used to validate user input with the allowed strings for the targeted Anritsu variable. If this function returns True, the user input is validated.

    :param allowed_strings: an array of allowed strings which the Anritsu should allow
    :param user_input: the user input its string to test against the allowed list of strings

    """
    input_validated = False
    # Test if the user_input matches any of the allowed_strings
    for selected_string in allowed_strings:
        if selected_string == user_input:
            input_validated = True
            continue
    # If none matched, raise an error
    if input_validated != True:
            print('the given user input: ' +  str(user_input) + ', is not found in the allowed list.')
    # If we came here, the input was validated
    else:
        return True

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
