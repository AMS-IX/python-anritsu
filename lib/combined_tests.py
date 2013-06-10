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
#!/usr/bin/python -Btt

from anritsu import stream, analyzer, convert_calc

def set_port(anritsu_control, port, src, dst, streamid, frames, frame_size, ns_IFG):
	stream = anritsu_control.stream(streamid, port[0], port[1], port[2])
	stream.distribution('NEXT')
	stream.frames_per_burst(str(frames))
	stream.inter_frame_gap('FIXED', str(ns_IFG))
	stream.frame_size('FIXED', frame_size)
	stream.frame_source_address(src)
	stream.frame_destination_address(dst)
	stream.protocol('IPV4')
	stream.ipv4_source_address('127.0.0.1/24', 'STATIC')
	stream.ipv4_destination_address('127.0.0.0/24', 'RANDOM')
	stream.test_frame('PRBS', '46')
	anritsu_control.stream_commit(stream)

def run(anritsu_control, p1, p2, sec, speed, frame_size, Gbps, learn):
	mac_a = convert_calc.MactoHex('00-00', p1[0], p1[1], p1[2])
	mac_b = convert_calc.MactoHex('00-00', p2[0], p2[1], p2[2])
	anritsu_control.port_clear_own(p1[0], p1[1], p1[2])
	anritsu_control.port_clear_own(p2[0], p2[1], p2[2])
	IFG = convert_calc.calculate_inter_frame_gap(speed, 8, frame_size, Gbps)
	frames = convert_calc.calculate_frames(sec, 8, IFG[0], frame_size, Gbps)
	set_port(anritsu_control, p1, mac_a, mac_b, 1, frames, frame_size, IFG[1])
	set_port(anritsu_control, p2, mac_b, mac_a, 1, frames, frame_size, IFG[1])
	anritsu_control.count_transmit(p1[0], p1[1], p1[2], p2[0], p2[1], p2[2])
	anritsu_control.wait_for_transmission(p2[0], p2[1], p2[2], 'STOP') 
	anritsu_control.stop_counter(p1[0], p1[1], p1[2], p2[0], p2[1], p2[2])
	if learn == 0:
		anritsu_control.get_port_counter_group(p1[0], p1[1], p1[2], p2[0], p2[1], p2[2], 'test_and_IPV4')
		result_a = anritsu_control.test_port_counter(p1[0], p1[1], p1[2], 'rxframes', frames, frames)
		result_b = anritsu_control.test_port_counter(p2[0], p2[1], p2[2], 'rxframes', frames, frames)

def run_test(anritsu_control, p1, p2, sec, speed, frame_sizes, Gbps, learn):
	for teller, frame_size in enumerate(frame_sizes):
		if learn == 1:
			print (
				'\n'
				'*************************\n'
				'Test: LEARNING MAC\n'
				'Speed: '+ str(speed) +'%\n'
				'Seconds: '+ str(sec) + '\n'
				'Frame size: '+ str(frame_size) + ' Byte\n'
				'*************************'
				)
			run(anritsu_control, p1, p2, sec, speed, frame_size, Gbps, learn)
		else:
			print (
				'\n'
				'*************************\n'
				'Test: '+ str(teller+1) + '/'+ str(len(frame_sizes)) + '\n'
				'Speed: '+ str(speed) +'%\n'
				'Seconds: '+ str(sec) + '\n'
				'Frame size: '+ str(frame_size) + ' Byte\n'
				'*************************'
				)
			run(anritsu_control, p1, p2, sec, speed, frame_size, Gbps, learn)

def cleanup(anritsu_control):
	anritsu_control.disconnect()

