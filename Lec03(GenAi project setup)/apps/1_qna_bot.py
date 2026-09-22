
from dotenv import load_dotenv 
load_dotenv()


from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st

llm = ChatGoogleGenerativeAI(model = "gemini-3.5-flash-lite")


st.title("AskBuddy - AI Qna Bot")
st.markdown("My Qna Bot with Langchain and google Gemini")



if "messages" not in st.session_state:
    st.session_state.messages = []



for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]
    st.chat_message(role).markdown(content)  ## iss line ka mtlb ye content dikha do



que = st.chat_input("Ask anything ?")
if que:
    st.session_state.messages.append({"role":"user","content":que})
    st.chat_message("user").markdown(que)   # user ne query di hai
    res = llm.invoke(que)
    st.chat_message("ai").markdown(res.content[0]["text"])
    st.session_state.messages.append({"role":"ai","content":res.content[0]["text"]})




# while True :
#     que = input("User: ")

#     if que.lower() in ["quit","exit","bye"]:
#         break

#     res = llm.invoke(que)
#     print(res.content[0]["text"])