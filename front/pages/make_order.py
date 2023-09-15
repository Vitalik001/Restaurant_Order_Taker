# import streamlit as st
# import requests
# from config import get_settings
#
#
# settings = get_settings()
#
#
# def initialize_chat_session():
#     if "session_id" not in st.session_state:
#         response = requests.post(settings.backend_url_guest + "/create_session")
#         session = response.json()
#         session_id = session["order_id"]
#         message = session["message"]
#         st.session_state.session_id = session_id
#         st.session_state.messages = [f"Restaurant: - {message}"]
#
#     if "something" not in st.session_state:
#         st.session_state.something = ""
#
#     if "chat_log" not in st.session_state:
#         st.session_state.chat_log = None
#
#     if "chat_log_element" not in st.session_state:
#         st.session_state.chat_log_element = None
#
#
# def display_chat_log():
#     chat_style = """
#         <style>
#             .chat-log {
#                 height: 500px;
#                 overflow-y: auto;
#                 display: flex;
#                 flex-direction: column-reverse;
#             }
#             .css-1y4p8pa {
#             width: 100%;
#             padding: 6rem 1rem 3rem;
#             max-width: 46rem;
#             }
#         </style>
#     """
#     st.markdown(chat_style, unsafe_allow_html=True)
#
#     st.session_state.chat_log = "<br>".join(st.session_state.messages)
#     st.session_state.chat_log_element = (
#         st.empty()
#     )  # Create an empty element to update the chat log
#     st.session_state.chat_log_element.markdown(
#         f"<div class='chat-log'>{st.session_state.chat_log}</div>",
#         unsafe_allow_html=True,
#     )
#
#     # actions that a made after user sends message
#
#
# def submit():
#     handle_message(st.session_state.widget)
#     st.session_state.something = st.session_state.widget
#
#     st.session_state.widget = ""
#
#
# # handle user message(visualize and generate response)
# def handle_message(message):
#     user_message = f"You: - {message}"
#     bot_response = generate_bot_response(message)
#
#     st.session_state.messages.append(user_message)
#     st.session_state.messages.append(bot_response)
#
#     updated_chat_log = "<br>".join(st.session_state.messages)
#     st.session_state.chat_log_element.markdown(
#         f"<div class='chat-log'>{updated_chat_log}</div>", unsafe_allow_html=True
#     )
#
#
# def generate_bot_response(user_input):
#     data = {"message": user_input}
#     response = requests.post(
#         settings.backend_url_guest + f"/send_message/{st.session_state.session_id}",
#         params=data,
#         headers={"Content-Type": "application/json"},
#     )
#     return f"Restaurant: - {response.json()['message']}"
#
#
# st.set_page_config(page_title="Make Order", page_icon="🛎️")
#
# st.write(" # Restaurant chat bot ")
# initialize_chat_session()
# display_chat_log()
#
# st.text_input(
#     key="widget",
#     on_change=submit,
#     label="user input",
#     label_visibility="hidden",
#     placeholder="type here",
# )


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
    st.session_state["temp"] = ""


def query(payload):
    data = {"message": payload}
    response = requests.post(
        settings.backend_url_guest
        + f"/send_message/{st.session_state.session['order_id']}",
        params=data,
        headers={"Content-Type": "application/json"},
    )

    return response.json()["message"]


def clear_text():
    st.session_state["temp"] = st.session_state["text"]
    st.session_state["text"] = ""


user_input = st.text_input(
    key="text",
    on_change=clear_text,
    label="user input",
    label_visibility="hidden",
    placeholder="type here",
)


if not st.session_state.generated:
    st.session_state.generated.append(
        f"Restaurant: - {st.session_state.session['message']}"
    )

if st.session_state["temp"]:
    output = query(st.session_state["temp"])

    st.session_state.past.append(f"You: - {st.session_state['temp']}")
    st.session_state.generated.append(f"Restaurant: - {output}")


if st.session_state["past"]:
    message(st.session_state["generated"][-1], key=str(-1))
    for i in range(len(st.session_state["past"]) - 2, -1, -1):
        message(st.session_state["past"][i + 1], is_user=True, key=str(i) + "_user")
        message(st.session_state["generated"][i], key=str(i))
