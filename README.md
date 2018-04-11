# light-switch-server

## Run From Fresh Install

```
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install python-pip
sudo pip install virtualenv

```

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

## Trouble Shooting

Address already in use

```
sudo service light_switch stop
ps -fA | grep python
```

The number in the second column is the PID

`sudo kill -9 <PID>`