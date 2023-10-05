import requests
import streamlit as st
from config import get_settings

settings = get_settings()


def get_menu():
    st.header("Menu")
    response = requests.get(f"{settings.backend_url_admin}/get_menu")
    if response.status_code == 200:
        menu = response.json()

        formatted_menu_data = []
        for item in menu:
            id = item["id"]
            name = item["name"]
            typ = item["type"]
            price = item["price"]
            formatted_price = f"${price:.2f}"
            in_stock = item["in_stock"]
            formatted_menu_data.append(
                {
                    "id": id,
                    "name": name,
                    "type": typ,
                    "price": formatted_price,
                    "in stock": in_stock,
                }
            )

        st.table(formatted_menu_data)
    else:
        st.error("Failed to retrieve menu.")
