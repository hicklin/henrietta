#!/usr/bin/python
from . import max11040klib
import datetime
from ablib import Pin
from threading import Thread

BUFFER_SIZE = 1000

m = max11040klib.MaxSpiDev(0)
m.set_registers("config.ini")

file_data_name = datetime.datetime.now().strftime("%Y%j-%H%M%S.dat")

fd = open(file_data_name, "w")

def read_adc():
    global s
    global BUFFER_SIZE
    global adc
    print(m.read_adc_data())
    adc[s] = m.read_adc_data()
    print(adc[s])
    if s == BUFFER_SIZE:
        fd.write("\n".join(adc))
        fd.close
        s = 0
    else:
        s =+ 1
DRDYOUT = Pin('PC0', 'INPUT')
#DRDYOUT.set_edge("both", read_adc)


def write_file(f, buff, t):
    print(t)
    print("Writing file")
    f.write("\n".join(str(x) for x in buff))
    t = 0
    buff = None
    return buff, t


t1 = 0
t2 = BUFFER_SIZE
buffer1 = []
buffer2 = []

run_time = datetime.timedelta(seconds=60)
until_time = datetime.datetime.now() + run_time

print("Sampling from " + datetime.datetime.now().strftime("%H:%M:%S.%f") + " to " + until_time.strftime("%H:%M:%S.%f"))
while datetime.datetime.now() < until_time:
    io = DRDYOUT.digitalRead()
    if io == 0:
        print(t1, t2)

        # Storing in buffer 1
        if t1 < BUFFER_SIZE and t2 == BUFFER_SIZE:
            buffer1.append(m.read_adc_data())
            t1 += 1
        elif t1 == BUFFER_SIZE and t2 == BUFFER_SIZE:
            buffer1.append(m.read_adc_data())
            print("Buffer 1 full... saving in file")
            print("t1a: " + str(t1))
            # Creating independent thread to save buffer in file
            thread_save = Thread(target=write_file, args=(fd, buffer1, t1))
            thread_save.start()
            print("t1b: " + str(t1))

        # Storing in buffer 2
        elif t2 < BUFFER_SIZE and t1 == BUFFER_SIZE:
            buffer2.append(m.read_adc_data())
            t2 += 1
        elif t2 == BUFFER_SIZE and t1 == 0:
            buffer2.append(m.read_adc_data())
            print("Buffer 2 full... saving in file")
            print("t2a: " + str(t2))
            # Creating independent thread to save buffer in file
            thread_save = Thread(target=write_file, args=(fd, buffer2, t2))
            thread_save.start()
            print("t2a: " + str(t2))

        else:
            print("What are you doing here?")
            break

    elif io == 1:
        print("You're vary fast!")
        break

    else:
        print("Hemm xi haga hazina hafna!")
        print(str(DRDYOUT.digitalRead()))
        break

print("Ended now " + datetime.datetime.now().strftime("%H:%M:%S.%f"))
print("Closing file")
fd.close
exit()

#
# def pressed():
#     global z
#     print z
#     z += 1
# PC1 = Pin('PC1', 'INPUT')
# PC1.set_edge("falling", pressed)
#
# print m.read_adc_data()
#
# run_time = datetime.timedelta(seconds=3)
# until_time = datetime.datetime.now() + run_time
#
#
# while True:
#     # print str(m.read_adc_data())
#     if datetime.datetime.now() > until_time:
#         data_file.close()
#         exit()
#
#
# while datetime.datetime.now() < until_time:
#     pass
#     data_file.write(str(m.read_adc_data())+"\n")
#
# while True:
#     if datetime.datetime.now() > until_time:
#         data_file.close()
#         exit()
#     else:
#         data_file.write(str(PB.digitalRead()))
#         pass
#
#
# while True:
#     a = PB.digitalRead()
#     if a == 0:
#         print m.read_adc_data()
#     elif a == 1:
#         print "You're vary fast!"
#     else:
#         print "Hemm xihaga hazina hafna!"
#         print str(PB.digitalRead())
#         exit()
