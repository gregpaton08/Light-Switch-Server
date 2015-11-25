#!/usr/bin/env python

import argparse
import pickle
import md5
import os
import getpass


LS_AUTH_DB_FILE = 'lsauth_users.p'


def add_user(username):
    auth_users = {}
    if os.path.isfile(LS_AUTH_DB_FILE):
        auth_users = pickle.load(open(LS_AUTH_DB_FILE, "rb"))

    if username in auth_users.keys():
        print('ERROR: \'{0}\' already in database'.format(username))
        quit()

    password = getpass.getpass()
    if password != getpass.getpass():
        print('ERROR: passwords do not match!')
        quit()

    if len(username) > 100 or len(password) > 100:
        print('ERROR: username or password exceeds character limit (100)')
        quit()

    m = md5.new()
    m.update(password)

    auth_users[username] = m.digest()

    pickle.dump(auth_users, open(LS_AUTH_DB_FILE, "wb"))


def get_args():
    parser = argparse.ArgumentParser(description='Module for authenticating users')
    parser.add_argument('-add', nargs=1, metavar='user', help='add user')
    parser.add_argument('-rem', nargs=1, metavar='user', help='remove user')

    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()

    if args.add:
        add_user(args.add[0])
    elif args.rem:
        pass
