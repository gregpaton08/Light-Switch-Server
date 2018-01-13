# Outlet Alarms

## Interacting with the API

### CURL

```
# 
curl http://localhost:8000/alarms -X POST -H "Content-Type: application/json" -d \
"{\
    \"enabled\":true\
}"

curl http://<RPi address>:<RPi port>/api/v1.0/light_status -X PUT -H "Content-Type: application/json" -d "{\"status\":false}"

curl http://localhost:8000/alarms -X GET
```

```
curl http://localhost:8000/alarms/5cb872fff45c430d9e55f52559a13860 -X GET

curl http://localhost:8000/alarms/5cb872fff45c430d9e55f52559a13860 -X DELETE
```