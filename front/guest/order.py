import streamlit as st
import requests


from config import get_settings


settings = get_settings()

# response = requests.get(f"{settings.backend_url}/menu")
def make_order(order):
    st.title("Chat bot")

    if "messages" not in st.session_state:
        st.session_state.messages = ["Bot: - Welcome, what can I get you?"]

    if "something" not in st.session_state:
        st.session_state.something = ""

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

    # Display the chat log
    chat_log = "<br>".join(st.session_state.messages)
    chat_log_element = st.empty()  # Create an empty element to update the chat log
    chat_log_element.markdown(
        f"<div class='chat-log'>{chat_log}</div>", unsafe_allow_html=True
    )

    def submit():
        handle_message(st.session_state.widget)
        st.session_state.something = st.session_state.widget
        st.session_state.widget = ""

    st.text_input(
        key="widget",
        on_change=submit,
        label="user input",
        label_visibility="hidden",
        placeholder="type here",
    )

    def handle_message(message):
        user_message = f"You: {message}"
        bot_response = generate_bot_response(message, order)

        st.session_state.messages.append(user_message)
        st.session_state.messages.append(bot_response)

        updated_chat_log = "<br>".join(st.session_state.messages)
        chat_log_element.markdown(
            f"<div class='chat-log'>{updated_chat_log}</div>", unsafe_allow_html=True
        )


def generate_bot_response(user_input, order):
    if user_input == "I'd like an americano.":
        # check_item(user_input.split(" ")[-1])
        return "Bot: - Would you like to add a muffin for $0.70?"
    if user_input == "Yes, please.":
        return "Bot: - Would you like anything else?"
    if user_input == "That's all.":
        # process_order(order)
        return "Bot: - Your total is $2.84. Thank you and have a nice day!"
    return "Bot: - I don't understand"



def process_order(order):
    response = requests.post(settings.backend_url, data=order)

    if response.status_code == 200:
        print("POST request successful")
        response_data = response.json()  # If the response contains JSON data
        print(response_data)
    else:
        print("POST request failed")