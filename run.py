#!venv/bin/python

import sys
from outletswitch import app

DEBUG = False

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

    print 'light switch server shutting down...'
