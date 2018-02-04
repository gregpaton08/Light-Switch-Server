#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
script_link="/etc/init.d/run_outlet_switch.sh"
if [ ! -f "$script_link" ]; then
    echo "Adding run script to /etc/init.d"
    echo "${DIR}/../run.sh" > $script_link
fi

service="light_switch"
if [ ! -e "/etc/init.d/$service" ]; then
    echo "Adding service to etc/init.d"
    cp $service /etc/init.d
    update-rc.d $service defaults
fi
