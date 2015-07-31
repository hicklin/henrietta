import ablib

print "Pressing button"
print "Type ctrl-C to exit"
 
led = ablib.Pin('PA24', 'out')
button = ablib.Pin('PA25', 'in')
 
while True:
	if button.get_value() == 0:
		led.on()
	else:
		led.off()

