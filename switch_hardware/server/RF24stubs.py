

class RF24:
    def __init__(self, cepin, cspin):
        pass

    def begin(self):
        pass

    def enableDynamicPayloads(self):
        pass     

    def getDynamicPayloadSize(self):
        return 0

    def setRetries(self, delay, count):
        pass

    def openReadingPipe(self, number, address):
        pass

    def openWritingPipe(self, address):
        pass

    def startListening(self):
        pass

    def stopListening(self):
        pass

    def available(self):
        return True

    def read(self, len):
        return "1"

    def write(self, buf):
        pass
