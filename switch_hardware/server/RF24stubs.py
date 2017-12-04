import pickle

class RF24:
    def __init__(self, cepin, cspin):
        self.status_file = '.rf24.stubs.status.pkl'

    def __get_status(self):
        try:
            with open(self.status_file, 'rb') as file:
                data = pickle.load(file)
            return data['status']
        except:
            return False

    def __set_status(self, status):
        with open(self.status_file, 'wb') as file:
            data = { 'status' : status }
            pickle.dump(data, file)

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
        return '1' if self.__get_status() else '0'

    def write(self, buf):
        if buf == bytes(1):
            self.__set_status(True)
        elif buf == bytes(0):
            self.__set_status(False)
