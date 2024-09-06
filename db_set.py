import sqlite3
import streamlit as st
from cryptography.fernet import Fernet


#Encryption Stuff

def Load_Key():
    return st.secrets.Key

def Encrypt(data, f):
    return f.encrypt(data.encode())

def Decrypt(data, f):
    return f.decrypt(data).decode()

# Database Stuff

## Only Use once
def Init_DB():
    connection = sqlite3.connect("OE_Users.db")
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTs users(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   username TEXT NOT NULL,
                   pwd BLOB NOT NULL
                   )
''')
    connection.commit()
    connection.close()

## Only Use once
def Init_approved():
    connection = sqlite3.connect("OE_Users.db")
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTs approved_users(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   username BLOB NOT NULL
                   )
''')
    connection.commit()
    connection.close()

def Add_Approved(username):
    f = Fernet(Load_Key())
    encrypted_name = Encrypt(username,f)
    connection = sqlite3.connect("OE_Users.db")
    cursor = connection.cursor()
    cursor.execute('''
    INSERT INTO approved_users (username) VALUES (?)
''', ((encrypted_name,)))
    connection.commit()
    connection.close()

def Check_Approved(username):
    f = Fernet(Load_Key())
    connection = sqlite3.connect("OE_Users.db")
    cursor = connection.cursor()
    cursor.execute('''
    SELECT username FROM approved_users
''')
    Users = cursor.fetchall()
    connection.commit()
    connection.close()
    for i in Users:
        if Decrypt(i[0],f) == username:
            return True


def View_Approved():
    f = Fernet(Load_Key())
    connection = sqlite3.connect("OE_Users.db")
    cursor = connection.cursor()
    cursor.execute('''
        SELECT username FROM approved_users
''')
    Approved = cursor.fetchall()
    connection.commit()
    connection.close()
    for i in Approved:
        print(Decrypt(i[0],f))


def Insert_User(name, username, pwd):
    f = Fernet(Load_Key())
    encryptedpwd = Encrypt(pwd, f)
    connection = sqlite3.connect("OE_Users.db")
    cursor = connection.cursor()
    cursor.execute('''
    INSERT INTO users (name, username, pwd) VALUES (?,?,?)
''', (name, username, encryptedpwd))
    connection.commit()
    connection.close()

def Fetch_User(pwd,username):
    f = Fernet(Load_Key())
    connection = sqlite3.connect("OE_Users.db")
    cursor = connection.cursor()
    cursor.execute('''
    SELECT * FROM users WHERE username = ?
''',(username,))
    Desired_User = cursor.fetchall()
    connection.commit()
    connection.close()
    for i in Desired_User:
        if Decrypt(i[3],f) == pwd:
            return Desired_User
    return None

def Fetch_ALL():
    f = Fernet(Load_Key())
    connection = sqlite3.connect("OE_Users.db")
    cursor = connection.cursor()
    cursor.execute('''
    SELECT * FROM users
''')
    All_Users = cursor.fetchall()
    connection.commit()
    connection.close()
    return All_Users

def Fetch_Name(username):
    connection = sqlite3.connect("OE_Users.db")
    cursor = connection.cursor()
    cursor.execute('''
    SELECT name FROM users WHERE username = ?
''', (username,))
    All_Users = cursor.fetchall()
    connection.commit()
    connection.close()
    return All_Users[1]


def Delete_User(username):
    connection = sqlite3.connect("OE_Users.db")
    cursor = connection.cursor()
    cursor.execute('''
    DELETE FROM users WHERE username = ?
''', (username,))
    connection.commit()
    connection.close()
    return 
