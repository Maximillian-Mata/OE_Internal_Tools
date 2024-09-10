import streamlit as st
from nav import Navbar
from db_set import Fetch_User
from db_set import Check_Approved
from db_set import Insert_User

#Globals

register1 = st.empty()

register2 = st.empty()


def check_password():
    """Returns `True` if the user had a correct password."""

    def login_form():
        """Form with widgets to collect user information"""
        register = st.toggle("New User?")
        if register:
            with register1.form("Verify"):
                st.write("Please input your OE username to see if you are on the list of approved users.")
                st.text_input("OE Username", type="default", key="username")
                st.form_submit_button("Verify", on_click=Check_Approved(st.session_state.username))
            if Check_Approved(st.session_state.username):
                with register2.form("Registration"):
                    st.text_input("Name", type="default", key="name")
                    st.text_input("Password", type="password", key="password")
                    st.text_input("Password Again", type="password", key="password2")
                    st.form_submit_button("Register", on_click=register_new)
 
            else:
                if st.session_state.username != "":
                    st.error("Not an approved Username")
                
        else:
            with st.form("Credentials"):
                st.write("Please login to use the tools")
                st.text_input("Username", type="default", key="username")
                st.text_input("Password", type="password", key="password")
                st.form_submit_button("Log in", on_click=password_entered)
            
    
    def register_new():
        Name = st.session_state.name
        Username = st.session_state.username
        pwd = st.session_state.password
        pwd2 = st.session_state.password2
        if (Name == "" or pwd != pwd2 or pwd == ""):
            st.error("Invalid entries")
        else:
            Insert_User(Name, Username, pwd)
            st.info(f"Welcome {Name}. Please refresh the page and login to begin using the tools")
        return

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        
        User = Fetch_User(pwd = st.session_state["password"], username = st.session_state["username"]) 
        if User is not None:
            st.session_state["password_correct"] = True           
            del st.session_state["password"]  # Don't store the username or password.
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False


    # Return True if the username + password is validated.
    if st.session_state.get("password_correct", False):
        return True


    # Show inputs for username + password.
    login_form()
    if "password_correct" in st.session_state:
        st.error("😕 User not known or password incorrect")
    return False


if not check_password():
    st.stop()


Navbar()
st.title("OE Internal Tools")
#if not check_password():
    #st.stop()

st.write("Welcome to the OE Internal Tools page!")

#st.sidebar()