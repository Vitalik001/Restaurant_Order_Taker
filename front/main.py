from guest.guest import guest_page
from admin.admin import admin_page

import streamlit as st


def order():
    upper_bar = st.container()
    with upper_bar:
        st.title("Seafood place")

        st.markdown(
            "<style>div.row-widget.stRadio>div{flex-direction: row;}</style>",
            unsafe_allow_html=True,
        )

        page = st.radio(
            options=["Guest Page", "Admin Page"],
            label="Page Choice",
            format_func=lambda x: x,
            label_visibility="hidden",
        )

        if page == "Admin Page":
            admin_page()
        elif page == "Guest Page":
            guest_page()


if __name__ == "__main__":
    order()
