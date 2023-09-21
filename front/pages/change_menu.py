import streamlit as st

from pydantic import BaseModel
import requests

from config import get_settings


settings = get_settings()


st.set_page_config(page_title="change menu", page_icon="👨🏽‍🍳",)


# Define the Menu_item model
class Menu_item(BaseModel):
    name: str
    type: str
    price: float
    in_stock: int

# Define the Streamlit app
st.title("Admin Dashboard")

# Sidebar menu
selected_option = st.sidebar.radio("Select an Option", ("Add Menu Item", "Change Stock", "Get Menu"))

if selected_option == "Add Menu Item":
    st.header("Add Menu Item")
    # Input fields for adding menu items
    name = st.text_input("Name")
    type = st.selectbox("Type", ["Dish", "Drink"])
    price = st.number_input("Price", value=0.0)
    in_stock = st.number_input("In Stock", value=0, min_value=0, step=1)

    if st.button("Add Item"):
        item = Menu_item(name=name, type=type, price=price, in_stock=in_stock)
        response = requests.post(f"{settings.backend_url_admin}/add_menu_item", json=item.dict())
        if response.status_code == 200:
            st.success("Menu item added successfully!")
        else:
            st.error("Failed to add menu item.")

elif selected_option == "Change Stock":
    st.header("Change Stock")
    # Input fields for changing stock
    item_id = st.number_input("Item ID", value = 0)
    in_stock = st.number_input("New Stock Value", value=0)

    if st.button("Change Stock"):
        response = requests.put(f"{settings.backend_url_admin}/change_stock/{item_id}", params={"in_stock": in_stock})
        if response.status_code == 200:
            st.success("Stock updated successfully!")
        else:
            st.error("Failed to update stock.")

elif selected_option == "Get Menu":
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
            formatted_menu_data.append({"id": id, "name": name, "type":typ, "price": formatted_price, "in stock": in_stock})

        st.table(formatted_menu_data)

    else:
        st.error("Failed to retrieve menu.")

