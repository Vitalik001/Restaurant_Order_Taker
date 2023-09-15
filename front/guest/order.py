import streamlit as st
import requests
from config import get_settings


settings = get_settings()


class Order:
    chat_log = None
    chat_log_element = None

    def __init__(self):
        st.title("Chat bot")
        self.initialize_chat_session()
        self.display_chat_log()

        st.text_input(
            key="widget",
            on_change=self.submit,
            label="user input",
            label_visibility="hidden",
            placeholder="type here",
        )

    def initialize_chat_session(self):
        if "session_id" not in st.session_state:
            response = requests.post(settings.backend_url + "/create_session")
            session = response.json()
            session_id = session["order_id"]
            message = session["message"]
            st.session_state.session_id = session_id
            st.session_state.messages = [message]

        if "something" not in st.session_state:
            st.session_state.something = ""

    def display_chat_log(self):
        chat_style = """
            <style>
                .chat-log {
                    height: 300px;
                    overflow-y: auto;
                    display: flex;
                    flex-direction: column-reverse;
                }
            </style>
        """
        st.markdown(chat_style, unsafe_allow_html=True)

        self.chat_log = "<br>".join(st.session_state.messages)
        self.chat_log_element = (
            st.empty()
        )  # Create an empty element to update the chat log
        self.chat_log_element.markdown(
            f"<div class='chat-log'>{self.chat_log}</div>", unsafe_allow_html=True
        )

    # actions that a made after user sends message
    def submit(self):
        self.handle_message(st.session_state.widget)
        st.session_state.something = st.session_state.widget

        st.session_state.widget = ""

    # handle user message(visualize and generate response)
    def handle_message(self, message):
        user_message = f"You: -{message}"
        bot_response = self.generate_bot_response(message)

        st.session_state.messages.append(user_message)
        st.session_state.messages.append(bot_response)

        updated_chat_log = "<br>".join(st.session_state.messages)
        self.chat_log_element.markdown(
            f"<div class='chat-log'>{updated_chat_log}</div>", unsafe_allow_html=True
        )

    def generate_bot_response(self, user_input):
        data = {"message": user_input}
        response = requests.post(
            settings.backend_url + f"/send_message/{st.session_state.session_id}",
            params=data,
            headers={"Content-Type": "application/json"},
        )
        return f"Restaurant: {response.json()['message']}"
