import os
from embedchain import Pipeline as App
import streamlit as st


with st.sidebar:
    st.title("EL-DEMO")
    st.subheader("Prajwal M Pawar 1RV21AI038")
    st.subheader("Aayaan Hasnain 1RV21AI001")
    st.subheader("Akshay Alva 1RV21AI007")  
    st.subheader("Ayush Goyal 1RV21AI015")

st.title("💬 RVChat")
st.caption("🚀 LLM used for demo: Mixtral-8x7B-Instruct-v0.1")
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": """
        Hello professors! I'm a model chatbot. I can answer anything you want to know about RVCE \n
        For now, my knowledge base consists of the homepage and pdfs. However, I can more documents, pdfs, circulars that
                my creators give me!        """,
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


#here we embed the html file in the streamlit app, ok?
with open("maps.html", "r") as f:
    map_html = f.read()
st.components.v1.html(map_html, width=1000, height=600) #take 1000x600 as defualt


if prompt := st.chat_input("Ask me anything!"):
    

    os.environ["HUGGINGFACE_ACCESS_TOKEN"] = "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"
    app = App.from_config(config_path="config.yaml")

    if prompt.startswith("/add"):
        with st.chat_message("user"):
            st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
        prompt = prompt.replace("/add", "").strip()
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Adding to knowledge base...")
            app.add(prompt)
            message_placeholder.markdown(f"Added {prompt} to knowledge base!")
            st.session_state.messages.append({"role": "assistant", "content": f"Added {prompt} to knowledge base!"})
            st.stop()

    with st.chat_message("user"):
        st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        msg_placeholder = st.empty()
        msg_placeholder.markdown("Thinking...")
        full_response = ""

        for response in app.chat(prompt):
            msg_placeholder.empty()
            full_response += response

        msg_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
