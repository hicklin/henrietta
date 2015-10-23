from log import *
import ConfigParser

config = ConfigParser.ConfigParser()
config.read("config.ini")

sample_rate = float(config.get('logging', 'sample_rate'))
segment_time = float(config.get('logging', 'segment_time'))
running_hours = float(config.get('logging', 'running_hours'))

if __name__ == '__main__':
    l = Log(sample_rate)
    l.init_adc()
    l.start(segment_time, running_hours)
