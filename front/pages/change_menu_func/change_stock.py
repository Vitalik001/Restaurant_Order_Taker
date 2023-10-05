import requests
import streamlit as st
from config import get_settings

settings = get_settings()


def change_stock():
    st.header("Change Stock")
    item_id = st.number_input("Item ID", value=0)
    in_stock = st.number_input("New Stock Value", value=0)

    if st.button("Change Stock"):
        response = requests.put(
            f"{settings.backend_url_admin}/change_stock/{item_id}",
            params={"in_stock": in_stock},
        )
        if response.status_code == 200:
            st.success("Stock updated successfully!")
        else:
            st.error("Failed to update stock.")
