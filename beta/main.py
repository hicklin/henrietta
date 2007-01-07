from logging import *
import threading

m = max11040klib.MaxSpiDev(0)
m.set_registers("config.ini")
logged = datetime.datetime.now().date() - datetime.timedelta(days=1)

while True:
    while datetime.datetime.now().date() != logged:
        now = datetime.datetime.now()
        # end_time = (datetime.datetime.now() + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0)
        end_time = now + datetime.timedelta(seconds=1)
        logged = now.date()
        data_file_name = datetime.datetime.now().strftime("%Y%j-%H%M%S.dat")
        log_book = open(data_file_name, "w")
        t = threading.Thread(target=day_log, args=(log_book, m, end_time))
        t.start()
        time.sleep((end_time-now).total_seconds())
        exit()
