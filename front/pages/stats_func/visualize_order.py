import streamlit as st
import pandas as pd
import altair as alt


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
        for idx, message in enumerate(order["chat"]):
            if idx % 2 == 0:
                st.markdown(f"**Bot: - {message}**")
            else:
                st.markdown(f"**Guest: - {message}**")
