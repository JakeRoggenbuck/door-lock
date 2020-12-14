import sqlite3
from random import randint
import string
import enum


class Permission(enum.Enum):
    NONE = 0
    HIGH = 3
    MEDIUM = 2
    LOW = 1


class Database:
    def __init__(self, name="database.db"):
        self.name = name
        self.db = sqlite3.connect(self.name)

    def create_table(self):
        sql = f"""
            CREATE TABLE codes (
            key_number INTEGER PRIMARY KEY,
            key_info VARCHAR(200),
            permission INT,
            active INT,
            key_data VARCHAR(40));"""
        self.db.cursor().execute(sql)
        self.db.commit()

    def generate_key_data(self) -> str:
        key_data = ""
        for x in range(40):
            key_data += string.ascii_letters[randint(0, 51)]
        return key_data

    def add_key(self, key_info: str, permission: int, actived: int, key_data: str):
        sql = "INSERT INTO codes (key_info, permission, active, key_data) VALUES (?, ?, ?, ?)"
        self.db.cursor().execute(sql, (key_info, permission, actived, key_data))
        self.db.commit()

    def delete_key(self, key_number: int):
        sql = "DELETE FROM codes WHERE key_number = ?"
        self.db.cursor().execute(sql, (key_number,))

    def revoke_key(self, key_number: int):
        sql = "UPDATE codes SET active = 0 WHERE key_number = ?"
        self.db.cursor().execute(sql, (key_number,))

    def activate_key(self, key_number: int):
        sql = "UPDATE codes SET active = 1 WHERE key_number = ?"
        self.db.cursor().execute(sql, (key_number,))

    def check_key(self, data: str) -> int:
        sql = "SELECT * FROM codes WHERE key_data = ?"
        cursor = self.db.cursor()
        cursor.execute(sql, (data,))
        found = cursor.fetchone()
        print(found)
        if found is not None:
            return Permission(found[2])
        else:
            return Permission(0)

    def view_all_keys(self):
        sql = "SELECT * FROM codes"
        cursor = self.db.cursor()
        cursor.execute(sql)
        found = cursor.fetchall()
        return found
