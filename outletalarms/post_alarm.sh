#!/usr/bin/env bash

curl http://localhost:8000/alarms -X POST -H "Content-Type: application/json" -d \
"{\
    \"enabled\":true,\
    \"name\":\"morning alarm\",
    \"action\":\"set_switch_status true\",\
    \"minute\":18,\
    \"hour\":12,\
    \"days\":\"0,1,2,3,4,5,6\"\
}"