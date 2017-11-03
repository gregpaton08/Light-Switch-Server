# light-switch-server

## Interacting with the API

### CURL

```
# Light on
curl http://<RPi address>:<RPi port>/api/v1.0/light_status -X PUT -H "Content-Type: application/json" -d "{\"status\":true}"

# Light off
curl http://<RPi address>:<RPi port>/api/v1.0/light_status -X PUT -H "Content-Type: application/json" -d "{\"status\":false}"
```

### Useful Commands

```
# listports in use
netstat -tulnap

# list PIDs listening on ports
fuser <port num>/tcp
# kill processes listening on port
fuser <port num>/txp -k
```