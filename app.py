from common import *
import streamlit as st
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.chains import RetrievalQA
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
# 1. Session Initialize & Donation
initialize_session()


embeddings = OpenAIEmbeddings()
temporal_docs_vector_store = Pinecone.from_existing_index(st.session_state["index_name"], embeddings)
conversational_memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    k = 5,
    return_messages = True
)
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

template = """Use the following pieces of context to answer the question at the end. 
If you don't know the answer, just say that you don't know, don't try to make up an answer. 
Use five sentences maximum and include java code examples where applicable. 
{context}
Question: {question}
Helpful Answer:"""
QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)



# 2. Sidebar username input
st.sidebar.title("`Temporal Java Docs`")
st.session_state["user_name"] = st.sidebar.text_input(
    "GitHub Username:",
    key="github_user_input",
    placeholder="input GitHub username",
    value=st.session_state["user_name"],
    on_change=handling_user_change,
)

# Main screen chat
st.header("`Chat with Temporal Java Docs`")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])



# React to user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        result_docs = temporal_docs_vector_store.similarity_search(
            prompt,  # our search query
            k=3  # return 3 most relevant docs
        )
        print("result docs length:", len(result_docs))
        result_vector_store = Pinecone.from_documents(
            result_docs,
            embeddings,
            index_name=st.session_state["index_name"]
        )
        qa_chain = RetrievalQA.from_chain_type(
            llm,
            retriever=result_vector_store.as_retriever(),
            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
        )
        result = qa_chain({"query": prompt})
        full_response = result["result"]
        message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

