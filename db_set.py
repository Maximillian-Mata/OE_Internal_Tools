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
