import max11040klib
import time
import sched
import datetime
import bz2
# import configparser


class Log(object):

    def __init__(self, frequency):
        self.file = None
        self.msd = max11040klib.MaxSpiDev(0)
        self.delay = 1/frequency
        self.schedule = sched.scheduler(time.time, time.sleep)
        self.time_a = None
        self.time_b = None
        self.end_time = None
        self.segment_time = 1
        self.absolute_end_time = None

    def config(self, config_file):
        self.msd.set_registers(config_file)

    def start_log(self, segment_time, running_hours=1000000):
        self.file = bz2.BZ2File(datetime.datetime.now().strftime("%Y%j-%H%M%S.dat"), 'wb', 0)
        # todo: add a one time delay to time_a to give time for the initialization.
        # Put this delay in a config.ini file.
        self.time_a = time.time()
        self.time_b = self.time_a + self.delay
        self.segment_time = segment_time * 3600
        self.end_time = self.time_a + self.segment_time
        self.absolute_end_time = self.time_a + (running_hours * 3600)
        self.schedule.enterabs(self.time_b, 0, self.record, [])
        # self.record()
        self.schedule.run()
        # todo: check if we need to close the schedule object.

    def record(self):
        x, y, z, a = self.msd.read_adc_data()
        self.file.writelines(str(x)+"\t"+str(y)+"\t"+str(z)+"\t"+str(a)+"\n")
        self.time_a = self.time_b
        self.time_b = self.time_a + self.delay
        self.schedule.enterabs(self.time_b, 0, self.record, [])
        # self.loop.call_at(self.time_b, self.record)

        if self.time_b > self.end_time:
            self.file.close()
            self.file = bz2.BZ2File(datetime.datetime.now().strftime("%Y%j-%H%M%S.dat"), 'wb', 0)
            self.end_time = self.time_b + self.segment_time
            # todo: call write_headers

            # This "if" could have been made an "elif" command but to avoid an extra if statement at every
            # loop, we place this here. The down side is that logging will stop when both the segment_time
            # (or an integer number thereof) and the absolute_end_time have been exceeded.
            if self.time_b >= self.absolute_end_time:
                self.file.close()
                # todo: cancel schedule

    # todo: finish the command below to write header. Call this at the start of every logfile.
    # def write_headers(self):
    #     config = configparser.ConfigParser()
    #     config.read("header_info.ini")
