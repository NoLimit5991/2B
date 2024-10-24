#!/usr/env python3

import time
import random
import serial
import serial.tools.list_ports as port_list

# 0 = Pulse
# 1 = Bounce
# 2 = Continuous
# 3 = A Split
# 4 = B Split
# 5 = Wave
# 6 = Waterfall
# 7 = Squeeze
# 8 = Milk
# 9 = Throb
# 10 = Thrust
# 11 = Random
# 12 = Step
# 13 = Training
# 14 = Microphone
# 15 = Stereo
# 16 = Tickle
# 17 = Power Level
# 18 = Mic Level
# 19 = A&B Channel Link

# List of favorite programs and their settings
# Program,Name,A,C,D,Rise,Run,Fall,HL
matrix = [
	[0,'Pulse',0,63,18,55,15,60,15,'L'],
	[0,'Pulse',0,62,2,41,30,60,10,'L'],
	[0,'Pulse',0,79,84,55,30,180,15,'L'],
	[0,'Pulse',0,60,98,2,15,20,10,'H'],
	[1,'Bounce',0,62,2,50,15,60,15,'L'],
	[1,'Bounce',0,51,2,50,30,180,10,'H'],
	[2,'Continuous',0,34,24,50,15,40,15,'L'],
	[3,'Asplit',0,33,2,2,30,30,30,'L'],
	[3,'Asplit',0,28,2,2,30,10,30,'H'],
	[5,'Wave',0,58,2,26,60,180,10,'L'],
	[5,'Wave',0,39,30,26,30,180,15,'L'],
	[6,'Waterfall',0,41,34,29,30,180,15,'L'],
	[6,'Waterfall',0,41,75,29,15,180,15,'L'],
	[6,'Waterfall',0,39,15,77,30,180,10,'L'],
	[6,'Waterfall',0,39,2,77,30,720,10,'L'],
	[7,'Squeeze',0,50,33,50,30,180,10,'H'],
	[8,'Milk',0,45,99,89,30,180,10,'H'],
	[8,'Milk',0,51,99,89,30,120,30,'H'],
	[8,'Milk',0,55,99,89,30,60,30,'H'],
	[9,'Throb',0,26,86,50,15,120,15,'L'],
	[9,'Throb',0,31,86,50,5,60,5,'L'],
	[9,'Throb',0,31,10,50,30,180,15,'L'],
	[10,'Thrust',0,28,91,29,30,10,30,'H'],
	[10,'Thrust',0,33,91,50,15,90,15,'L'],
	[12,'Step',0,43,5,50,15,599,15,'L'],
	[13,'Training',0,45,3,2,30,180,10,'L'],
	[13,'Training',0,45,3,100,30,180,10,'L'],
	[13,'Training',0,45,10,2,30,180,10,'L'],
	[13,'Training',0,42,10,100,30,180,10,'L'],
	[13,'Training',0,50,3,50,15,120,15,'L']
]


def send_to_2b(cmd):

	# print("Send: >" + str(cmd) + "<")
	ser.write(bytearray(cmd + "\r", 'ascii'))
	time.sleep(1)



def reset_2b():

	print("Resetting 2B")

	# Power (L or H) - high
	# print("High power")
	send_to_2b("H")

	# Zero out channel a power
	# print("Zero out A")
	send_to_2b("A0")

	# Zero out channel b power
	# print("Zero out B")
	send_to_2b("B0")

	# Zero out channel c (feeling) setting
	# print("Reset C")
	send_to_2b("C50")

	# Zero out channel d (rate) setting
	# print("Reset D")
	send_to_2b("D50")

	print("Done resetting")
	print(" ")



def ramp_do(from_lvl, to_lvl, ramp_secs, incrs):

	print("Ramp from level ", from_lvl, " to ", to_lvl, " in ", incrs, " increments over ", ramp_secs, " seconds")

	# compute step increment value incrs increments
	step_incr = (to_lvl - from_lvl) / incrs
	# print("Step size is ", step_incr)

	# print("Set initial level output to ", from_lvl)
	for i in range (1, incrs):

		new_lvl = int((from_lvl + (step_incr * i)))
		print(i, ": set transitory level output to ", new_lvl)

		send_to_2b("A" + str(new_lvl))
		# send_to_2b("B" + str(max(0,new_lvl-10)))

		# print("sleep for ", (ramp_secs/10), " seconds")
		time.sleep(int(ramp_secs/incrs))

	print("Set final level output to ", to_lvl)
	send_to_2b("A" + str(to_lvl))

	print(" ")



