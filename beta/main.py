import datetime
import time
import max11040klib
import threading
import sched

scheduler = sched.scheduler(time.time, time.sleep)

m = max11040klib.MaxSpiDev(0)
m.set_registers("config.ini")

log_book = open(datetime.datetime.now().strftime("%Y%j-%H%M%S.dat"), "w")


def log(data_file, m_spi, delay=0.01):
    threading.Timer(delay, log, [data_file, m_spi]).start()
    x, y, z, a = m_spi.read_adc_data()
    data_file.write(str(x)+"\t"+str(y)+"\t"+str(x)+"\t"+str(a)+"\n")


def main(data_file, m_spi):
    log(data_file, m_spi)
    next_datetime = datetime.datetime.now() + datetime.timedelta(days=1)
    data_file = open(next_datetime.strftime("%Y%j-%H%M%S.dat"), "w")
    next_schedule = next_datetime.replace(hour=0, minute=0, second=0)
    scheduler.enterabs(time.mktime(next_schedule.timetuple()), 1, log, (data_file, m_spi,))

main(log_book, m)
scheduler.run()
