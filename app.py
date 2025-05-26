import streamlit as st
from utils import s3_loader, encryptor, retriever, mpc_layer
from config import OPENAI_API_KEY
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="Compliance Assistant", layout="wide")
st.title("🛡️ Clara the Compliance Bot: Your AI Compliance Companion for Banks")
st.markdown("Securely query encrypted audit logs, policies, and regulations.")

@st.cache_resource
def init_vectorstore():
    keys = s3_loader.list_files()
    file_paths = [s3_loader.download_file(key) for key in keys]
    retriever.build_vectorstore(file_paths)
    return retriever.load_vectorstore()

vectorstore = init_vectorstore()
llm = OpenAI(openai_api_key=OPENAI_API_KEY)
qa_chain = load_qa_chain(llm, chain_type="stuff")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "👋 Hello! I'm your Regulatory Compliance Assistant. How can I help you today?"}
    ]
    st.session_state.awaiting_confirmation = False

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_query = st.chat_input("Ask me about compliance, audits, regulations...")

greetings = {"hi", "hello", "hey", "good morning", "good afternoon", "good evening"}

if user_query:
    normalized = user_query.lower().strip()
    st.session_state.messages.append({"role": "user", "content": user_query})

    if normalized in greetings:
        greeting = "👋 Hello again! How can I help you today?"
        st.session_state.messages.append({"role": "assistant", "content": greeting})
        st.chat_message("assistant").write(greeting)
        st.session_state.awaiting_confirmation = False

    elif st.session_state.awaiting_confirmation and normalized in {"no", "nothing", "nope", "that's all","thanks","thank you"}:
        goodbye = "Thank you! Have a great day!"
        st.session_state.messages.append({"role": "assistant", "content": goodbye})
        st.chat_message("assistant").write(goodbye)
        st.session_state.awaiting_confirmation = False

        st.markdown("---")
        if st.button("🔄 Start New Chat"):
            st.session_state.messages = [{"role": "assistant", "content": "👋 Hello! I'm your Regulatory Compliance Assistant. How can I help you today?"}]
            st.session_state.awaiting_confirmation = False
            st.rerun()

    else:
        with st.spinner("🔐 Running MPC-secured query..."):
            docs = vectorstore.similarity_search(user_query, k=2)
            raw_texts = [doc.page_content for doc in docs]
            secured_context = mpc_layer.mpc_secure_query(user_query, raw_texts)
            response = qa_chain.run(input_documents=docs, question=user_query)

        full_reply = response + "\n\n🤖 Is there anything else I can help you with?"
        st.session_state.messages.append({"role": "assistant", "content": full_reply})
        st.chat_message("assistant").write(full_reply)

        with st.expander("🔍 Secure Context Retrieved"):
            st.write(secured_context)

        st.download_button("Download Report", data=response, file_name="compliance_response.txt", key=f"dl_{len(st.session_state.messages)}")

        st.session_state.awaiting_confirmation = True
