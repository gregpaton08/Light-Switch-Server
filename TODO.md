# To Do  

## Tasks
* bug: see error_log.txt for details 
* Implement authentication for web and mobile
* bug: fix this error:
```
bcm2835_init: gpio mmap failed: Cannot allocate memory
/home/pi/projects/light_switch/run.sh: line 4:  2228 Segmentation fault      ${DIR}/venv/bin/python ${DIR}/run.py $@
```
* research: make generic switches which can be added/configured by the user without adhoc programming
  * create name, edit name, delete -> standard HTTP/REST operations
* fix hardware: add transitor/diode to control relay
* Add logging to flask server 
* Add progress/spinner when loading/setting light status (front end) (possible with pure CSS? codepen)
* Replace on/off button with lightbulb graphic that visually turns on/off, displays current status
* iOS app and widget (separate project)
* research: how to install (?) so that production is separate from development environment
* add alarm API and interface (e.g. turn on living room light at 6am)
* build remote to control light (button + arduino + NRF)

## Completed  
* REST API
* AJAX front end using REST API
* Change displayed texted to "loading..." when loading page or on/off action is in progress
* Update front end to display status now that GET is supported


## Stretch Goals  

