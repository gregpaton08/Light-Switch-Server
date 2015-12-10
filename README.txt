useful commands

# listports in use
netstat -tulnap

# list PIDs listening on ports
fuser <port num>/tcp
# kill processes listening on port
fuser <port num>/txp -k
