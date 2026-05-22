import json
import random
import string
from pathlib import Path


class Bank:
    database = "data.json"
    dummy_data = []

    # Load data
    try:
        if Path(database).exists():
            with open(database, "r") as fs:
                dummy_data = json.load(fs)
    except Exception as e:
        print(e)

    @classmethod
    def __update(cls):
        with open(cls.database, "w") as fs:
            json.dump(cls.dummy_data, fs, indent=4)

    @classmethod
    def __accountgenerate(cls):
        alpha = random.choices(string.ascii_letters, k=3)
        num = random.choices(string.digits, k=3)
        spchar = random.choices("!@#$%^&*", k=1)

        acc = alpha + num + spchar
        random.shuffle(acc)

        return "".join(acc)

    # CREATE ACCOUNT
    @classmethod
    def create_account(cls, name, age, email, pin):

        if age < 18:
            return None, "Age must be 18+"

        if len(str(pin)) != 4:
            return None, "PIN must be 4 digits"

        user = {
            "name": name,
            "age": age,
            "email": email,
            "pin": pin,
            "accountNo.": cls.__accountgenerate(),
            "balance": 0,
        }

        cls.dummy_data.append(user)
        cls.__update()

        return user, "Account created successfully"

    # FIND USER
    @classmethod
    def find_user(cls, acc_no, pin):

        for user in cls.dummy_data:
            if user["accountNo."] == acc_no and user["pin"] == pin:
                return user

        return None

    # DEPOSIT
    @classmethod
    def deposit(cls, acc_no, pin, amount):

        user = cls.find_user(acc_no, pin)

        if not user:
            return False, "Invalid account or PIN"

        if amount <= 0:
            return False, "Invalid amount"

        user["balance"] += amount

        cls.__update()

        return True, f"${amount} deposited successfully"

    # WITHDRAW
    @classmethod
    def withdraw(cls, acc_no, pin, amount):

        user = cls.find_user(acc_no, pin)

        if not user:
            return False, "Invalid account or PIN"

        if amount > user["balance"]:
            return False, "Insufficient balance"

        user["balance"] -= amount

        cls.__update()

        return True, f"${amount} withdrawn successfully"

    # UPDATE USER
    @classmethod
    def update_user(cls, acc_no, pin, name=None, email=None, new_pin=None):

        user = cls.find_user(acc_no, pin)

        if not user:
            return False, "Invalid account or PIN"

        if name:
            user["name"] = name

        if email:
            user["email"] = email

        if new_pin:
            if len(str(new_pin)) != 4:
                return False, "PIN must be 4 digits"

            user["pin"] = int(new_pin)

        cls.__update()

        return True, "Details updated successfully"

    # DELETE USER
    @classmethod
    def delete_user(cls, acc_no, pin):

        user = cls.find_user(acc_no, pin)

        if not user:
            return False, "Invalid account or PIN"

        cls.dummy_data.remove(user)

        cls.__update()

        return True, "Account deleted successfully"
