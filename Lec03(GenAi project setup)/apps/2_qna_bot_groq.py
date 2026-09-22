from dotenv import load_dotenv
load_dotenv()


from langchain_groq import ChatGroq
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
import streamlit as st



llm = ChatGroq(model="openai/gpt-oss-20b",streaming=True)
search = GoogleSerperAPIWrapper()   ## search is not a tool , tool tho iske andr hai
tools = [search.run]

# memory = MemorySaver()   ## page reload hone pre ye to change ho jaega
# print(memory)  # isse pata chal jaega memory ka address
if "memory" not in  st.session_state:         ## issme store kro , ye preserve rahega
    st.session_state.memory = MemorySaver()
    st.session_state.conversation = []    # to display previous conversation





agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="you are a amazing ai agent and can search on google as well",
    checkpointer= st.session_state.memory
)



#####   Building web interface    #####

st.subheader("QuickAnswer - Answers at the speed of thought")



for message in st.session_state.conversation:   ## Display previous message
    role = message["role"]
    content = message["content"]
    st.chat_message(role).markdown(content)




query = st.chat_input("Ask Anything ??")
if query:
    st.chat_message("user").markdown(query)
    st.session_state.conversation.append({"role":"user","content":query})


    res = agent.stream(
    {"messages": [{"role":"user","content":query}]},
    {"configurable":{"thread_id":"1"}},
    stream_mode="messages"   ## in agents we hv to give this , but not in llms
    )


    ai_container = st.chat_message("ai")
    with ai_container:
        space = st.empty()     # space is refering to ai_container

        message = ""

        for chunk in res:
            message = message + chunk[0].content
            space.write(message)    ## writing in st.chat_message("ai")

        st.session_state.conversation.append({"role":"ai","content":message})

    # ans =res["messages"][-1].content

    # st.session_state.conversation.append({"role":"ai","content":ans})

    # st.chat_message("ai").markdown(ans)






