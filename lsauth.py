#!/usr/bin/env python

import argparse
import pickle
import md5
import os


LS_AUTH_DB_FILE = 'lsauth_users.p'


def add_user(username, password):
    if len(username) > 100 or len(password) > 100:
        print('ERROR: username or password exceeds character limit (100)')
        quit()

    auth_users = {}
    if os.path.isfile(LS_AUTH_DB_FILE):
        auth_users = pickle.load(open(LS_AUTH_DB_FILE, "rb"))

    if username in auth_users.keys():
        print('ERROR: {0} already in database'.format(username))
        quit()

    m = md5.new()
    m.update(password)

    auth_users[username] = m.digest()


def get_args():
    parser = argparse.ArgumentParser(description='Module for authenticating users')
    parser.add_argument('-add', nargs=2, metavar=('user', 'password'), help='add user')
    parser.add_argument('-rem', nargs=1, metavar='user', help='remove user')

    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()

    if args.add:
        add_user(args.add[0], args.add[1])
    elif args.rem:
        pass
