import streamlit as st
import requests
from config import get_settings


settings = get_settings()


def initialize_chat_session():
    if "session_id" not in st.session_state:
        response = requests.post(settings.backend_url + "/create_session")
        session = response.json()
        session_id = session["order_id"]
        message = session["message"]
        st.session_state.session_id = session_id
        st.session_state.messages = [f"Restaurant: - {message}"]

    if "something" not in st.session_state:
        st.session_state.something = ""

    if "chat_log" not in st.session_state:
        st.session_state.chat_log = None

    if "chat_log_element" not in st.session_state:
        st.session_state.chat_log_element = None

def display_chat_log():
    chat_style = """
        <style>
            .chat-log {
                height: 500px;
                overflow-y: auto;
                display: flex;
                flex-direction: column-reverse;
            }
            .css-1y4p8pa {
            width: 100%;
            padding: 6rem 1rem 3rem;
            max-width: 46rem;
            }
        </style>
    """
    st.markdown(chat_style, unsafe_allow_html=True)

    st.session_state.chat_log = "<br>".join(st.session_state.messages)
    st.session_state.chat_log_element = (
        st.empty()
    )  # Create an empty element to update the chat log
    st.session_state.chat_log_element.markdown(
        f"<div class='chat-log'>{st.session_state.chat_log}</div>", unsafe_allow_html=True
    )

    # actions that a made after user sends message
def submit():
    handle_message(st.session_state.widget)
    st.session_state.something = st.session_state.widget

    st.session_state.widget = ""

# handle user message(visualize and generate response)
def handle_message(message):
    user_message = f"You: - {message}"
    bot_response = generate_bot_response(message)

    st.session_state.messages.append(user_message)
    st.session_state.messages.append(bot_response)

    updated_chat_log = "<br>".join(st.session_state.messages)
    st.session_state.chat_log_element.markdown(
        f"<div class='chat-log'>{updated_chat_log}</div>", unsafe_allow_html=True
    )

def generate_bot_response(user_input):
    data = {"message": user_input}
    response = requests.post(
        settings.backend_url + f"/send_message/{st.session_state.session_id}",
        params=data,
        headers={"Content-Type": "application/json"},
    )
    return f"Restaurant: - {response.json()['message']}"

st.set_page_config(page_title="Make Order", page_icon="🛎️")

st.write(" # Restaurant chat bot ")
initialize_chat_session()
display_chat_log()

st.text_input(
    key="widget",
    on_change=submit,
    label="user input",
    label_visibility="hidden",
    placeholder="type here",
)