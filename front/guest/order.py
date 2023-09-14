import json

import streamlit as st
import requests
from config import get_settings
import re



settings = get_settings()

class Order:

    order = dict()
    chat_log = None
    chat_log_element = None
    upsell = None
    upsell_recommended = False

    def __init__(self):
        st.title("Chat bot")
        self.initialize_chat_session()

        response = requests.get(f"{settings.backend_url}/upsell")
        if response.status_code == 200:
            self.upsell = response.json()[0]
        else:
            st.error("Error getting upsell")

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
            st.session_state.messages = [f"Bot: - Welcome, what can I get you?"]

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

    # actions that a made after user sends message
    def submit(self):
        self.handle_message(st.session_state.widget)
        st.session_state.something = st.session_state.widget
        if st.session_state.widget == "That's all":
            del self

        st.session_state.widget = ""

    # handle user message(visualize and generate response)
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
        if match:=re.match(r"^i'd like (an? )?(.+)$", user_input, re.IGNORECASE):
            item_name = match.group(2)
            if id:=self.check_item(item_name):
                self.order[id] = self.order.setdefault(id, 0) + 1

                # if selected item is an upsell do not recommend it
                if id == self.upsell['id']:
                    self.upsell_recommended = True

                # if upsell was not recommend, recommend it
                if not self.upsell_recommended:
                    self.upsell_recommended = True
                    return f"Bot: - Would you like to add a {self.upsell['name']} for ${self.upsell['price']}?"

                return "Bot: - Would you like anything else?"

        elif re.match(r"yes, please$", user_input, re.IGNORECASE):
            self.order[self.upsell['id']] = 1
            return "Bot: - Would you like anything else?"

        elif re.match(r"no, thank you$", user_input, re.IGNORECASE):
            return "Bot: - Would you like anything else?"

        elif match:=re.match(r"i don't want (an? )?(.+)$", user_input, re.IGNORECASE):
            item_name = match.group(2)
            if id:=self.check_item(item_name):
                self.order.pop(id)
                return "Bot: - Would you like anything else?"


        elif user_input == "That's all":
            return self.add_order()

        return "Bot: - I don't understand"

    def add_order(self):

        json_data = [
            {"item_id": item_id, "number_of_items": number_of_items}
            for item_id, number_of_items in self.order.items()
        ]

        json_payload = json.dumps(json_data)

        headers = {"Content-Type": "application/json"}

        url = f"{settings.backend_url}/order"
        response = requests.post(url, data=json_payload, headers=headers)
        order = response.json()
        return f"Bot: - Your total is ${order[0]['total_price']}. Thank you and have a nice day!"


    def check_item(self, item_name: str):
        response = requests.get(settings.backend_url + "/check_item", params = {"item_name": item_name})
        result = response.json()
        return result[0]["id"] if result else None

if __name__ == "__main__":
    Order()