ports = list(port_list.comports())
print("Identified serial ports:")
for p in ports:
	print (p)
print(" ")

# For MacOS, we do this
# try:
# 	ser = serial.Serial('/dev/tty.usbserial-FT99B8BN', timeout = 1)
# except:
#	print("Unable to open /dev/tty.usbserial-FT99B8BN")
#	exit()

# for Windows, we do this
try:
	ser = serial.Serial('COM3', timeout = 1)
except:
	print("Unable to open COM3")
	exit()

ser.close()
ser.open()
ser.flushInput()
ser.flushOutput()

# initialize 2B, set all channel outputs to 0
reset_2b()

# Let the fun begin
for base_lvl in range (55, 70):

	# print("Base level is ", base_lvl)

	# calculate +/- 10% of base_lvl
	delt = random.randint(int(round(base_lvl/-20,0)), int(round(base_lvl/10,0)))
	adj_lvl = base_lvl + delt

	# calculate random run time between 13 and 22 seconds
	dur_sec_run = random.randint(20, 32)

	# calculate random rest time between 20 and 30 seconds
	dur_sec_rest = random.randint(15, 25)

	print(base_lvl, ": final level is ", adj_lvl, " for ", dur_sec_run, " seconds ")


	############################################
	# PULSE
	############################################

	# set HIGH (H)
	print("High")
	send_to_2b("H")

	# set mode (M) - pulse
	print("Pulse")
	send_to_2b("M0")

	# set feeling (C) (1st param)
	print("C channel 2")
	send_to_2b("C02")

	# set rate (D) (2nd param)
	print("D channel 89")
	send_to_2b("D89")

	print (" ")

	# ramp up
	ramp_do(0, adj_lvl, 45, 10)

	# stay on for calcualted duration
	print("Run for ", dur_sec_run, " seconds")
	time.sleep(dur_sec_run)

	# ramp down
	ramp_do(adj_lvl, 0, 10, 5)

	# wait a random number of seconds to rest
	print("Random rest interval of ", dur_sec_rest, " seconds")
	time.sleep(dur_sec_rest)

	print(" ")


	############################################
	# MILK
	############################################

	# set HIGH (H)
	print("High")
	send_to_2b("H")

	# set mode (M) - milk
	print("Milk")
	send_to_2b("M8")

	# set feeling (C) (1st param)
	print("C channel 98")
	send_to_2b("C98")

	# set rate (D) (2nd param)
	print("D channel 89")
	send_to_2b("D89")

	print (" ")

	# ramp up
	ramp_do(0, adj_lvl, 20, 10)

	# stay on for 80 seconds (1 cycle)
	print("Run for 80 seconds")
	time.sleep(80)

	# ramp down
	ramp_do(adj_lvl, 0, 10, 5)

	# wait a random number of seconds to rest
	print("Random rest interval of ", dur_sec_rest, " seconds")
	time.sleep(dur_sec_rest)

	print(" ")


	############################################
	# A SPLIT
	############################################

	# set HIGH (H)
	print("High")
	send_to_2b("H")

	# set mode (M) - A Split
	print("A Split")
	send_to_2b("M3")

	# set feeling (C) (1st param)
	print("C channel 2")
	send_to_2b("C02")

	# set rate (D) (2nd param)
	print("D channel 2")
	send_to_2b("D02")

	print (" ")

	# ramp up to 1/3 of current level value (this is a strong routine)
	ramp_do(0, int(round(adj_lvl/2.5,0)), 20, 10)

	# stay on for calcualted duration
	print("Run for ", dur_sec_run, " seconds")
	print(" ")
	time.sleep(dur_sec_run)

	# ramp down
	ramp_do(int(round(adj_lvl/3,0)), 0, 10, 5)

	# wait a random number of seconds to rest
	print("Random rest interval of ", dur_sec_rest, " seconds")
	time.sleep(dur_sec_rest)

	print(" ")



