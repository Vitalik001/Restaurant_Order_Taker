import streamlit as st
import requests

from config import get_settings


settings = get_settings()

st.set_page_config(
    page_title="Menu",
    page_icon="👋",
)

st.write("# Welcome to our Restaurant! 👋")
response = requests.get(f"{settings.backend_url}/menu")

menu = response.json()

st.write("MENU:")
st.table(menu)
