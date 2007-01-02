#!/usr/bin/env python
import smbus
import ablib
import time

print "================================================================" 
print "Welcome to MONSOON Seismo ADC and Datalogger"
print "Type ctrl-C to exit"
print "================================================================"
 
I2C_ADDRESS = 0x41
 
bus = smbus.SMBus(0)
 
#Set all ports in input mode
bus.write_byte(I2C_ADDRESS,0xFF)

#Read all the unput lines
value=bus.read_byte(I2C_ADDRESS)
print "%02X" % value


