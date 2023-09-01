import streamlit as st
from .menu import show_menu
from .order import Order
def guest_page():
    st.title("Welcome to our restaurant!")
    options = ["menu", "make order"]
    selected_option = st.selectbox("Select an option", options)
    if selected_option == "make order":
        Order()
    else:
        show_menu()


if __name__ == "__main__":
    guest_page()
