import Rpi.GPIO as GPIO
from mfrc522 import SimpleMFRC522


READER = SimpleMFRC522()


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
