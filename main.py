
# importing the necessary libraries
import pandas as pd
import mysql.connector as sqlator
import random as rand
import sys

con = sqlator.connect(host='localhost', user='root',  password="Current-Root-Password", database='dvmtask1')  # starting a connection with mysql database
cursor = con.cursor()

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
        print('9. EXIT')
        print('_________________________________________________________________')
        print('\n', 'SELECT FROM 1-8')
        f = int(input("Enter your choice: "))
        if f == 1:
            createaccount()
        elif f == 2:
            deposit()
        elif f == 3:
            withdraw()
        elif f == 4:
            balance()
        elif f == 5:
            admin()
        elif f == 9:
            print('THANKS FOR VISITING BANK BY PI!')
            cursor.close()
            con.close()
            sys.exit
        else:
            Home()


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
    query7 = '''select exists (select * from accounts where account_no=%s)''' % (
        accno)  # checking whether the entered account exists or not
    quer7 = pd.read_sql(query7, con)
    gs = quer7.iat[0, 0]
    if gs == 1:  # if the entered account exists then we proceed
        print('PLEASE ENTER YOUR PINCODE:')
        pin = int(input())
        query1 = '''select pin from accounts where account_no=%s''' % (
            accno)  # checking whether the entered pin is correct or not
        quer1 = pd.read_sql(query1, con)
        gh = quer1.pin[0]
        if gh != pin:  # if the entered pin is not correct the loop reiterates
            print('please retry! wrong pin!')
        else:
            cursor = con.cursor()
            query2 = '''update accounts set balance=balance+%s where account_no=%s'''  # updating the balance after deposition
    inpu = (deposit, accno)
    cursor.execute(query2, inpu)
    con.commit()
    cursor.close()
    print(deposit, 'rupees deposited successfully!')
    query3 = '''select balance from accounts where account_no=%s''' % (accno)
    quer3 = pd.read_sql(query3, con)  # displaying the updated balance
    gh = quer3.balance[0]
    print('updated balance:', gh)


def withdraw():
    print('PLEASE ENTER THE AMOUNT YOU WANT TO WITHDRAW:')
    withdraw = int(input())
    print('PLEASE ENTER YOUR ACCOUNT NUMBER:')
    accno = int(input())
    query7 = '''select exists (select * from accounts where account_no=%s)''' % (
        accno)  # checking whether the entered account exists or not
    quer7 = pd.read_sql(query7, con)
    gs = quer7.iat[0, 0]
    query8 = '''select balance from accounts where account_no=%s''' % (accno)
    quer8 = pd.read_sql(query8, con)
    bb = quer8.iat[0, 0]
    if gs == 1:  # if the entered account exists then we proceed
        print('PLEASE ENTER YOUR PINCODE:')
        pin = int(input())
        query1 = '''select pin from accounts where account_no=%s''' % (accno)
        quer1 = pd.read_sql(query1, con)
        gh = quer1.pin[0]
        if gh != pin:  # checking whether the entered pin is correct or not
            print('please retry! wrong pin!')
        else:
            if bb > withdraw:
                cursor = con.cursor()
                query2 = '''update accounts set balance=balance-%s where account_no=%s'''
                inpu = (withdraw, accno)
                cursor.execute(query2, inpu)
                con.commit()
                cursor.close()
                print(withdraw, 'rupees withdrawn successfully!')
                query4 = '''select balance from accounts where account_no=%s''' % (accno)
                quer4 = pd.read_sql(query4, con)
                gh = quer4.balance[0]
                print('updated balance:', gh)  # displaying the updated balance
            else:
                print('insufficient funds!')
    else:
        print('please check your account number and try again.')
        Home()


def balance():
    print('PLEASE ENTER YOUR ACCOUNT NUMBER:')
    accno = int(input())
    query7 = '''select exists (select * from accounts where account_no=%s)''' % (accno)
    quer7 = pd.read_sql(query7, con)
    gs = quer7.iat[0, 0]
    if gs == 1:
        print('PLEASE ENTER YOUR PINCODE:')
        pin = int(input())
        query1 = '''select pin from accounts where account_no=%s''' % (accno)
        quer1 = pd.read_sql(query1, con)
        gh = quer1.pin[0]
        if gh != pin:
            print('please retry! wrong pin!')
        else:
            query4 = '''select balance from accounts where account_no=%s''' % (accno)
            quer4 = pd.read_sql(query4, con)
            gh = quer4.balance[0]
            print('Balance:', gh)
    else:
        print('please check your account number and try again.')


def admin():
    passwd = 'bankproject'
    print('PLEASE ENTER THE ADMIN PASSWORD TOO PROCEED:')
    pass1 = input()
    if pass1 == passwd:
        query5 = '''select account_no,aadhar_no,phone_no,email_id,address,savcurr from accounts'''
        quer5 = pd.read_sql(query5, con)
        print(quer5)
    else:
        print('WRONG PASSWORD! please try again.')

Home()