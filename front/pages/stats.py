import streamlit as st
import requests
import pandas as pd
import altair as alt
from config import get_settings


settings = get_settings()


st.set_page_config(page_title="Orders", page_icon="🛍️")
orders_response = requests.get(f"{settings.backend_url_admin}/stats")
data = orders_response.json()

col1, col2, col3 = st.columns(3)

with st.container():
    col1.metric(label="Total Orders", value=data["total_orders"])
    col2.metric(
        label="Total Revenue",
        value=f'${round(data["total_revenue"] if data["total_revenue"] else 0, 2):0.2f}',
    )
    col3.metric(
        label="Average Order Price",
        value=f'${round(data["average_order_price"] if data["average_order_price"] else 0, 2):0.2f}',
    )


col1, col2 = st.columns(2)

with col1:
    st.header("Upsell Stats")
    col1.metric(
        label="Total Upsell Revenue",
        value=f'${round(data["upsell_stats"]["total_upsell_revenue"] if data["upsell_stats"]["total_upsell_revenue"] else 0, 2):0.2f}',
    )
    st.bar_chart(
        {
            key.capitalize(): value
            for key, value in data["upsell_stats"].items()
            if key != "total_upsell_revenue"
        }
    )

items_df = pd.DataFrame(data["items"])

bar_chart = (
    alt.Chart(items_df)
    .mark_bar()
    .encode(
        x=alt.X("number_of_orders:Q", axis=alt.Axis(title="Number of Orders")),
        y=alt.Y("name:N", axis=alt.Axis(title="Item Name")),
    )
    .properties(width=500)
)
with col2:
    st.header("Items Stats")
    st.altair_chart(bar_chart)


def visualize_order(order):
    col1, col2, col3 = st.columns(3)

    with st.container():
        col1.metric(label="Id", value=order["id"])
        col2.metric(
            label="Total Price", value=f'${round(order["total_price"], 2):0.2f}'
        )

    items_df = pd.DataFrame(order["items"])

    bar_chart = (
        alt.Chart(items_df)
        .mark_bar()
        .encode(
            x=alt.X("number:Q", axis=alt.Axis(title="Number of Orders")),
            y=alt.Y("name:N", axis=alt.Axis(title="Item Name")),
        )
        .properties(width=300)
    )
    with col3:
        st.header("Order Items")
        st.altair_chart(bar_chart)

    with st.expander("Chat History"):
        for message in order["chat"]:
            st.write(f"- {message}")


st.title("Completed Orders:")
orders_response = requests.get(f"{settings.backend_url_admin}/orders")
data = orders_response.json()
if data:
    for order in data:
        visualize_order(order)
else:
    st.write("# There is no completed orders")
