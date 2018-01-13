# Outlet Alarms

## Interacting with the API

### CURL

```
# 
curl http://localhost:8000/alarms -X POST -H "Content-Type: application/json" -d \
"{\
    \"enabled\":true\
}"

# Light off
curl http://<RPi address>:<RPi port>/api/v1.0/light_status -X PUT -H "Content-Type: application/json" -d "{\"status\":false}"
```