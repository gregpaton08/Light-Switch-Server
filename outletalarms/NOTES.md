# Outlet Alarms

## Interacting with the API

### CURL

```
# 
curl http://localhost:8000/alarms -X POST -H "Content-Type: application/json" -d \
"{\
    \"enabled\":true\
}"

curl http://localhost:8000/alarms -X GET
```

```
curl http://localhost:8000/alarms/19a9619319b344e5b5c27009ac474f3f -X GET

curl http://localhost:8000/alarms/19a9619319b344e5b5c27009ac474f3f -X PUT -d \
"{\
    \"enabled\":true,\
    \"action\":\"switch 0 on\",\
    \"minute\":34,\
    \"hour\":10,\
    \"days\":\"0,1,2,3,4,5,6\"\
}"

curl http://localhost:8000/alarms/19a9619319b344e5b5c27009ac474f3f -X PUT -H "Content-Type: application/json" -d \
"{\
    \"hour\":11,\
    \"minute\":35\
}"

curl http://localhost:8000/alarms/19a9619319b344e5b5c27009ac474f3f -X PUT -H "Content-Type: application/json" -d \
"{\
    \"name\":\"RISE AND SHINE"\!"\"\
}"


curl http://localhost:8000/alarms/19a9619319b344e5b5c27009ac474f3f -X DELETE
```