import requests
import streamlit as st
from config import get_settings

from models import Menu_item

settings = get_settings()


def add_item():
    st.header("Add Menu Item")
    name = st.text_input("Name")
    type = st.selectbox("Type", ["Dish", "Drink"])
    price = st.number_input("Price", value=0.0)
    in_stock = st.number_input("In Stock", value=0, min_value=0, step=1)

    if st.button("Add Item"):
        item = Menu_item(name=name, type=type, price=price, in_stock=in_stock)
        response = requests.post(
            f"{settings.backend_url_admin}/add_menu_item", json=item.dict()
        )
        if response.status_code == 200:
            st.success("Menu item added successfully!")
        else:
            st.error("Failed to add menu item.")
