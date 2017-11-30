#!/usr/bin/env bash

script_link="/etc/init.d/run_ls_server.sh"
if [ ! -f "$script_link" ]; then
    echo "Adding symbolic like to /etc/init.d"
    ln -s ../run.sh $script_link
fi

service="light_switch"
if [ ! -e "/etc/init.d/$service" ]; then
    echo "Adding service to etc/init.d"
    cp $service /etc/init.d
    update-rc.d sample.py defaults
fi