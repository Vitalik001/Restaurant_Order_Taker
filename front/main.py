import streamlit as st
import requests

BACKEND_URL = "http://app:80"


def show_menu():
    response = requests.get(f"{BACKEND_URL}/guest/menu")
    if response.status_code == 200:
        menu = response.json()

        st.write("MENU:")
        st.table(menu)
    else:
        st.error("Error getting menu")

def make_order():

    st.title("Making order")

    st.text("Restaurant: Welcome! What can I get you?")

    user_input = st.text_input("You:", "")
    if "add" in user_input:
        st.text("Would you like anything else?")
    elif "remove" in user_input:
        st.text("Would you like anything else?")

def main():
    st.title("Welcome to our restaurant")

    options = ["menu", "order"]
    selected_option = st.selectbox("Select an option", options)

    if selected_option == "menu":
        show_menu()
    elif selected_option == "order":
        make_order()

if __name__ == "__main__":
    main()
