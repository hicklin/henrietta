import max11040klib
import datetime
import time

def day_log(file_name, m, end_time, frequency=100):
    log_book = open(file_name, "w")
    delay = 1/frequency

    while datetime.datetime.now() < end_time:
        x, y, z, a = m.read_adc_data()
        log_book.write(str(x)+"\t"+str(y)+"\t"+str(x)+"\t"+str(a)+"\n")
        time.sleep(delay)

    log_book.close()
