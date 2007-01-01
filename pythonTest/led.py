import ablib
import time
 
print "Blinking led"
print "Type ctrl-C to exit"
 
led = ablib.Pin('PA24', 'OUTPUT')
 
while True:
	time.sleep(0.2)
	led.on()
	time.sleep(0.2)
	led.off()

