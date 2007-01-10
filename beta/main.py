import datetime
import time
import max11040klib
import threading
import sched
import sys

sys.setrecursionlimit(1500)

scheduler = sched.scheduler(time.time, time.sleep)

m = max11040klib.MaxSpiDev(0)
m.set_registers("config.ini")

log_book = open(datetime.datetime.now().strftime("%Y%j-%H%M%S.dat"), "w")
schedule_counter = 0
read_counter = 0

# Look into multiprocess module, otherwise used drdyout
def log(data_file, m_spi):
    x, y, z, a = m_spi.read_adc_data()
    data_file.write(str(x)+"\t"+str(y)+"\t"+str(x)+"\t"+str(a)+"\n")
    global read_counter
    read_counter = read_counter+1 & 127


def log_schedule(data_file, m_spi, time_a, end_time):
    time_b = time_a+0.01
    global schedule_counter
    global read_counter
    if schedule_counter + 1 != read_counter:
        if time_b < end_time:
            scheduler.enterabs(time_b-time.time(), 1, log, (data_file, m_spi,))
            scheduler.run()
            schedule_counter = schedule_counter+1 & 127
            print "s: " + str(schedule_counter)
            print "r: " + str(read_counter)
            log_schedule(data_file, m_spi, time_b, end_time)
        else:
            data_file.close()
    else:
        log_schedule(data_file, m_spi, time_a, end_time)


def main(data_file, m_spi):
    next_datetime = datetime.datetime.now() + datetime.timedelta(days=1)
    # next_schedule = next_datetime.replace(hour=0, minute=0, second=0)
    time_a = time.time()
    log_schedule(data_file, m_spi, time_a, time.time()+5)
    # log_schedule(data_file, m_spi, time_a, time.mktime(next_schedule.timetuple()))
    # data_file = open(next_datetime.strftime("%Y%j-%H%M%S.dat"), "w")
    # scheduler.enterabs(time.mktime(next_schedule.timetuple()), 1, main, (data_file, m_spi,))

scheduler.run()
main(log_book, m)
