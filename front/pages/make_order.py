import streamlit as st
from streamlit_chat import message
import requests
from config import get_settings

settings = get_settings()

st.set_page_config(page_title="Make Order", page_icon="🛎️")

st.header("Restaurant Chat Bot")

if "session" not in st.session_state:
    response = requests.post(settings.backend_url_guest + "/create_session")
    st.session_state.session = response.json()
    st.session_state.generated = []
    st.session_state["past"] = [""]

with st.sidebar:
    st.markdown("***Possible messages:***")
    st.markdown("- **I'd like a(an) X.**")
    st.markdown("- **I don't want a(an) X.**")
    st.markdown("- **That's all.**")
    st.markdown("- **Yes, please.**")
    st.markdown("- **No, thank you.**")


def query(payload):
    data = {"message": payload}
    response = requests.post(
        settings.backend_url_guest
        + f"/send_message/{st.session_state.session['order_id']}",
        params=data,
        headers={"Content-Type": "application/json"},
    )

    return response.json()["message"]


with st.form("user_input_form", clear_on_submit=True):
    st.session_state.user_input = st.text_input(
        disabled=False,
        key="text",
        label="user input",
        label_visibility="hidden",
        placeholder="type here",
        max_chars=30,
    )

    submit_button = st.form_submit_button(label="Submit")

if not st.session_state.generated:
    st.session_state.generated.append(
        f"Restaurant: - {st.session_state.session['message']}"
    )

if st.session_state.user_input:
    output = query(st.session_state.user_input)
    st.session_state.past.append(f"You: - {st.session_state.user_input}")
    st.session_state.generated.append(f"Restaurant: - {output}")

if st.session_state["past"]:
    message(st.session_state["generated"][-1], key=str(-1))
    for i in range(len(st.session_state["past"]) - 2, -1, -1):
        message(
            st.session_state["past"][i + 1],
            is_user=True,
            key=str(i) + "_user",
        )
        message(st.session_state["generated"][i], key=str(i))
