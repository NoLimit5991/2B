#!/usr/env python3

from serial import serial_for_url
from random import gauss
from time import sleep

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

class E2bConnection():

	def __init__(self):
		print("init")
		self.conn = serial_for_url('hwgrep://COM3')

	def set(self, cmds, smooth=0):
		print("set")
		for cmd in cmds:
			print(cmd)
			self.conn.write(bytes(cmd + '\r', 'ascii'))
			sleep(max(0.5, smooth/len(cmds)))



if __name__ == "__main__":

	# print("main")

	e2b = E2bConnection()

	# high output, Pulse mode
	e2b.set(['H', 'M0'])

	a, c, d = 0, 0, 0

	while True:

		# print("loop")

		# m = max(12, round(gauss(a, 1)))
		a = min(55, max(45, round(gauss(a, 1))))

		print("a=",a)

		c = min(99, max(2, round(gauss(c, 2))))
		d = min(99, max(2, round(gauss(d, 2))))

		cmds = ['C' + str(c),
			'D' + str(d),
			'B' + str(a)]

		e2b.set(cmds, 12)
