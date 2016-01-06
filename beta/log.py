import max11040klib
import time
import sched
import datetime
import bz2
import os


class Log(object):

    def __init__(self, frequency):
        self.file = None
        self.filename = None
        self.msd = max11040klib.MaxSpiDev(0)
        self.delay = 1/float(frequency)
        self.schedule = sched.scheduler(time.time, time.sleep)
        self.time_a = None
        self.time_b = None
        self.end_time = None
        self.segment_time = 1
        self.absolute_end_time = None

    # Sets the ADC's registers according to the "register_config.ini" file
    def init_adc(self):
        self.msd.set_registers()

    def start(self, segment_time, running_hours=1000000):
        self.filename = datetime.datetime.now().strftime("%Y%j-%H%M%S")
        self.file = bz2.BZ2File(self.filename, 'wb', 0)
        self.time_a = time.time()
        self.time_b = self.time_a + self.delay
        self.write_headers()
        self.segment_time = float(segment_time) * 3600
        self.end_time = self.time_a + self.segment_time
        self.absolute_end_time = self.time_a + (float(running_hours) * 3600)
        self.schedule.enterabs(self.time_b, 0, self.record, [])
        # self.record()
        self.schedule.run()

    def record(self):
        x, y, z, a = self.msd.read_adc_data()
        self.file.writelines(str(x)+";"+str(y)+";"+str(z)+";"+str(a)+"\n")
        self.time_a = self.time_b
        self.time_b += self.delay
        event = self.schedule.enterabs(self.time_b, 0, self.record, [])

        if self.time_b >= self.end_time:
            self.file.close()
            filename = datetime.datetime.now().strftime("%Y%j-%H%M%S")
            self.file = bz2.BZ2File(filename, 'wb', 0)
            self.write_headers()
            os.rename(self.filename, self.filename + ".bz2")
            self.filename = filename
            self.end_time = self.time_a + self.segment_time

            # This "if" could have been made an "elif" command but to avoid an extra if statement at every
            # loop, we place this here. The down side is that logging will stop when both the segment_time
            # (or an integer number thereof) and the absolute_end_time have been exceeded.
            if self.time_b >= self.absolute_end_time:
                self.file.close()
                self.schedule.cancel(event)

    def write_headers(self):
        timestamp = time.strftime('%Y-%m-%d_%H:%M:%S.', time.localtime(self.time_b))
        timestamp += str(self.time_b - int(self.time_b))[2:5]
        self.file.writelines("Startdatetime_UTC=" + timestamp + ";Delta=" + str(self.delay) + "\n")
