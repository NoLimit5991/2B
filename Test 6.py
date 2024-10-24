#!/usr/env python3

import time
import random
import serial
import serial.tools.list_ports as port_list

# Uses channel A only
# Loops through a set of 20+ favorite mode settings
# After each 5 modes, increases power output by 1

# All of the codes for the 2B unit's different modes
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
# 20 = Microphone level
# 21 = Backlight level
# 22 = Factory reset

# List of favorite programs and their settings
# Program,Name,A,C,D,Rise,Run,Fall,HL
matrix = [
	[0,'Pulse',0,68,18,55,15,60,15,'L'],
	[0,'Pulse',0,62,2,41,30,60,10,'L'],
	[0,'Pulse',0,79,84,55,30,60,15,'L'],
	[0,'Pulse',0,60,98,2,15,20,10,'H'],
	[1,'Bounce',0,68,2,50,15,60,15,'L'],
	[1,'Bounce',0,51,2,50,30,60,10,'H'],
	[2,'Continuous',0,39,24,50,15,40,15,'L'],
	[3,'Asplit',0,33,2,2,30,30,30,'L'],
	[3,'Asplit',0,25,2,2,30,10,30,'H'],
	[5,'Wave',0,52,2,26,60,60,10,'L'],
	[5,'Wave',0,49,30,26,30,60,15,'L'],
	[6,'Waterfall',0,48,34,29,30,60,15,'L'],
	[6,'Waterfall',0,46,75,29,15,60,15,'L'],
	[6,'Waterfall',0,47,15,77,30,60,10,'L'],
	[6,'Waterfall',0,47,2,77,30,60,10,'L'],
	[7,'Squeeze',0,55,33,50,30,60,10,'H'],
	[8,'Milk',0,45,99,89,30,180,10,'H'],
	[8,'Milk',0,51,99,89,30,120,30,'H'],
	[8,'Milk',0,55,99,89,30,60,30,'H'],
	[9,'Throb',0,36,86,50,15,60,15,'L'],
	[9,'Throb',0,41,86,50,5,60,5,'L'],
	[9,'Throb',0,41,10,50,30,60,15,'L'],
	[10,'Thrust',0,28,91,29,30,10,30,'H'],
	[10,'Thrust',0,43,91,50,15,60,15,'L'],
	[12,'Step',0,53,5,50,15,60,15,'L'],
	[13,'Training',0,45,3,2,30,60,10,'L'],
	[13,'Training',0,45,3,100,30,60,10,'L'],
	[13,'Training',0,45,10,2,30,60,10,'L'],
	[13,'Training',0,48,10,100,30,60,10,'L']
]


def send_to_2b(cmd):

	# print("Send: >" + str(cmd) + "<")
	ser.write(bytearray(cmd + "\r", 'ascii'))
	time.sleep(0.4)



def reset_2b():

	print("Resetting 2B")

	# Power (L or H) - high
	# We have to send this command first
	send_to_2b("H")

	# Zero out channel a power
	send_to_2b("M0")

	# Zero out channel a power
	send_to_2b("A0")

	# Zero out channel b power
	send_to_2b("B0")

	# Reset channel c (feeling) setting
	send_to_2b("C50")

	# Reset channel d (rate) setting
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

# Do this fun cycling through our favorite settings
inc_ctr = 1
lvl_inc = 0

while True:

	i = random.randint(0, len(matrix)-1)
	mrow = matrix[i]

	print("Random entry is ", i, " -> ", mrow)
	print("Setting initial values")

	# Each row in matrix has the following structure:
	# prog_no,prog_name,a_lvl,c_lvl,d_lvl,rise_secs,run_secs,fall_secs,pwr_lvl

	# set high/low power level value first
	send_to_2b(mrow[9])

	# Set program mode
	send_to_2b("M" + str(mrow[0]))

	# set channel B to zero
	send_to_2b("B0")

	# set feeling (C)
	send_to_2b("C" + str(mrow[3]))

	# set rate (D)
	send_to_2b("D" + str(mrow[4]))

	# Rise to a_lvl over rise_secs
	ramp_do(0, (mrow[3] + lvl_inc), mrow[6], 10)

	# run for run_secs
	print("Run program for ", mrow[7], " seconds")
	time.sleep(mrow[7])

	# Fall to 0 over fall_secs
	ramp_do(mrow[3] + lvl_inc, 0, mrow[8], 5)

	sleep_sec = random.randint(15, 25)
	print("Rest interval of ", sleep_sec, " seconds")
	time.sleep(sleep_sec)

	# increase output level by 1 after every 5 programs
	inc_ctr = inc_ctr + 1
	if inc_ctr > 5:
		print("*** Will increase channel A output level by +1")
		lvl_inc = lvl_inc + 1
		inc_ctr = 1

	print(" ")

exit()

