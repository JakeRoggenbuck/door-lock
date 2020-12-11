import argparse
from database import Database, Permission
from key import write_data_to_key, read_key


DATABASE = Database()


def setup():
    DATABASE.create_table()


def create_key():
    key_info = input("Key info: ")
    if len(key_info) > 180:
        print("Make info shorter")
        exit()

    permission = int(input("Number 1-3, 3 being HIGH: "))
    if permission not in [1, 2, 3]:
        print("Pick a correct permission 1-3")
        exit()

    should_activate = input("Activate now? [Y/n]: ").upper()
    if should_activate not in ["Y", "N"]:
        print("Pick Y or N")
        exit()

    if should_activate == "Y":
        activate = 1
    else:
        activate = 0

    data = DATABASE.generate_key_data()
    if write_data_to_key(data):
        DATABASE.add_key(key_info, permission, activate, data)
    else:
        print("Failed to write data")


def main_read():
    while 1:
        key = read_key()
        if key is not None:
            id, data = key
            perms = DATABASE.check_key(data)
            print(perms)


def parse_args():
    parse = argparse.ArgumentParser()
    parse.add_argument("-m", help="Main read loop", action='store_true')
    parse.add_argument("-w", help="Write a key", action='store_true')
    parse.add_argument("-v", help="View all of the keys", action='store_true')
    return parse.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.m:
        main_read()
    elif args.w:
        create_key()
    elif args.v:
        for key in DATABASE.view_all_keys():
            print(key)
