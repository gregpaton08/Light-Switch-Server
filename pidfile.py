import os

class PidFile:
    def __init__(self, file_name='pid_file'):
        self.file_name = file_name

        pidFile = open(self.file_name, 'w')
        pidFile.write(str(os.getpid()))
        pidFile.close()

    def cleanup(self):
        try:
            os.remove(self.file_name)
        except OSError:
            pass