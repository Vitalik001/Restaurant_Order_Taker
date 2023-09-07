import streamlit as st
import requests
from config import get_settings
import re

settings = get_settings()

class Order:

    order = {}
    chat_log = None
    chat_log_element = None
    upsell = None
    upsell_recommended = False

    def __init__(self):
        st.title("Chat bot")
        self.initialize_chat_session()
        self.upsell = requests.get(settings.backend_url + "/upsell")
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
        if match:=re.match(r"^i'd like an (.+)$", user_input, re.IGNORECASE):
            item_name = match.group(1)
            if id:=self.check_item(item_name):
                self.order[id] = self.order.setdefault(id, 0) + 1

                # if selected item is an upsell do not recommend it
                if id == self.upsell.id:
                    self.upsell_recommended = True

                # if upsell was not recommend, recommend it
                if not self.upsell_recommended:
                    self.upsell_recommended = True
                    self.suggest_uppsell()

                return "Bot: - Would you like anything else?"

            return "Bot: - I don't understand"

        elif user_input == "That's all.":
            self.add_order()

        return "Bot: - I don't understand"

    def add_order(self):
        return "Bot: - Your total is $2.84. Thank you and have a nice day!"


    def suggest_uppsell(self):
        # elif user_input == "Yes, please.":
        #     return "Bot: - Would you like anything else?"
        return "Bot: - Would you like to add a muffin for $0.70?"

    def check_item(self, item_name: str):
        print(item_name)
        response = requests.get(settings.backend_url + "/check_item", params = {"item_name": item_name})
        return response

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
