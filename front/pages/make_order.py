import streamlit as st
from streamlit_chat import message
import requests
from config import get_settings
import re

settings = get_settings()

st.set_page_config(page_title="Make Order", page_icon="🛎️")

st.header("Restaurant Chat Bot")

if "session" not in st.session_state:
    response = requests.post(settings.backend_url_guest + "/create_session")
    st.session_state.session = response.json()
    st.session_state.generated = []
    st.session_state["past"] = [""]
    st.session_state["disabled"] = False

with st.expander("Help"):
    st.markdown("The guest agent can say any of the following messages:")
    st.markdown(
        "- **I'd like a(an) X.**: This is said when the guest wants to order a specific item on the menu."
    )
    st.markdown(
        "- **I don't want a(an) X.**: This is said when the guest changes their mind about a previously ordered item."
    )
    st.markdown(
        "- **That's all.**: This is said after the guest has finished ordering."
    )
    st.markdown(
        "- **Yes, please.**: This is said when the guest wants to accept the upsell."
    )
    st.markdown(
        "- **No, thank you.**: This is said when the guest wants to reject the upsell."
    )


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
        disabled=st.session_state.disabled,
        key="text",
        label="user input",
        label_visibility="hidden",
        placeholder="type here",
        max_chars=20,
    )

    submit_button = st.form_submit_button(label="Submit")

if not st.session_state.generated:
    st.session_state.generated.append(
        f"Restaurant: - {st.session_state.session['message']}"
    )

if (
    st.session_state.user_input
    and not re.match(r"^that's all(\.?)$", st.session_state.user_input, re.IGNORECASE)
):
    output = query(st.session_state.user_input)
    st.session_state.past.append(f"You: - {st.session_state.user_input}")
    st.session_state.generated.append(f"Restaurant: - {output}")
elif st.session_state.user_input:
    st.session_state.disabled = True

if st.session_state["past"]:
    message(st.session_state["generated"][-1], key=str(-1))
    for i in range(len(st.session_state["past"]) - 2, -1, -1):
        message(
            st.session_state["past"][i + 1],
            is_user=True,
            key=str(i) + "_user",
        )
        message(st.session_state["generated"][i], key=str(i))
