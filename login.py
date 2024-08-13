import streamlit as st
from db import create_table, insert_user, verify_credentials
from Validation import validate_email, validate_password
from Dashboard import render_dashboard

class SessionState:
    def __init__(self):
        self.is_authenticated = False
        self.successful_login = False
        self.successful_signup = False

def main():
    create_table()
    session_state = get_session_state()

    if session_state.is_authenticated:
        render_dashboard(session_state)
    elif session_state.successful_signup:
        render_login_page(session_state)
    elif 'signup_mode' in st.session_state and st.session_state.signup_mode:
        render_signup_page(session_state)
    else:
        render_login_page(session_state)

def get_session_state():
    if 'session_state' not in st.session_state:
        st.session_state['session_state'] = SessionState()
    return st.session_state['session_state']

def render_login_page(session_state):
    st.title("Bank Loan Prediction")
    st.title("Login")
    with st.container():
        col1, _ = st.columns([2, 1])

        username = col1.text_input("Username")
        password = col1.text_input("Password", type="password")
        login_button = col1.button("Login")
        signup_button = col1.button("Go to Sign Up", key="signup_button")

        if login_button:
            if verify_credentials(username, password):
                session_state.is_authenticated = True
                session_state.successful_login = True
                st.experimental_rerun()
            else:
                st.error("Invalid username or password. Please check your credentials.")

        if signup_button:
            st.session_state.signup_mode = True
            st.experimental_rerun()

def render_signup_page(session_state):
    st.title("Bank Loan Prediction")
    st.title("Sign Up")
    with st.container():
        col1, _ = st.columns([2, 1])

        new_username = col1.text_input("Username", key="new_username")
        new_password = col1.text_input("New Password", type="password", key="new_password")
        confirm_password = col1.text_input("Confirm Password", type="password", key="confirm_password")
        signup_button = col1.button("Sign Up", key="signup_button_2")
        back_to_login_button = col1.button("Back to Login", key="back_to_login_button")

        if signup_button:
            if validate_email(new_username) and validate_password(new_password) and new_password == confirm_password:
                if insert_user(new_username, new_password):
                    session_state.successful_signup = True
                    st.success("Successfully signed up! Please log in.")
                    st.session_state.signup_mode = False
                    st.experimental_rerun()
                else:
                    st.error("Username already exists. Please choose a different username.")
            else:
                if not validate_email(new_username):
                    st.error("Invalid email format. Please enter a valid email address.")
                elif not validate_password(new_password):
                    st.error("Invalid password format. Please make sure the password meets the requirements.")
                else:
                    st.error("Passwords do not match. Please make sure the passwords match.")

        if back_to_login_button:
            st.session_state.signup_mode = False
            st.experimental_rerun()

if __name__ == '__main__':
    main()
