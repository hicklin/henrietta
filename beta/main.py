import datetime
import time
import max11040klib
import sched
import asyncio
import sys
import bz2

# Set runtime error maximum
sys.setrecursionlimit(1500)

scheduler = sched.scheduler(time.time, time.sleep)

m = max11040klib.MaxSpiDev(0)
m.set_registers("config.ini")

log_book = bz2.BZ2File(datetime.datetime.now().strftime("%Y%j-%H%M%S.dat"), 'wb', 0)
loop = asyncio.get_event_loop()
time_a = loop.time()


# Look into multiprocess module, otherwise used drdyout
def log(data_file, m_spi, loop, time_a):
    x, y, z, a = m_spi.read_adc_data()
    data_file.writelines(str(x)+"\t"+str(y)+"\t"+str(z)+"\t"+str(a)+"\n")
    time_b = time_a + 0.01
    loop.call_at(time_b, log, data_file, m_spi, loop, time_b)


def main(data_file, m_spi):

    loop = asyncio.get_event_loop()
    time_a = loop.time()
    log(data_file, m_spi, loop, time_a)
    loop.run_forever()
    # time.sleep(3)

    # next_datetime = datetime.datetime.now() + datetime.timedelta(days=1)
    # # next_schedule = next_datetime.replace(hour=0, minute=0, second=0)
    # time_a = time.time()
    # log_schedule(data_file, m_spi, time_a, time.time()+5)
    # # log_schedule(data_file, m_spi, time_a, time.mktime(next_schedule.timetuple()))
    # # data_file = open(next_datetime.strftime("%Y%j-%H%M%S.dat"), "w")
    # # scheduler.enterabs(time.mktime(next_schedule.timetuple()), 1, main, (data_file, m_spi,))

scheduler.run()
main(log_book, m)
