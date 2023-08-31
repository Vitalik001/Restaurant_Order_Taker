import requests
import streamlit as st

from config import get_settings


settings = get_settings()
def show_menu():
    response = requests.get(f"{settings.backend_url}/menu")
    if response.status_code == 200:
        menu = response.json()

        st.write("MENU:")
        st.table(menu)
    else:
        st.error("Error getting menu")