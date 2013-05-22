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
stream.py - this module is contains the stream class to make messages to create streams.
"""

from anritsu import iptohex
from anritsu import mactohex
from anritsu import input_validator

class Stream:
    """This class represents one stream. These functions create command messages and its related query messages. The commands set a variable on the Anritsu. The queries test the user input with the Anritsu current set variable. 

    :ivar commands: A list is created for the command messages, which set a variable on the Anritsu
    :ivar stream_queries: A dictionary is created with query messages for the stream, as required to test a variable on the Anritsu.
    :ivar frame_queries: A dictionary is created with the query messages for the frame, as required to test a variable on the Anritsu.
    :ivar anritsu_type: the Anritsu type, because not all Anritsu API messages are applicable on all Anritsu devices 

    """
    def __init__(self, stream_identification_number, unit, module, port, anritsu_type):
        """Creates messages to initialize a stream, more specifically: add a stream with a ID.

        :param stream_identification_number: -- the ID as a string number which identifies the objects stream ID on the Anritsu port
        :param unit: the unit (generator) number as a string to be selected
        :param module: the module (network card) number as a string to be selected
        :param port: the port number as a string to be selected
        :param anritsu_type: save the Anritsu type, because not all Anritsu API messages are applicable on all Anritsu devices

        """
        self.commands = []
        self.stream_queries = {}
        self.frame_queries = {}
        self.port_queries = {}
        self.port_commands = []
        self.unit = unit
        self.module = module
        self.port = port
        self.anritsu_type = anritsu_type
        # Append the associated command message to the self.commands list, to set a variable on the Anritsu
        self.commands.append(':TSTReam:TABLe:ADD\n')
        self.commands.append(':TSTReam:TABLe:ID '+ str(stream_identification_number) + '\n')
        # Write the corresponding query message to the self.stream_queries dictionary as a key and the input as it value.
        # Which is required to test a variable on the Anritsu with the users input value.
        self.stream_queries[':TSTReam:TABLe:ID?\n'] = str(stream_identification_number) + '\n'
        # Append commands messages for setting a port on the Anritsu.
        self.port_commands.append(':UENTry:ID ' + str(unit) + '\n')
        self.port_commands.append(':MODule:ID ' + str(module) + '\n')
        self.port_commands.append(':PORT:ID ' + str(port) + '\n')
        # Write a dictionary with the queries messages as the key and the input port as its value.
        self.port_queries[':UENTry:ID?\n'] = str(unit) + '\n'
        self.port_queries[':MODule:ID?\n'] = str(module) + '\n'
        self.port_queries[':PORT:ID?\n'] = str(port) + '\n'
    def distribution(self, stream_distribution_type, jump_to_id=None, count=None):
        """Creates messages to define the type of distribution of the stream.
    
        :param stream_distribution_type: can choose from 'CONT', 'CONT_BURST', 'STOP', 'NEXT', 'JUMP', 'JUMP_COUNT', 'JUMP_STOP'.
        :param jump_to_id: if the distribution type is 'JUMP', 'JUMP_COUNT', 'JUMP_STOP', this parameter represents to what stream ID to JUMP to. Expects to be a number between 1 and 256 (requirement: the stream id must be already set on the Anritsu)
        :param count: if the distribution type is 'JUMP_COUNT', 'JUMP_STOP'. This parameter sets the loop count, which is the amount of jumps, before this stream stops. Expects to be a number between 1 and 256.
    
        """
        # First validate the user input
        input_validator.string_set(['CONT', 'CONT_BURST', 'STOP', 'NEXT', 'JUMP', 'JUMP_COUNT', 'JUMP_STOP'], stream_distribution_type)
        # Append the associated command message to the self.commands list, to set a variable on the Anritsu
        self.commands.append(':TSTReam:TABLe:ITEM:CONTrol:DISTribution ' + str(stream_distribution_type) + '\n')
        # Write the corresponding query message to the self.stream_queries dictionary as a key and the input as it value.
        # Which is required to test a variable on the Anritsu with the users input value.
        self.stream_queries[':TSTReam:TABLe:ITEM:CONTrol:DISTribution?\n'] = str(stream_distribution_type) + '\n'
        # Expect extra parameters when a certain subset of the first argument is set and append the required command and query messages.
        if stream_distribution_type == 'JUMP':
            input_validator.value_minimum_maximum(1, 256, jump_to_id)
            self.commands.append(':TSTReam:TABLe:ITEM:CONTrol:JTID ' + str(jump_to_id) + '\n')
            self.stream_queries[':TSTReam:TABLe:ITEM:CONTrol:JTID?\n'] = str(jump_to_id) + '\n'
        elif stream_distribution_type == 'JUMP_COUNT' or stream_distribution_type == 'JUMP_STOP':
            input_validator.value_minimum_maximum(1, 256, jump_to_id)
            input_validator.value_minimum_maximum(1, 16000000, count)
            self.commands.append(':TSTReam:TABLe:ITEM:CONTrol:JTID ' + str(jump_to_id) + '\n')
            self.commands.append(':TSTReam:TABLe:ITEM:CONTrol:COUNt ' + str(count) + '\n')
            self.stream_queries[':TSTReam:TABLe:ITEM:CONTrol:JTID?\n'] = str(jump_to_id) + '\n'
            self.stream_queries[':TSTReam:TABLe:ITEM:CONTrol:COUNt?\n'] = str(count) + '\n'
    def inter_burst_gap(self, inter_burst_gap_value):
        """Creates messages to define the Inter Burst Gap (IBG).
    
        :param inter_burst_gap_value: the IBG in ns.
    
        """
        # First validate the user input
        input_validator.value_minimum_maximum(1, 1200000000000, inter_burst_gap_value)
        # Append the associated command message to the self.commands list, to set a variable on the Anritsu
        self.commands.append(':TSTReam:TABLe:ITEM:CONTrol:GAP:IBG ' + str(inter_burst_gap_value) + '\n')
        # Write the corresponding query message to the self.stream_queries dictionary as a key and the input as it value.
        # Which is required to test a variable on the Anritsu with the users input value.
        self.stream_queries[':TSTReam:TABLe:ITEM:CONTrol:GAP:IBG?\n'] = str(inter_burst_gap_value) + '\n'
    def inter_stream_gap(self, inter_stream_gap_value):
        """Creates messages to define the Inter Stream Gap (ISG).
    
        :param inter_stream_gap_value: the ISG in ns.
    
        """
        # First validate the user input
        input_validator.value_minimum_maximum(1, 1200000000000, inter_stream_gap_value)
        # Append the associated command message to the self.commands list, to set a variable on the Anritsu
        self.commands.append(':TSTReam:TABLe:ITEM:CONTrol:GAP:ISG ' + str(inter_stream_gap_value) + '\n')
        # Write the corresponding query message to the self.stream_queries dictionary as a key and the input as it value.
        # Which is required to test a variable on the Anritsu with the users input value.
        self.stream_queries[':TSTReam:TABLe:ITEM:CONTrol:GAP:ISG?\n'] = str(inter_stream_gap_value) + '\n'
    def inter_frame_gap(self, inter_frame_gap_type, inter_frame_gap_value, inter_frame_gap_maximum=None):
        """Creates messages to define the Inter Frame Gap (IFG).
    
        :param inter_frame_gap_type: the type of IFG, which can be 'FIXED' or 'RANDOM'. 
        :param inter_frame_gap_value: if the IFG type is 'FIXED', this will be the fixed IFG in nanosecond (ns). If its 'RANDOM', the keyword represents the minimum time in ns.
        :param inter_frame_gap_maximum: if the IFG type is 'RANDOM', this keyword is the maximum time in ns.
    
        """
        # First validate the user input
        input_validator.string_set(['FIXED', 'RANDOM'], inter_frame_gap_type)
        if inter_frame_gap_type == 'FIXED':
            input_validator.value_minimum_maximum(1, 1200000000000, inter_frame_gap_value)
            # Append the associated command message to the self.commands list, to set a variable on the Anritsu
            self.commands.append(':TSTReam:TABLe:ITEM:CONTrol:GAP:IFG:TYPE ' + str(inter_frame_gap_type) + '\n')
            self.commands.append(':TSTReam:TABLe:ITEM:CONTrol:GAP:IFG:VALue ' + str(inter_frame_gap_value) + '\n')
            # Write the corresponding query message to the self.stream_queries dictionary as a key and the input as it value.
            # Which is required to test a variable on the Anritsu with the users input value.
            self.stream_queries[':TSTReam:TABLe:ITEM:CONTrol:GAP:IFG:TYPE?\n'] = str(inter_frame_gap_type) + '\n'
            self.stream_queries[':TSTReam:TABLe:ITEM:CONTrol:GAP:IFG:VALue?\n'] = str(inter_frame_gap_value) + '\n'
        if inter_frame_gap_type == 'RANDOM':
            input_validator.value_minimum_maximum(1, 1200000000000, inter_frame_gap_value)
            input_validator.value_minimum_maximum(1, 1200000000000, inter_frame_gap_maximum)
            # Append the associated command message to the self.commands list, to set a variable on the Anritsu
            self.commands.append(':TSTReam:TABLe:ITEM:CONTrol:GAP:IFG:TYPE ' + str(inter_frame_gap_type) + '\n')
            self.commands.append(':TSTReam:TABLe:ITEM:CONTrol:GAP:IFG:MINimum ' + str(inter_frame_gap_value) + '\n')
            self.commands.append(':TSTReam:TABLe:ITEM:CONTrol:GAP:IFG:MAXimum ' + str(inter_frame_gap_maximum) + '\n')
            # Write the corresponding query message to the self.stream_queries dictionary as a key and the input as it value.
            # Which is required to test a variable on the Anritsu with the users input value.
            self.stream_queries[':TSTReam:TABLe:ITEM:CONTrol:GAP:IFG:TYPE?\n'] = str(inter_frame_gap_type) + '\n'
            self.stream_queries[':TSTReam:TABLe:ITEM:CONTrol:GAP:IFG:VALue?\n'] = str(inter_frame_gap_value) + '\n'
            self.stream_queries[':TSTReam:TABLe:ITEM:CONTrol:GAP:IFG:MAXimum?\n'] = str(inter_frame_gap_maximum) + '\n'
    def burst_per_stream(self, burst_per_stream_amount):
        """Creates messages to define how many burst are needed for this stream.
    
        :param burst_per_stream_amount: amount of burst
    
        """
        # First validate the user input
        input_validator.value_minimum_maximum(1, 1099511627775, burst_per_stream_amount)
        # Append the associated command message to the self.commands list, to set a variable on the Anritsu
        self.commands.append(':TSTReam:TABLe:ITEM:CONTrol:BPSTream ' + str(burst_per_stream_amount) + '\n')
        # Write the corresponding query message to the self.stream_queries dictionary as a key and the input as it value.
        # Which is required to test a variable on the Anritsu with the users input value.
        self.stream_queries[':TSTReam:TABLe:ITEM:CONTrol:BPSTream?\n'] = str(burst_per_stream_amount) + '\n'
    def frames_per_burst(self, frames_per_burst_amount):
        """Creates messages to define how many frames are needed for every burst.
    
        :param frames_per_burst_amount: amount of frames
    
        """
        input_validator.value_minimum_maximum(1, 1099511627775, frames_per_burst_amount)
        self.commands.append(':TSTReam:TABLe:ITEM:CONTrol:FPBurst ' + str(frames_per_burst_amount) + '\n')
        self.stream_queries[':TSTReam:TABLe:ITEM:CONTrol:FPBurst?\n'] = str(frames_per_burst_amount) + '\n'
    def frame_size(self, frame_size_type, frame_size_value=None, frame_size_maximum=None):
        """Creates messages to define what frame size type is needed. 
    
        :param frame_size_type: the type of frame size, which can be 'AUTO', 'FIXED', 'INCREMENT', 'RANDOM'
        :param frame_size_value param: if the frame size type is 'AUTO', this value is ignored. If 'FIXED' it is the frame size. If 'INCREMENT' or 'RANDOM', it is the minimum frame size.
        :param frame_size_maximum: ignored with frame size type 'AUTO' and 'FIXED'. If it is 'INCREMENT' or 'RANDOM' it is the maximum frame size.
    
        """
        input_validator.string_set(['AUTO', 'FIXED', 'INCREMENT', 'RANDOM'], frame_size_type)
        if frame_size_type == 'AUTO':
            self.commands.append(':TSTReam:TABLe:ITEM:FSIZe:TYPE ' + str(frame_size_type) + '\n')
            self.stream_queries[':TSTReam:TABLe:ITEM:FSIZe:TYPE?\n'] = str(frame_size_type) + '\n'
        elif frame_size_type == 'FIXED':
            input_validator.value_minimum_maximum(8, 65280, frame_size_value)
            self.commands.append(':TSTReam:TABLe:ITEM:FSIZe:TYPE ' + str(frame_size_type) + '\n')
            self.commands.append(':TSTReam:TABLe:ITEM:FSIZe:VALue ' + str(frame_size_value) + '\n')
            self.stream_queries[':TSTReam:TABLe:ITEM:FSIZe:TYPE?\n'] = str(frame_size_type) + '\n'
            self.stream_queries[':TSTReam:TABLe:ITEM:FSIZe:VALue?\n'] = str(frame_size_value) + '\n'
        elif frame_size_type == 'INCREMENT':
            input_validator.value_minimum_maximum(8, 65280, frame_size_value)
            self.commands.append(':TSTReam:TABLe:ITEM:FSIZe:TYPE ' + str(frame_size_type) + '\n')
            self.commands.append(':TSTReam:TABLe:ITEM:FSIZe:MINimum ' + str(frame_size_value) + '\n')
            self.commands.append(':TSTReam:TABLe:ITEM:FSIZe:MAXimum ' + str(frame_size_maximum) + '\n')
            self.stream_queries[':TSTReam:TABLe:ITEM:FSIZe:TYPE?\n'] = str(frame_size_type) + '\n'
            self.stream_queries[':TSTReam:TABLe:ITEM:FSIZe:MINimum?\n'] = str(frame_size_value) + '\n'
            self.stream_queries[':TSTReam:TABLe:ITEM:FSIZe:MAXimum?\n'] = str(frame_size_maximum) + '\n'
        elif frame_size_type == 'RANDOM':
            input_validator.value_minimum_maximum(8, 65280, frame_size_value)
            self.commands.append(':TSTReam:TABLe:ITEM:FSIZe:TYPE ' + str(frame_size_type) + '\n')
            self.commands.append(':TSTReam:TABLe:ITEM:FSIZe:MINimum ' + str(frame_size_value) + '\n')
            self.commands.append(':TSTReam:TABLe:ITEM:FSIZe:MAXimum ' + str(frame_size_maximum) + '\n')
            self.stream_queries[':TSTReam:TABLe:ITEM:FSIZe:TYPE?\n'] = str(frame_size_type) + '\n'
            self.stream_queries[':TSTReam:TABLe:ITEM:FSIZe:MINimum?\n'] = str(frame_size_value) + '\n'
            self.stream_queries[':TSTReam:TABLe:ITEM:FSIZe:MAXimum?\n'] = str(frame_size_maximum) + '\n'
    def frame_source_address(self, frame_source_address_hexed, frame_source_mask_hexed_separated='FF-FF-FF-FF-FF-FF', frame_source_address_type='STATIC'):
        """Creates messages to define the frame source MAC address. 
    
        :param frame_source_address_hexed_separated: source MAC address e.g. '00-00-00-00-00-00'
        :param frame_source_mask_hexed_separated: source mask MAC address e.g. '00-00-00-FF-FF-FF'
        :param frame_source_address_type: source address type,  can select out of the following set: 'GATEWAY', 'STATIC', 'INCREMENT', 'DECREMENT', 'RANDOM'
    
        """
        ## First convert and validate the users input MAC address
        #frame_source_address_hexed = mactohex.MactoHex(frame_source_address_hexed_separated,  self.unit, self.module, self.port)
        frame_source_mask_hexed = mactohex.MactoHex(frame_source_mask_hexed_separated,  self.unit, self.module, self.port)
        # Then append the commands and the corresponding queries, to set and test a variable on the Anritsu
        self.commands.append(':TSTReam:TABLe:ITEM:FRAMe:ETHernet:SA:VALue ' + str(frame_source_address_hexed) + '\n')
        self.commands.append(':TSTReam:TABLe:ITEM:FRAMe:ETHernet:SA:MASK ' + str(frame_source_mask_hexed) + '\n')
        self.commands.append(':TSTReam:TABLe:ITEM:FRAMe:ETHernet:SA:TYPE ' + str(frame_source_address_type) + '\n')
        self.frame_queries[':TSTReam:TABLe:ITEM:FRAMe:ETHernet:SA:VALue?\n'] = str(frame_source_address_hexed) + '\n'
        self.frame_queries[':TSTReam:TABLe:ITEM:FRAMe:ETHernet:SA:MASK?\n'] = str(frame_source_mask_hexed) + '\n'
        self.frame_queries[':TSTReam:TABLe:ITEM:FRAMe:ETHernet:SA:TYPE?\n'] = str(frame_source_address_type) + '\n'
    def frame_destination_address(self, frame_destination_address_hexed, frame_destination_mask_hexed_separated='FF-FF-FF-FF-FF-FF', frame_destination_address_type='STATIC'):
        """Creates messages to define the frame destination MAC address. 

        :param frame_destination_address_hexed_separated: destination MAC address e.g. '00-00-00-00-00-00'
        :param frame_destination_mask_hexed_separated: destination mask MAC address e.g. '00-00-00-FF-FF-FF'
        :param frame_destination_address_type: destination address type,  can select out of the following set: 'GATEWAY', 'STATIC', 'INCREMENT', 'DECREMENT', 'RANDOM'

        """
        #frame_destination_address_hexed = mactohex.MactoHex(frame_destination_address_hexed_separated, other_stream.unit, other_stream.module, other_stream.port)
        frame_destination_mask_hexed = mactohex.MactoHex(frame_destination_mask_hexed_separated, self.unit, self.module, self.port)
        self.commands.append(':TSTReam:TABLe:ITEM:FRAMe:ETHernet:DA:VALue ' + str(frame_destination_address_hexed) + '\n')
        self.commands.append(':TSTReam:TABLe:ITEM:FRAMe:ETHernet:DA:MASK ' + str(frame_destination_mask_hexed) + '\n')
        self.commands.append(':TSTReam:TABLe:ITEM:FRAMe:ETHernet:DA:TYPE ' + str(frame_destination_address_type) + '\n')
        self.frame_queries[':TSTReam:TABLe:ITEM:FRAMe:ETHernet:DA:VALue?\n'] = str(frame_destination_address_hexed) + '\n'
        self.frame_queries[':TSTReam:TABLe:ITEM:FRAMe:ETHernet:DA:MASK?\n'] = str(frame_destination_mask_hexed) + '\n'
        self.frame_queries[':TSTReam:TABLe:ITEM:FRAMe:ETHernet:DA:TYPE?\n'] = str(frame_destination_address_type) + '\n'
    def protocol(self, stream_protocol):
        """Creates messages to define the protocol in the stream. 

        :param protocol: the protocol used, can select out of the following set: 'NONE', 'ARP', 'IPV4', 'IGMP', 'IGAP', 'ICMP', 'TCP', 'UDP', 'RIP', 'DHCP', 'IPV6', 'ICMP6', 'TCP_IPV6', 'UDP_IPV6', 'TUNNEL', 'ICMP6_TUNNEL', 'TCP_TUNNEL', 'UDP_TUNNEL', 'TUNNEL6', 'TCP_TUNNEL6', 'UDP_TUNNEL6', 'IPX', 'IS_IS', 'MAC_CONTROL', 'EHTERNET', 'LEX_CONTROL', 'BPUD', 'LACP'.

        """
        input_validator.string_set(['NONE', 'ARP', 'IPV4', 'IGMP', 'IGAP', 'ICMP', 'TCP', 'UDP', 'RIP', 'DHCP', 'IPV6', 'ICMP6', 'TCP_IPV6', 'UDP_IPV6', 'TUNNEL', 'ICMP6_TUNNEL', 'TCP_TUNNEL', 'UDP_TUNNEL', 'TUNNEL6', 'TCP_TUNNEL6', 'UDP_TUNNEL6', 'IPX', 'IS_IS', 'MAC_CONTROL', 'EHTERNET', 'LEX_CONTROL', 'BPUD', 'LACP'], stream_protocol)
        self.commands.append(':TSTReam:TABLe:ITEM:PROTocol:TYPE ' + str(stream_protocol) + '\n')
        self.frame_queries[':TSTReam:TABLe:ITEM:PROTocol:TYPE?\n'] = str(stream_protocol) + '\n'
    def test_frame(self, test_type, length_or_offset=None, flow_id=None):
        """Adds a test frame in the frame its data field

        :param test_type: the type of test used, can select out of the following set: 'PRBS', 'flow'.
        :param length_or_offset: the length in bytes of a PRBS test frame and the offset in bytes of a flow test frame.
        :param flow_id: when a flow test frame is selected, this is the ID.

        """
        input_validator.string_set(['PRBS', 'FLOW'], test_type)
        if test_type == 'PRBS':
            input_validator.value_minimum_maximum(46, 65517, length_or_offset)
            self.commands.append(':TSTReam:TABLe:ITEM:FRAMe:DFIeld1:ENABle 1\n')
            self.commands.append(':TSTReam:TABLe:ITEM:FRAMe:DFIeld1:TYPE TEST_FRAME\n')
            self.commands.append(':TSTReam:TABLe:ITEM:FRAMe:DFIeld1:TFRame:TYPE '  + str(test_type) + '\n')
            self.frame_queries[':TSTReam:TABLe:ITEM:FRAMe:DFIeld1:ENABle?\n'] = '1\n'
            self.frame_queries[':TSTReam:TABLe:ITEM:FRAMe:DFIeld1:ITFRame?\n'] = '1\n'
            self.frame_queries[':TSTReam:TABLe:ITEM:FRAMe:DFIeld1:TYPE?\n'] = 'TEST_FRAME\n'
            self.frame_queries[':TSTReam:TABLe:ITEM:FRAMe:DFIeld1:TFRame:TYPE?\n'] = str(test_type) + '\n'
            if length_or_offset != None:
                self.commands.append(':TSTReam:TABLe:ITEM:FRAMe:DFIeld1:LENGth '  + str(length_or_offset) + '\n')
                self.frame_queries[':TSTReam:TABLe:ITEM:FRAMe:DFIeld1:LENGth?\n'] = str(length_or_offset) + '\n'
        elif test_type == 'FLOW':
            input_validator.value_minimum_maximum(28, 65499, length_or_offset)
            input_validator.value_minimum_maximum(0, 65535, flow_id)
            self.commands.append(':TSTReam:TABLe:ITEM:FRAMe:DFIeld1:ENABle 1\n')
            self.commands.append(':TSTReam:TABLe:ITEM:FRAMe:DFIeld1:TYPE TEST_FRAME\n')
            self.commands.append(':TSTReam:TABLe:ITEM:FRAMe:DFIeld1:TFRame:TYPE FLOW_ID\n')
            self.commands.append(':TSTReam:TABLe:ITEM:FRAMe:DFIeld1:TFRame:FID ' + str(flow_id) + '\n')
            self.frame_queries[':TSTReam:TABLe:ITEM:FRAMe:DFIeld1:ENABle?\n'] = '1\n'
            self.frame_queries[':TSTReam:TABLe:ITEM:FRAMe:DFIeld1:TYPE?\n'] = 'TEST_FRAME\n'
            self.frame_queries[':TSTReam:TABLe:ITEM:FRAMe:DFIeld1:TFRame:TYPE?\n'] = 'FLOW_ID\n'
            self.frame_queries[':TSTReam:TABLe:ITEM:FRAMe:DFIeld1:TFRame:FID?\n'] = str(flow_id) + '\n'
            if length_or_offset != None:
                self.commands.append(':TSTReam:TABLe:ITEM:FRAMe:DFIeld1:OFFSet ' + str(length_or_offset) + '\n')
                self.frame_queries[':TSTReam:TABLe:ITEM:FRAMe:DFIeld1:OFFSet?\n'] = str(length_or_offset) + '\n'
    def ethernet_error(self, error_type):
        """Insert an ethernet error in a stream.

        :param error_type: what type of ethernet error, can select out of the following set: 'FCS', 'UNDERSIZE', 'OVERSIZE', 'OVERSIZE_FCS', 'PRBS_BIT'.

        """
        input_validator.string_set(['FCS', 'UNDERSIZE', 'OVERSIZE', 'OVERSIZE_FCS', 'PRBS_BIT'], error_type)
        self.commands.append(':TSTReam:TABLe:ITEM:ERRor:ETHernet:TYPE ' + str(error_type) + '\n')
        self.frame_queries[':TSTReam:TABLe:ITEM:ERRor:ETHernet:TYPE?\n'] = str(error_type) + '\n'
    def ipv4_error(self, error_type):
        """Insert an IPv4 error in a stream.

        :param error_type: what type of IPv4 error, can select out of the following set: 'CHECKSUM'.

        """
        input_validator.string_set(['CHECKSUM'], error_type)
        self.commands.append(':TSTReam:TABLe:ITEM:ERRor:IP:TYPE ' + str(error_type) + '\n')
        self.frame_queries[':TSTReam:TABLe:ITEM:ERRor:IP:TYPE?\n'] = str(error_type) + '\n'
    def arp(self, arp_type, sender_mac, sender_ip, target_mac, target_ip):
        """Creates messages to set the ARP protocol

        :param arp_type:  set the type of ARP as defined in RFC 826 and RFC 903 can select out of the following set: 'ARP request', 'ARP reply', 'RARP request', 'RARP reply'
        :param sender_mac: set the sender's MAC address. (e.g. 00-DE-BB-00-00-00)
        :param sender_ip: set the sender's IP address. (e.g. 192.168.1.3)
        :param target_mac: set the target's MAC address. (e.g. 00-DE-BB-00-00-00)
        :param target_ip: set the target's IP address. (e.g. 192.168.1.3)

        """
        input_validator.string_set(['ARP request', 'ARP reply', 'RARP request', 'RARP reply'], arp_type)
        self.arp_type_translator = {}
        self.arp_type_translator['ARP request'] = '1'
        self.arp_type_translator['ARP reply'] = '2'
        self.arp_type_translator['RARP request'] = '3'
        self.arp_type_translator['RARP reply'] = '4'
        self.sender_mac_address_hexed = mactohex.MactoHex(sender_mac)
        self.target_mac_address_hexed = mactohex.MactoHex(target_mac)
        self.sender_ip_address = iptohex.IPtoHex(sender_ip)
        self.target_ip_address = iptohex.IPtoHex(target_ip)
        self.sender_ip_address_hexed = self.sender_ip_address[0]
        self.target_ip_address_hexed = self.target_ip_address[0]
        self.commands.append(':TSTReam:TABLe:ITEM:PROTocol:ARP:OPERation ' + str(self.arp_type_translator.get(arp_type)) + '\n')
        self.commands.append(':TSTReam:TABLe:ITEM:PROTocol:ARP:SMADdress ' + str(self.sender_mac_address_hexed) + '\n')
        self.commands.append(':TSTReam:TABLe:ITEM:PROTocol:ARP:SIADdress ' + str(self.sender_ip_address_hexed) + '\n')
        self.commands.append(':TSTReam:TABLe:ITEM:PROTocol:ARP:TIADdress ' + str(self.target_ip_address_hexed) + '\n')
        self.commands.append(':TSTReam:TABLe:ITEM:PROTocol:ARP:TMADdress ' + str(self.target_mac_address_hexed) + '\n')
        self.frame_queries[':TSTReam:TABLe:ITEM:PROTocol:ARP:OPERation?\n'] = str(self.arp_type_translator.get(arp_type) + '\n')
        self.frame_queries[':TSTReam:TABLe:ITEM:PROTocol:ARP:SMADdress?\n'] = str(self.sender_mac_address_hexed) + '\n'
        self.frame_queries[':TSTReam:TABLe:ITEM:PROTocol:ARP:SIADdress?\n'] = str(self.sender_ip_address_hexed) + '\n'
        self.frame_queries[':TSTReam:TABLe:ITEM:PROTocol:ARP:TIADdress?\n'] = str(self.target_ip_address_hexed) + '\n'
        self.frame_queries[':TSTReam:TABLe:ITEM:PROTocol:ARP:TMADdress?\n'] = str(self.target_mac_address_hexed) + '\n'
    def ipv4_source_address(self, ipv4_source_address, ipv4_source_address_type='STATIC'):
        """Creates messages to define the packets source IPv4 address. 

        :param ipv4_source_address: source IPv4 address e.g. '127.0.0.1/24'
        :param ipv4_source_address_type: source address type,  can select out of the following set: 'GATEWAY', 'STATIC', 'INCREMENT', 'DECREMENT', 'RANDOM'

        """
        # First convert and validate the users input IPv4 address
        input_validator.string_set(['GATEWAY', 'STATIC', 'INCREMENT', 'DECREMENT', 'RANDOM'], ipv4_source_address_type)
        ipv4_address_and_mask = iptohex.IPtoHex(ipv4_source_address)
        hexed_ipv4_source_address = ipv4_address_and_mask[0]
        hexed_ipv4_source_mask = ipv4_address_and_mask[1]
        # Then append the commands and the corresponding queries, to set and test a variable on the Anritsu
        self.commands.append(':TSTReam:TABLe:ITEM:PROTocol:IP:SA:TYPE ' + str(ipv4_source_address_type) + '\n')
        self.commands.append(':TSTReam:TABLe:ITEM:PROTocol:IP:SA:VALue ' + str(hexed_ipv4_source_address) + '\n')
        self.commands.append(':TSTReam:TABLe:ITEM:PROTocol:IP:SA:MASK ' + str(hexed_ipv4_source_mask) + '\n')
        self.frame_queries[':TSTReam:TABLe:ITEM:PROTocol:IP:SA:TYPE?\n'] = str(ipv4_source_address_type) + '\n'
        self.frame_queries[':TSTReam:TABLe:ITEM:PROTocol:IP:SA:VALue?\n'] = str(hexed_ipv4_source_address) + '\n'
        self.frame_queries[':TSTReam:TABLe:ITEM:PROTocol:IP:SA:MASK?\n'] = str(hexed_ipv4_source_mask) + '\n'
    def ipv4_destination_address(self, ipv4_destination_address, ipv4_destination_address_type='STATIC'):
        """Creates messages to define the packets destination IPv4 address. 

        :param ipv4_destination_address: destination IPv4 address e.g. '127.0.0.1/24'
        :param ipv4_destination_address_type: destination address type,  can select out of the following set: 'GATEWAY', 'STATIC', 'INCREMENT', 'DECREMENT', 'RANDOM'

        """
        input_validator.string_set(['GATEWAY', 'STATIC', 'INCREMENT', 'DECREMENT', 'RANDOM'], ipv4_destination_address_type)
        ipv4_address_and_mask = iptohex.IPtoHex(ipv4_destination_address)
        hexed_ipv4_destination_address = ipv4_address_and_mask[0]
        hexed_ipv4_destination_mask = ipv4_address_and_mask[1]
        self.commands.append(':TSTReam:TABLe:ITEM:PROTocol:IP:DA:TYPE ' + str(ipv4_destination_address_type) + '\n')
        self.commands.append(':TSTReam:TABLe:ITEM:PROTocol:IP:DA:VALue ' + str(hexed_ipv4_destination_address) + '\n')
        self.commands.append(':TSTReam:TABLe:ITEM:PROTocol:IP:DA:MASK ' + str(hexed_ipv4_destination_mask) + '\n')
        self.frame_queries[':TSTReam:TABLe:ITEM:PROTocol:IP:DA:TYPE?\n'] = str(ipv4_destination_address_type) + '\n'
        self.frame_queries[':TSTReam:TABLe:ITEM:PROTocol:IP:DA:VALue?\n'] = str(hexed_ipv4_destination_address) + '\n'
        self.frame_queries[':TSTReam:TABLe:ITEM:PROTocol:IP:DA:MASK?\n'] = str(hexed_ipv4_destination_mask) + '\n'
    def ipv6_source_address(self, ipv6_source_address, ipv6_source_address_type='STATIC'):
        """Creates messages to define the packets source IPv6 address. 

        :param ipv6_source_address: source IPv6 address e.g. '1:2:3:4:5:6:7:8/64'
        :param ipv6_source_address_type: source address type,  can select out of the following set: 'GATEWAY', 'STATIC', 'INCREMENT', 'DECREMENT', 'RANDOM'

        """
        input_validator.string_set(['GATEWAY', 'STATIC', 'INCREMENT', 'DECREMENT', 'RANDOM'], ipv6_source_address_type)
        # First convert and validate the users input IPv6 address
        ipv6_address_and_mask = iptohex.IPtoHex(ipv6_source_address)
        hexed_ipv6_source_address = ipv6_address_and_mask[0]
        hexed_ipv6_source_mask = ipv6_address_and_mask[1]
        # Then append the commands and the corresponding queries, to set and test a variable on the Anritsu
        self.commands.append(':TSTReam:TABLe:ITEM:PROTocol:IPv6:SA:TYPE ' + str(ipv6_source_address_type) + '\n')
        self.commands.append(':TSTReam:TABLe:ITEM:PROTocol:IPv6:SA:VALue ' + str(hexed_ipv6_source_address) + '\n')
        self.commands.append(':TSTReam:TABLe:ITEM:PROTocol:IPv6:SA:MASK ' + str(hexed_ipv6_source_mask) + '\n')
        self.frame_queries[':TSTReam:TABLe:ITEM:PROTocol:IPv6:SA:TYPE?\n'] = str(ipv6_source_address_type) + '\n'
        self.frame_queries[':TSTReam:TABLe:ITEM:PROTocol:IPv6:SA:VALue?\n'] = str(hexed_ipv6_source_address) + '\n'
        self.frame_queries[':TSTReam:TABLe:ITEM:PROTocol:IPv6:SA:MASK?\n'] = str(hexed_ipv6_source_mask) + '\n'
    def ipv6_destination_address(self, ipv6_destination_address, ipv6_destination_address_type='STATIC'):
        """Creates messages to define the packets destination IPv6 address. 

        :param ipv6_destination_address: destination IPv6 address e.g. '1:2:3:4:5:6:7:8'
        :param ipv6_destination_address_type: destination address type,  can select out of the following set: 'GATEWAY', 'STATIC', 'INCREMENT', 'DECREMENT', 'RANDOM'

        """
        input_validator.string_set(['GATEWAY', 'STATIC', 'INCREMENT', 'DECREMENT', 'RANDOM'], ipv6_destination_address_type)
        ipv6_address_and_mask = iptohex.IPtoHex(ipv6_destination_address)
        hexed_ipv6_destination_address = ipv6_address_and_mask[0] 
        hexed_ipv6_destination_mask = ipv6_address_and_mask[1]
        self.commands.append(':TSTReam:TABLe:ITEM:PROTocol:IPv6:DA:TYPE ' + str(ipv6_destination_address_type) + '\n')
        self.commands.append(':TSTReam:TABLe:ITEM:PROTocol:IPv6:DA:VALue ' + str(hexed_ipv6_destination_address) + '\n')
        self.commands.append(':TSTReam:TABLe:ITEM:PROTocol:IPv6:DA:MASK ' + str(hexed_ipv6_destination_mask) + '\n')
        self.frame_queries[':TSTReam:TABLe:ITEM:PROTocol:IPv6:DA:TYPE?\n'] = str(ipv6_destination_address_type) + '\n'
        self.frame_queries[':TSTReam:TABLe:ITEM:PROTocol:IPv6:DA:VALue?\n'] = str(hexed_ipv6_destination_address) + '\n'
        self.frame_queries[':TSTReam:TABLe:ITEM:PROTocol:IPv6:DA:MASK?\n'] = str(hexed_ipv6_destination_mask) + '\n'

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
