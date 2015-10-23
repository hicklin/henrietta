from log import *

if __name__ == '__main__':
    l = Log(100)
    l.init_adc()
    l.start(1.0/360, 3.0/360)
