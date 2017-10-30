import pickle
import os

_LS_ALARMS_DB_FILE = '.lsalarms.p'


def get_alarms():
    if not os.path.isfile(_LS_ALARMS_DB_FILE):
        return []
    switches = pickle.load(open(_LS_ALARMS_DB_FILE, "rb"))
    if switches:
        return switches

    return []

def add_switch(alarm):
    # Get current list of switches
    alarms = []
    if os.path.isfile(_LS_ALARMS_DB_FILE):
        alarms = pickle.load(open(_LS_ALARMS_DB_FILE, "rb"))

    # Only take the valid properties from the passed in switch dict
    new_alarm = {
        'minute' : alarm.get('minute', ''),
        'hour'   : alarm.get('hour', ''),
        'dow'    : alarm.get('dow', False)
    }
    
    # Assign a uniqye id to the switch
    id_list = [x['id'] for x in alarms]
    id = 0
    while id in id_list:
        id = id + 1
    new_alarms['id'] = id

    alarms.append(new_alarm)

    pickle.dump(alarms, open(_LS_ALARMS_DB_FILE, "wb"))

def delete_alarm(id):
    if os.path.isfile(_LS_ALARMS_DB_FILE):
        alarms = pickle.load(open(_LS_ALARMS_DB_FILE, "rb"))
        new_alarms = [x for x in alarms if id == x.get('id', -1)]
        pickle.dump(new_alarms, open(_LS_ALARMS_DB_FILE, "wb"))
                

if __name__ == '__main__':
    switch = {x
        'id' : 0,
        'title' : u'Bedroom',
        'status' : False,
        'outlet' : 0
    }
    #add_switch(switch)
