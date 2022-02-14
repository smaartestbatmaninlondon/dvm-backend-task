
# importing the necessary libraries
import pandas as pd
import mysql.connector as sqlator
import random as rand
import sys

con = sqlator.connect(host='localhost', user='root',  password="Current-Root-Password", database='dvmtask1')  # starting a connection with mysql database
cursor = con.cursor()


class credentials:
    def __init__(self, account_no, pin):
        self.account_no=account_no
        self.pin=pin

    def verification(self):
        query = '''select exists (select * from accounts where account_no=%s)''' % (self.account_no)
        quer = pd.read_sql(query, con)
        if (quer.iat[0, 0]) == 1:
            query1 = '''select pin from accounts where account_no=%s''' % (self.account_no)
            quer1 = pd.read_sql(query1, con)
            if (quer1.pin[0]) != self.pin:
                print("Verification successful. Please check the pin again!")
                return 0
            else:
                print("Verification successful. ")
                return 1
        else:
            print("Verification unsuccessful. Please check the account number again!")
            return 0

    def return_acc_no(self):
        return self.account_no
    def return_pin(self):
        return self.pin



class functions(credentials):
    def __init__(self, account_no, pin):
        super().__init__(account_no,pin)
        pass

    def createaccount():
        print('PLEASE ENTER THE FOLLOWING CREDENTIALS IN ORDER TO CREATE AN ACCOUNT:')
        c = input('FULL NAME:')  # taking in information
        e = int(input('CONTACT NO.:'))
        f = input("EMAIL ID:")
        query1 = '''select account_no from accounts '''  # checking whether the entered pin is correct or not
        quer1 = pd.read_sql(query1, con)
        p = rand.randint(10000000, 99999999)
        while p in quer1:
            p = rand.randint(10000000, 99999999)
        # p is the account number which is the primary key in database
        h = 0
        print('would you like to open a savings account or a current account?')
        while h == 0:
            print('press 1 for savings')
            print('press 2 for current')
            i = int(input())
            if i == 1:
                j = 'savv'
                h = 1
            elif i == 2:
                j = 'curr'
                h = 1
            else:
                print('please enter 1 or 2:')
        k = 0
        print('would you like to deposit some money?')
        while k == 0:
            print('press 1 if you want to deposit some money.')
            print('press 2 if you want to skip.')
            l = int(input())
            if l == 1:
                print('how much money would you like to deposit?')
                m = int(input())
                k = 1
            elif l == 2:
                k = 1
                m = 0
            else:
                print('please enter 1 or 2.')
        n = rand.randint(1000, 9999)  # generating a random pin for the account
        print('your account number is:', p)
        print('your randomly generated pincode is:', n)
        print('Your account has been successfully created, thanks for choosing bank by pi!')
        cursor = con.cursor()
        query = '''INSERT INTO accounts values (%s,%s,%s,%s,%s,%s,%s)'''  # inserting a new record in the database
        inpu = (j, p, e, m, f, n, c)
        cursor.execute(query, inpu)
        con.commit()
        cursor.close()

    def deposit():
        print('PLEASE ENTER THE AMOUNT YOU WANT TO DEPOSIT:')
        deposit = int(input())
        print('PLEASE ENTER YOUR ACCOUNT NUMBER:')
        accno = int(input())
        print('PLEASE ENTER YOUR PINCODE:')
        pin = int(input())
        if credentials(accno,pin).verification()==1:
            cursor = con.cursor()
            query2 = '''update accounts set balance=balance+%s where account_no=%s'''  # updating the balance after deposition
            inpu = (deposit, credentials(accno,pin).return_acc_no())
            cursor.execute(query2, inpu)
            con.commit()
            cursor.close()
            print(deposit, 'rupees deposited successfully!')
            query3 = '''select balance from accounts where account_no=%s''' % (credentials(accno,pin).return_acc_no())
            quer3 = pd.read_sql(query3, con)  # displaying the updated balance
            print('updated balance:', quer3.balance[0])
        else:
            pass

    def withdraw():
        print('PLEASE ENTER THE AMOUNT YOU WANT TO WITHDRAW:')
        withdraw = int(input())
        print('PLEASE ENTER YOUR ACCOUNT NUMBER:')
        accno = int(input())
        print('PLEASE ENTER YOUR PINCODE:')
        pin = int(input())
        if credentials(accno, pin).verification() == 1:
             query = '''select balance from accounts where account_no=%s''' % (credentials(accno, pin).return_acc_no())
             quer = pd.read_sql(query, con)
             if  quer.balance[0]> withdraw:
                 cursor = con.cursor()
                 query2 = '''update accounts set balance=balance-%s where account_no=%s'''
                 inpu = (withdraw, accno)
                 cursor.execute(query2, inpu)
                 con.commit()
                 cursor.close()
                 print(withdraw, 'rupees withdrawn successfully!')
                 query4 = '''select balance from accounts where account_no=%s''' % (credentials(accno,pin).return_acc_no())
                 quer4 = pd.read_sql(query4, con)
                 print('updated balance:', quer4.balance[0])  # displaying the updated balance
             else:
                 print('insufficient funds!')
        else:
            pass

    def balance():
        print('PLEASE ENTER YOUR ACCOUNT NUMBER:')
        accno = int(input())
        print('PLEASE ENTER YOUR PINCODE:')
        pin = int(input())
        if credentials(accno, pin).verification() == 1:
            query4 = '''select balance from accounts where account_no=%s''' % (accno)
            quer4 = pd.read_sql(query4, con)
            print('Balance:', quer4.balance[0])
        else:
            pass

    def admin():
        passwd = 'bankproject'
        print('PLEASE ENTER THE ADMIN PASSWORD TOO PROCEED:')
        pass1 = input()
        if pass1 == passwd:
            query5 = '''select account_no,phone_no,email_id,savcurr,name from accounts'''
            quer5 = pd.read_sql(query5, con)
            print(quer5)
        else:
            print('WRONG PASSWORD! please try again.')


    def Home():
        f = 1
        while f != 9:
            print('WELCOME:')
            print('_________________________________________________________________')
            print('1. CREATE NEW ACCOUNT')
            print('2. DEPOSIT AMOUNT')
            print('3. WITHDRAW AMOUNT')
            print('4. BALANCE ENQUIRY')
            print('5. ACCOUNT HOLDER LIST (only admin)')
            print('6. EXIT')
            print('_________________________________________________________________')
            print('\n', 'SELECT FROM 1-6')
            f = int(input("Enter your choice: "))
            if f == 1:
                functions.createaccount()
            elif f == 2:
                functions.deposit()
            elif f == 3:
                functions.withdraw()
            elif f == 4:
                functions.balance()
            elif f == 5:
                functions.admin()
            elif f == 6:
                print('THANKS FOR VISITING !')
                cursor.close()
                con.close()
                sys.exit
            else:
                functions.Home()

functions.Home()
