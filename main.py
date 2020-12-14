import argparse
from database import Database, Permission
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep



READER = SimpleMFRC522()
DATABASE = Database()
GPIO.setmode(GPIO.BCM)


REPLAY_PIN = 17
GPIO.setup(REPLAY_PIN, GPIO.OUT)
GPIO.output(REPLAY_PIN, 0)


def setup():
    DATABASE.create_table()


def write_data_to_key(data: str):
    did_complete = False
    try:
        READER.write(data)
        print("Data written")
        did_complete = True
    finally:
        GPIO.cleanup()

    return did_complete


def read_key():
    did_complete = False
    try:
        id, text = READER.read()
        did_complete = True
    finally:
        GPIO.cleanup()

    if did_complete:
        return id, text


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


def unlock():
    GPIO.output(REPLAY_PIN, 1)
    sleep(30)
    GPIO.output(REPLAY_PIN, 0)


def main_read():
    while 1:
        key = read_key()
        if key is not None:
            id, data = key
            data = data.strip()
            perms = DATABASE.check_key(data)
            if perms == Permission(3):
                unlock()
            elif perms == Permission(2):
                unlock()
            elif perms == Permission(1):
                unlock()


def parse_args():
    parse = argparse.ArgumentParser()
    parse.add_argument("-m", help="Main read loop", action='store_true')
    parse.add_argument("-w", help="Write a key", action='store_true')
    parse.add_argument("-v", help="View all of the keys", action='store_true')
    parse.add_argument("-s", help="Setup", action='store_true')
    return parse.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.m:
        main_read()
    elif args.s:
        setup()
    elif args.w:
        create_key()
    elif args.v:
        for key in DATABASE.view_all_keys():
            print(key)
