#!/usr/env python3

import time
import random
import serial
import serial.tools.list_ports as port_list

# Channel codes for estim 2B running firmware 2.106 (current as of 8/29/2024)
#
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

def reset_2b():

	print("Resetting 2B")

	# Zero out channel a power
	print("Zero out A")
	output = bytearray("A0" + "\r", 'ascii')
	ser.write(output)
	time.sleep(1)

	# Zero out channel b power
	print("Zero out B")
	output = bytearray("B0" + "\r", 'ascii')
	ser.write(output)
	time.sleep(1)

	# Power (L or H) - high
	print("High power")
	ser.write(bytearray("H\r", 'ascii'))
	time.sleep(1)

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

		output = bytearray("A" + str(new_lvl) + "\r", 'ascii')
		ser.write(output)
		time.sleep(1)

		# print("sleep for ", (ramp_secs/10), " seconds")
		time.sleep(int(ramp_secs/incrs) - 1)

	print("Set final level output to ", to_lvl)
	print(" ")

	output = bytearray("A" + str(to_lvl) + "\r", 'ascii')
	ser.write(output)
	time.sleep(1)



def run_up(strt, fin):

	print("Running up from level ", strt, " to ", fin)

	for base_lvl in range (strt, fin):

		# print("Base level is ", base_lvl)

		# calculate +/- 10% of lvl
		delt = random.randint(int(round(base_lvl/-10,0)), int(round(base_lvl/10,0)))
		adj_lvl = base_lvl + delt

		# calculate random on time between 13 and 22 seconds
		dur_sec_run = random.randint(13, 22)

		# calculate random rest time between 20 and 30 seconds
		dur_sec_rest = random.randint(20, 30)

		print(base_lvl, ": final level is ", adj_lvl, " for ", dur_sec_run, " seconds ")


		# PULSE
		# PULSE
		# PULSE

		# set mode (M) - pulse
		print("Pulse")
		ser.write(bytearray("M0\r", 'ascii'))
		time.sleep(1)

		# set feeling (C) (1st param)
		print("C channel 2")
		ser.write(bytearray("C2\r", 'ascii'))
		time.sleep(1)

		# set rate (D) (2nd param)
		print("D channel 89")
		ser.write(bytearray("D89\r", 'ascii'))
		time.sleep(1)

		print (" ")

		# ramp up
		ramp_do(0, adj_lvl, 30, 10)

		# stay on for calcualted duration
		print("Run for ", dur_sec_run, " seconds")
		time.sleep(dur_sec_run)

		# ramp down
		ramp_do(adj_lvl, 0, 10, 5)

		# wait a random number of seconds to rest
		print("Random rest interval of ", dur_sec_rest, " seconds")
		time.sleep(dur_sec_rest)

		print(" ")


		# MILK
		# MILK
		# MILK

		# set mode (M) - milk
		print("Milk")
		ser.write(bytearray("M8\r", 'ascii'))
		time.sleep(1)

		# set feeling (C) (1st param)
		print("C channel 98")
		ser.write(bytearray("C98\r", 'ascii'))
		time.sleep(1)

		# set rate (D) (2nd param)
		print("D channel 89")
		ser.write(bytearray("D89\r", 'ascii'))
		time.sleep(1)

		print (" ")

		# ramp up
		ramp_do(0, adj_lvl, 20, 10)

		# stay on for 90 seconds (1 cycle)
		print("Run for 90 seconds")
		time.sleep(90)

		# ramp down
		ramp_do(adj_lvl, 0, 10, 5)

		# wait a random number of seconds to rest
		print("Random rest interval of ", dur_sec_rest, " seconds")
		time.sleep(dur_sec_rest)

		print(" ")


		# A SPLIT
		# A SPLIT
		# A SPLIT

		# set mode (M) - A Split
		print("A Split")
		ser.write(bytearray("M3\r", 'ascii'))
		time.sleep(1)

		# set feeling (C) (1st param)
		print("C channel 2")
		ser.write(bytearray("C2\r", 'ascii'))
		time.sleep(1)

		# set rate (D) (2nd param)
		print("D channel 2")
		ser.write(bytearray("D2\r", 'ascii'))
		time.sleep(1)

		print (" ")

		# ramp up
		ramp_do(0, int(round(adj_lvl/2,0)), 20, 10)

		# stay on for calcualted duration
		print("Run for ", dur_sec_run, " seconds")
		print(" ")
		time.sleep(dur_sec_run)

		# ramp down
		ramp_do(int(round(adj_lvl/2,0)), 0, 10, 5)

		# wait a random number of seconds to rest
		print("Random rest interval of ", dur_sec_rest, " seconds")
		time.sleep(dur_sec_rest)

		print(" ")


ports = list(port_list.comports())
print("Existing serial ports:")
for p in ports:
	print (p)
print(" ")

# For MacOS, we do this
# try:
# 	ser = serial.Serial('/dev/tty.usbserial-FT99B8BN', timeout = 1)
# except:
#	  print("Unable to open /dev/tty.usbserial-FT99B8BN")
#	  exit()

# for Windows, we do this
try:
	ser = serial.Serial('COM3', timeout = 1)
except:
	print("Unable to open COM3")
	exit()

ser.close()
ser.open()

# initialize 2B, set all channel outputs to 0
reset_2b()

run_up(40, 70)

exit()

