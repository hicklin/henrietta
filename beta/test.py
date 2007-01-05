import max11040klib

m = max11040klib.MaxSpiDev(0)
m.set_registers("config.ini")

q = []
for i in range(0, 10000):
    q.append(m.read_adc_data())
