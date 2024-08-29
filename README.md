USE AT YOUR OWN RISK.
USE AT YOUR OWN RISK.
USE AT YOUR OWN RISK.

Simple python3 script to control an estim systems 2B estim box via the USB-to-serial connection cable.
Works by connecting to the unit, then by launching into a loop which raises power by +1 each time the loop starts over.  

In each loop it:
   Derives a random +/- 10% delta to add to the power limit for the duration of this loop (could go up or down 10%!)
   Derives a random run and a random rest duration for this loop
   Executes the first setting/program (Pulse)
   Ramps from 0 power level up to the loop's derived max power setting
   Then it runs at that power level for the random period of time (for a little fun)
   Then it ramps back down to 0 (fairly quickly)
   Then it waits for some the random period of rest time to give you a little break (so you can have a little more fun later)
   Then it moves on to the next program (Milk) in the level and does the above again
   Then it moves on to the last program (ASplit) in the level and does the above again
   When all 3 programs have completed, the loop repeats at a new level which increases the power level by 1

The script currently is set to stop at power level 70 (on high power mode) but can easily be adjusted to your needs -- run times, max power, randomizations, rest times, etc.
The script is currently hard-coded with my 3 favorite programs/settings: Pulse, Milk, and ASplit. 
You should be connected to A channel to match what the script is doing.
Milk run-time is hard-coded to 90 seconds since that gets through 1 complete cycle.
ASplit power level is halved because that's a super strong type of stim and that would quickly become torturous, lol.  (But you do you!)
