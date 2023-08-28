import streamlit as st

def guest_page():
    st.title("Chat Interface")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if 'something' not in st.session_state:
        st.session_state.something = ''



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
    chat_log_element.markdown(f"<div class='chat-log'>{chat_log}</div>", unsafe_allow_html=True)



    def submit():
        handle_message(st.session_state.widget)
        st.session_state.something = st.session_state.widget
        st.session_state.widget = ''


    st.text_input(key='widget', on_change=submit, label = "user input", label_visibility="hidden", placeholder="type here")



    def handle_message(message):
        user_message = f"You: {message}"
        bot_response = generate_bot_response(message)

        st.session_state.messages.append(user_message)
        st.session_state.messages.append(bot_response)

        updated_chat_log = "<br>".join(st.session_state.messages)
        chat_log_element.markdown(f"<div class='chat-log'>{updated_chat_log}</div>", unsafe_allow_html=True)

def generate_bot_response(user_input):
    return "Bot response to " + user_input

if __name__ == "__main__":
    guest_page()
