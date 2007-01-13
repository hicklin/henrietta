import spidev
import configparser

class MaxSpiDev(spidev.SpiDev):
    """
    This is a subclass of SpiDev. MaxSpiDev is a class specifically for
    communicating with the MAX11040k 24-bit 4-channel ADC.
    """

    def __init__(self, cs):
        # Initializing the SpiDev class
        super(MaxSpiDev, self).__init__()
        # Opening the device on chip select cs
        self.open(32766, cs)
        # setting the clock speed for communication
        self.max_speed_hz = 24576000

    # Write to Configuration register
    def write_configuration_register(self, cr):
        if len(cr) != 1:
            return "1 byte is required"
        CR = [0x60]
        CR.extend(cr)
        _ = self.xfer(CR)

    # Read configuration register -- returns register in hex
    def read_configuration_register(self):
        response_CR = self.xfer([0xe0, 0x00])
        return hex(response_CR[1])

    # Write to Data-rate control register
    def write_data_rate_control_register(self, drcr):
        if len(drcr) != 2:
            return "2 bytes are required"
        DRCR = [0x50]
        DRCR.extend(drcr)
        _ = self.xfer(DRCR)

    # Read Data-rate control register -- returns register in hex
    def read_data_rate_control_register(self):
        read_byte = [0xd0]
        read_byte.extend([0x00] * 2)
        response_DRCR = self.xfer(read_byte)
        return hex(response_DRCR[1]), hex(response_DRCR[2])

    # Write to Sampling instant control register
    def write_sampling_instant_control_register(self, sicr):
        if len(sicr) != 4:
            return "4 bytes are required"
        SICR = [0x40]
        SICR.extend(sicr)
        _ = self.xfer(SICR)

    # Read Sampling instant control register
    def read_sampling_instant_control_register(self):
        read_byte = [0xc0]
        read_byte.extend([0x00] * 4)
        response_SICR = self.xfer(read_byte)
        return hex(response_SICR[1]), hex(response_SICR[2]), hex(response_SICR[3]), hex(response_SICR[4])

    # Read ADC data -- data is returned as 4 separate values
    ####################################################################
    # IMP: This function is designed for 24 bit resolution therefore,  #
    # XTALEN in the configuration register is set high                 #
    ####################################################################
    def read_adc_data(self):
        read_byte = [0xf0]
        read_byte.extend([0x00] * 12)
        ADC_data = self.xfer(read_byte)

        # Convert hex to binary
        ADC_bins = []
        for byte in ADC_data[1:]:
            ADC_bins.append(format(byte, '#010b')[2:])

        # Selects channel bytes, converts to binary, concatenates binaries, calculate resultant
        # int -- returns a 4-element array containing integer value readings of the 4 channels
        channels = []
        for i in range(0, 4):
            j = 3 * i
            channel = int(ADC_bins[j] + ADC_bins[j+1] + ADC_bins[j+2], 2)
            if channel & 0x800000:
                channel -= 0x1000000
            channels.append(channel*3.3/0x800000)

        return channels

    def set_registers(self, ini_file):
        config = configparser.ConfigParser()
        config.read(ini_file)
        # Write settings from ini file to chip
        self.write_data_rate_control_register(eval(config.get('registers', 'data_rate_control_register')))
        self.write_configuration_register(eval(config.get('registers', 'configuration_register')))
        self.write_sampling_instant_control_register(eval(config.get('registers', 'sampling_control_register')))
        # Print register settings
        print("\n********************")
        print("* Settings written *")
        print("********************\n")
        print("Configuration register:            " + str(self.read_configuration_register()))
        print("Data rate control register:        " + str(self.read_data_rate_control_register()))
        print("Sampling instant control register: " + str(self.read_sampling_instant_control_register()))
        print("********************\n")

    def read_registers(self):
        # Print register settings
        print("\n********************")
        print("*    Registers     *")
        print("********************\n")
        print("Configuration register:            " + str(self.read_configuration_register()))
        print("Data rate control register:        " + str(self.read_data_rate_control_register()))
        print("Sampling instant control register: " + str(self.read_sampling_instant_control_register()))
        print("********************\n")
