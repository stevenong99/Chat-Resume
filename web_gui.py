import os
import streamlit as st

from utilities import is_api_key_valid

st.title("Chat Resume")

valid_api_key = False

st.markdown("### Enter OpenAI API key here:")
openai_api_key = st.text_input("Enter OpenAI API key here", key="langchain_search_api_key_openai", type="password", label_visibility="collapsed")
if is_api_key_valid(openai_api_key):
    os.environ["OPENAI_API_KEY"] = openai_api_key
    valid_api_key = True
    st.info("OpenAI API key valid.")
else:
    st.info("OpenAI API key invalid. Please enter a different API key.")

with st.sidebar:
    st.markdown("# Made by [Steven](https://github.com/stevenong99)")
    st.markdown("A simple chatbot that tells you all about me.\n")
    st.markdown("Source Code: [Here](https://github.com/stevenong99/Chat-Resume)")
    st.markdown("Contact Me: [Here](https://www.linkedin.com/in/ong-teng-kheng-5114431a9/)")
    st.markdown("## Some examples questions you could ask:")
    st.markdown('''
                1. What is his educational background?
                2. What projects has he done?
                3. Tell me more about {project name}
                4. How many years of experience does he have?
                5. What languages does he code in?
                6. What are his hobbies?
                ''')

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello, I'm Cerulean, Steven's robot assistant. He's not paying me, so let's make this quick. What would you like to know about him?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if not valid_api_key:
        st.info("It costs approximately 2 USD per conversation. Please enter your OpenAI API key if you want to use this.")
        st.stop()
    else:
        from doc_qa_utils import get_answer

        assistant_response = {
            "role": "assistant",
            "content": get_answer(prompt)
        }
        st.session_state.messages.append(assistant_response)
        st.chat_message("assistant").write(assistant_response["content"])
