import streamlit as st
import requests
from config import get_settings

settings = get_settings()

class Order:

    order = {}
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
        if "messages" not in st.session_state:
            st.session_state.messages = ["Bot: - Welcome, what can I get you?"]

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
        self.chat_log_element = st.empty()  # Create an empty element to update the chat log
        self.chat_log_element.markdown(
            f"<div class='chat-log'>{self.chat_log}</div>", unsafe_allow_html=True
        )

    def submit(self):
        self.handle_message(st.session_state.widget)
        st.session_state.something = st.session_state.widget
        st.session_state.widget = ""

    def handle_message(self, message):
        user_message = f"You: {message}"
        bot_response = self.generate_bot_response(message)

        st.session_state.messages.append(user_message)
        st.session_state.messages.append(bot_response)

        updated_chat_log = "<br>".join(st.session_state.messages)
        self.chat_log_element.markdown(
            f"<div class='chat-log'>{updated_chat_log}</div>", unsafe_allow_html=True
    )


    def generate_bot_response(self, user_input):
        if user_input == "I'd like an americano.":
            return "Bot: - Would you like to add a muffin for $0.70?"
        elif user_input == "Yes, please.":
            return "Bot: - Would you like anything else?"
        elif user_input == "That's all.":
            return "Bot: - Your total is $2.84. Thank you and have a nice day!"
        return "Bot: - I don't understand"

    def send_order_to_api(self):
        response = requests.post(settings.backend_url, data=self.order)

        if response.status_code == 200:
            print("POST request successful")
            response_data = response.json()  # If the response contains JSON data
            print(response_data)
        else:
            print("POST request failed")



if __name__ == "__main__":
    Order()
