# Outlet Alarms

## Interacting with the API

### CURL

```
# Create an alarm
curl http://localhost:8000/alarms -X POST -H "Content-Type: application/json" -d \
"{\
    \"enabled\":true,\
    \"action\":\"set_switch_status on\",\
    \"minute\":34,\
    \"hour\":10,\
    \"days\":\"0,1,2,3,4,5,6\"\
}"

# Get a list of all alarms
curl http://localhost:8000/alarms -X GET
```

```
# Get an alarm with the provided ID
curl http://localhost:8000/alarms/19a9619319b344e5b5c27009ac474f3f -X GET

# Update the settings of an alarm
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

## References

[API Docs](http://apscheduler.readthedocs.io/en/latest/py-modindex.html)

