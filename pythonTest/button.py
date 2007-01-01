import ablib

print "Pressing button"
print "Type ctrl-C to exit"
 
led = ablib.Pin('PA24', 'OUTPUT')
button = ablib.Pin('PA25', 'INPUT')
 
while True:
	if button.get_value() == 0:
		led.on()
	else:
		led.off()

