import pickle
import os

_LS_SWITCHES_DB_FILE = '.lsswitches.p'


def get_switches():
    if not os.path.isfile(_LS_SWITCHES_DB_FILE):
        return []
    switches = pickle.load(open(_LS_SWITCHES_DB_FILE, "rb"))
    if switches:
        return switches

    return []

def add_switch(switch):
    # Get current list of switches
    switches = []
    if os.path.isfile(_LS_SWITCHES_DB_FILE):
        switches = pickle.load(open(_LS_SWITCHES_DB_FILE, "rb"))

    # Only take the valid properties from the passed in switch dict
    new_switch = {
        'room'   : switch.get('room', ''),
        'device' : switch.get('device', ''),
        'status' : switch.get('status', False)
    }
    
    # Assign a uniqye id to the switch
    id_list = [x['id'] for x in switches]
    id = 0
    while id in id_list:
        id = id + 1
    new_switch['id'] = id

    switches.append(new_switch)

    pickle.dump(switches, open(_LS_SWITCHES_DB_FILE, "wb"))

def delete_switch(id):
    if os.path.isfile(_LS_SWITCHES_DB_FILE):
        switches = pickle.load(open(_LS_SWITCHES_DB_FILE, "rb"))
        new_switches = [x for x in switches if id == x.get('id', -1)]
        pickle.dump(new_switches, open(_LS_SWITCHES_DB_FILE, "wb"))
                

if __name__ == '__main__':
    switch = {
        'id' : 0,
        'title' : u'Bedroom',
        'status' : False,
        'outlet' : 0
    }
    #add_switch(switch)
