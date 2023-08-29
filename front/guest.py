import requests
import streamlit as st

BACKEND_URL = "http://app:80"


def guest_page():
    st.title("Welcome to our restaurant!")

    options = ["menu", "make order"]
    selected_option = st.selectbox("Select an option", options)
    if selected_option == "make order":
        make_order()
    else:
        show_menu()


def show_menu():
    response = requests.get(f"{BACKEND_URL}/guest/menu")
    if response.status_code == 200:
        menu = response.json()

        st.write("MENU:")
        st.table(menu)
    else:
        st.error("Error getting menu")


def make_order():
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
        bot_response = generate_bot_response(message)

        st.session_state.messages.append(user_message)
        st.session_state.messages.append(bot_response)

        updated_chat_log = "<br>".join(st.session_state.messages)
        chat_log_element.markdown(
            f"<div class='chat-log'>{updated_chat_log}</div>", unsafe_allow_html=True
        )


def generate_bot_response(user_input):
    if user_input == "I'd like an americano.":
        return "Bot: - Would you like to add a muffin for $0.70?"
    if user_input == "Yes, please.":
        return "Bot: - Would you like anything else?"
    if user_input == "That's all.":
        return "Bot: - Your total is $2.84. Thank you and have a nice day!"
    return "Bot: - I don't understand"


if __name__ == "__main__":
    guest_page()
