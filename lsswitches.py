import pickle
import os

_LS_SWITCHES_DB_FILE = 'lsswitches.p'


def get_switches():
    if not os.path.isfile(_LS_SWITCHES_DB_FILE):
        return []
    switches = pickle.load(open(_LS_SWITCHES_DB_FILE, "rb"))
    if switches:
        return switches

    return []

def add_switch(switch):
    print("adding switch")
    switches = []
    if os.path.isfile(_LS_SWITCHES_DB_FILE):
        switches = pickle.load(open(_LS_SWITCHES_DB_FILE, "rb"))
    switches.append(switch)
    print(switches)
    pickle.dump(switches, open(_LS_SWITCHES_DB_FILE, "wb"))

if __name__ == '__main__':
    switch = {
        'id' : 0,
        'title' : u'Bedroom',
        'status' : False,
        'outlet' : 0
    }
    #add_switch(switch)
