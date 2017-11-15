import time
from RF24 import *

### NRF24l01 pinout
# 1 GND  =>  ground
# 2 VCC  =>  3.3V
# 3 CE   =>  GPIO22
# 4 CSN  =>  SPI CE0
# 5 SCK  =>  CPI CLK
# 6 MOSI =>  SPI MOSI
# 7 MISO =>  SPI MISO
# 8 IRQ  =>  ?



class OutletSwitch:
    def __init__(self):
        self.radio = RF24(22, 0);
        self.reading_pipe = 0xF0F0F0F0E1
        self.writing_pipe = 0xF0F0F0F0D2

        self.radio.begin()
        self.radio.enableDynamicPayloads()
        self.radio.setRetries(5, 15)

        self.radio.openReadingPipe(1, self.reading_pipe)
        self.radio.openWritingPipe(self.writing_pipe)
        self.radio.startListening()

        self.millis = lambda: int(round(time.time() * 1000))

    def __send_message(self, message, retries=100):
        for x in xrange(retries):
            self.radio.stopListening()
            self.radio.write(message)
            self.radio.startListening()

            # Wait here until for a response, or timeout.
            started_waiting_at = self.millis()
            timeout = False
            while (not self.radio.available()) and (not timeout):
                if (self.millis() - started_waiting_at) > 250:
                    timeout = True

            if not timeout:
                break

        if timeout:
            raise Exception('Status request timed out')
        else:
            return self.radio.read(self.radio.getDynamicPayloadSize())

    def set_status(self, on):
        self.__send_message(bytes(1 if on else 0))

    def get_status(self):
        if self.__send_message(bytes(2)) == "1":
            return True
        return False