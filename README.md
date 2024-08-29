USE AT YOUR OWN RISK.
USE AT YOUR OWN RISK.
USE AT YOUR OWN RISK.

Simple python3 script to control an estim systems 2B estim box via the USB-to-serial connection cable.
Works by connecting to the unit, then by launching into a loop, each time executing 3 different stim settings which ramp up
from 0 to a determined base amount +/- 10% power (random) for some random amount of run time followed by a random amount of rest time.
Each new loop increases the power level by 1 (plus or minus the random amount to be added in).
The script stops at power level 70 (on high power mode) but can easily be adjusted to your needs -- durations, max power, rest times, etc.
The script is currently hard-coded with my 3 favorite settings, Pulse, Milk, and ASplit. 
You should be connected to A channel to match what the script is doing.
Milk run-time is hard-coded to 90 seconds since that gets through 1 complete cycle.
ASplit power level is halved because that's a super strong type of stim and that would quickly become torturous, lol.
