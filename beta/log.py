import max11040klib
import asyncio
import datetime

class Log(object):

    def __init__(self, frequency):
        self.file = None
        self.msd = max11040klib.MaxSpiDev(0)
        self.delay = 1/frequency
        self.loop = asyncio.get_event_loop()
        self.time_a = self.loop.time()
        self.time_b = self.time_a + self.delay
        self.end_time = None
        self.segment_time = 1
        self.absolute_end_time = None

    def config(self, config_file):
        self.msd.set_registers(config_file)

    def start_log(self, segment_time, absolute_end_time=1000000):
        self.file = open(datetime.datetime.now().strftime("%Y%j-%H%M%S.dat"), "w")
        self.time_a = self.loop.time()
        self.time_b = self.time_a + self.delay
        self.end_time = self.loop.time() + (segment_time * 3600)
        self.absolute_end_time = self.loop.time() + (absolute_end_time * 3600)
        self.segment_time = segment_time * 3600
        self.record()
        self.loop.run_forever()
        self.loop.close()

    def record(self):
        x, y, z, a = self.msd.read_adc_data()
        self.file.write(str(x)+"\t"+str(y)+"\t"+str(x)+"\t"+str(a)+"\n")
        self.time_a = self.time_b
        self.time_b = self.time_a + self.delay
        self.loop.call_at(self.time_b, self.record)

        if self.time_b > self.end_time:
            self.file.close()
            self.file = open(datetime.datetime.now().strftime("%Y%j-%H%M%S.dat"), "w")
            self.end_time = self.time_b + self.segment_time
            # print("\nChanged log file name.\n")
            print(self.loop.time())

            # This "if" could have been made an "elif" command but to avoid an extra if statement at every
            # loop, we place this here. The down side is that logging will stop when both the segment_time
            # (or an integer number thereof) and the absolute_end_time have been exceeded.
            if self.time_b >= self.absolute_end_time:
                self.file.close()
                self.loop.stop()
