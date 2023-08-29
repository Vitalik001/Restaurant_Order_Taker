import streamlit as st
import requests

BACKEND_URL = "http://app:80"

def admin_page():
    st.title("Admin page")
    st.title("General statistics:")

    # Make a request to the admin/orders endpoint
    orders_response = requests.get(f"{BACKEND_URL}/admin/orders")

    if orders_response.status_code == 200:
        orders_data = orders_response.json()
        st.header("Orders:")
        st.table(orders_data)
    else:
        st.write("Failed to fetch orders data")

if __name__ == "__main__":
    admin_page()
