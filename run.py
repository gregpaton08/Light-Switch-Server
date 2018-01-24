#!venv/bin/python

import sys
from outletswitch import app
import signal

DEBUG = False

def sigterm_handler(_signo, _stack_frame):
    sys.exit(0)

signal.signal(signal.SIGTERM, sigterm_handler)

if __name__ == "__main__":
    port = 3333
    try:
        port = int(sys.argv[1])
    except IndexError:
        pass

    try:
        app.run(host='0.0.0.0', port=port, debug=DEBUG)
    except KeyboardInterrupt:
        pass
    finally:
        pass

    print 'light switch server shutting down...'
