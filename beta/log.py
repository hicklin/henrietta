import max11040klib
import asyncio

class Log(object):

    def __init__(self, log_start_datetime, frequency):
        self.file = open(log_start_datetime.strftime("%Y%j-%H%M%S.dat"), "w")
        self.msd = max11040klib.MaxSpiDev(0)
        self.delay = 1/frequency
        self.loop = asyncio.get_event_loop()
        self.time_a = self.loop.time()
        self.time_b = self.time_a + self.delay
        self.end_time = None

    def config(self, config_file):
        self.msd.set_registers(config_file)

    def start_log(self, hours):
        self.time_a = self.loop.time()
        self.time_b = self.time_a + self.delay
        self.end_time = self.loop.time() + (hours * 3600)
        self.record()
        self.loop.run_forever()
        self.loop.close()

    def record(self):
        x, y, z, a = self.msd.read_adc_data()
        self.file.write(str(x)+"\t"+str(y)+"\t"+str(x)+"\t"+str(a)+"\n")
        if self.time_b < self.end_time:
            self.time_a = self.time_b
            self.time_b = self.time_a + self.delay
            self.loop.call_at(self.time_b, self.record)
        else:
            self.loop.stop()
            self.file.close()
