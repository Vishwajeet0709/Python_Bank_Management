import json
import random
import string
from pathlib import Path

class Bank:
    database = 'data.json'
    dummy_data = []                                       # Create Dummy Data

    try:
        if Path(database).exists():                       # Check File Exists or not?
            with open(database,'r') as fs:
                dummy_data = json.loads(fs.read())
        else:
            print("No such file exists")

    except Exception as Error:
        print(f"An exception occurd as {Error}")

    @classmethod
    def __update(cls):
        with open(cls.database,'w') as fs:
            fs.write(json.dumps(Bank.dummy_data))

    @classmethod
    def __accountgenerate(cls):
        alpha = random.choices(string.ascii_letters,k = 3)
        num = random.choices(string.digits,k = 3)
        spchar = random.choices("!@#$%^&*",k = 1)
        id = alpha + num+ spchar
        random.shuffle(id)
        return "".join(id)

    def createaccount(self):                                # Create account
        data = {
            'name': input("Enter your name: "),
            'age' : int(input("Enter your age: ")),
            'email' : input("Enter your Email address: "),
            'pin': int(input("Enter 4 digit pin which you want: ")),
            'accountNo' : Bank.__accountgenerate(),
            'balance' : 0 
        }

        if data['age'] < 18 or len(str(data['pin'])) != 4:
            print("Sorry you can not create account!")
        else:
            print("Account has been created successfully!")
            for i in data:
                print(f"{i}:{data[i]}")
            print("Please note down your account number")

            Bank.dummy_data.append(data)
            
            Bank.__update()

    def depositmoney(self):
        accno = input("Please enter your account number: ")
        pin = int(input("Please enter your pin: "))

        userdata = [i for i in Bank.dummy_data if i['accountNo'] == accno and i['pin'] == pin]

        if userdata == False:
            print("Sorry no data found!")
        else:
            amount = int(input("Please enter amount which you want deposit: "))
            if amount >= 10000 or amount <= 0:
                print("Sorry amount is not valid you can deposite amount in between 1 to 10000")
            else:
                print(userdata)
                userdata[0]['balance'] += amount
                Bank.__update()
                print("Amount diposited successfully!")


    def withdrowmoney(self):
        accno = input("Please enter your account number: ")
        pin = int(input("Please enter your pin: "))

        userdata = [i for i in Bank.dummy_data if i['accountNo'] == accno and i['pin'] == pin]

        if userdata == False:
            print("Sorry no data found!")
        else:
            amount = int(input("Please enter amount which you want withdrow: "))
            if userdata[0]['balance'] < amount:
                print("Sorry you don't have that much money")
            else:
                print(userdata)
                userdata[0]['balance'] -= amount
                Bank.__update()
                print("Amount Withdrow successfully!")

    
    def showdetails(self):
        accno = input("Input account number: ")
        pin = int(input("Please enter your pin: "))

        userdata = [i for i in Bank.dummy_data if i["accountNo"] == accno and i['pin'] == pin]
        print("Your information are \n")
        for i in userdata[0]:
            print(f"{i}: {userdata[0][i]}") 

    def updatedetails(self):
        accno = input("Enter account number: ")
        pin = int(input("Please enter pin: "))

        userdata = [i for i in Bank.dummy_data if i['accountNo'] == accno and i['pin'] == pin]
        
        if userdata == False:
            print("No such user found")
        else:
            print("You cannot change the age, account number, balance")

            print("Fill details details for change or leave it empty for no change")

            newdata = {
                'name': input("Please tell new name or press enter to skip: "),
                'email': input("Please enter new email or press enter to skip: "),
                'pin': input("Please enter new pin or press enter to skip: ")
            }

            if newdata['name'] == "":
                newdata['name'] = userdata[0]['name']
            if newdata['email'] == "":
                newdata['email'] = userdata[0]['email']
            if newdata['pin'] == "":
                newdata['pin'] = userdata[0]['pin']

            newdata['age'] = userdata[0]['age']
            newdata['accountNo'] = userdata[0]['accountNo']
            newdata['balance'] = userdata[0]['balance']

            if type(newdata['pin']) == str:
                newdata['pin'] = int(newdata['pin'])

            for i in newdata:
                if newdata[i] == userdata[0][i]:
                    continue
                else:
                    userdata[0][i] = newdata[i]

            Bank.__update()
            print("Details updated successfully!")


    def delete(self):
        accno = input("please enter account number: ")
        pin = int(input("please enter pin: "))

        userdata = [i for i in Bank.dummy_data if i['accountNo'] == accno and i['pin'] == pin]

        if userdata == False:
            print("sorry no such data exist ")
        else:
            check = input("press y if you actually want to delete the account or press n: ")
            if check == 'n'.lower():
                print("bypassed")
            else:
                index = Bank.dummy_data.index(userdata[0])
                Bank.dummy_data.pop(index)
                print("account deleted successfully ")
                Bank.__update()

            
user = Bank()
print("Press 1 for Craeting New Account")
print("Press 2 for Deposit The Money In The Bank")
print("Press 3 for Withdrow The Money")
print("Press 4 for Details")
print("Press 5 for Update The Details")
print("Press 6 for Delete Your Account")

check = int(input("Select your option between 1 to 6: "))
if check == 1:
    user.createaccount()

if check == 2:
    user.depositmoney()

if check == 3:
    user.withdrowmoney()

if check == 4:
    user.showdetails()

if check == 5:
    user.updatedetails()

if check == 6:
    user.delete()