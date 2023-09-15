import streamlit as st
import requests
import matplotlib.pyplot as plt
import pandas as pd
BACKEND_URL = "http://app:80/admin"

st.set_page_config(page_title="Orders", page_icon="🛍️")
orders_response = requests.get(f"{BACKEND_URL}/stats")
data = orders_response.json()
st.title("Item Orders Visualization")
item_names = [item["name"] for item in data["items"]]
number_of_orders = [item["number_of_orders"] for item in data["items"]]
# Create a bar chart
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(item_names, number_of_orders)

# Add total orders, total revenue, and average order price to the legend
legend_text = (
    f"Total Orders: {data['total_orders']}\n"
    f"Total Revenue: ${data['total_revenue']:.2f}\n"
    f"Average Order Price: ${data['average_order_price']:.3f}"
)
ax.legend([legend_text], loc="upper left")

# Display the bar chart
st.pyplot(fig)

st.title("Order Visualization")
orders_response = requests.get(f"{BACKEND_URL}/orders")
data = orders_response.json()
# Display information for each order
for order in data:
    st.subheader(f"Order ID: {order['id']}")
    st.write(f"Total Price: ${order['total_price']:.2f}")

    # Visualize items using a bar chart
    items_df = pd.DataFrame(order["items"])
    fig, ax = plt.subplots()
    items_df["name"] = items_df["name"].apply(lambda x: str(x) if x is not None else "None")
    items_df["number"] = items_df["number"].apply(lambda x: int(x) if x is not None else 0)
    ax.bar(items_df["name"], items_df["number"])
    plt.xlabel("Item Name")
    plt.ylabel("Number")
    plt.title("Items")
    st.pyplot(fig)

    # Display chat messages
    st.subheader("Chat Messages:")
    for message in order["chat"]:
        st.write(message)

    # Add a horizontal line for separation
    st.markdown("---")

