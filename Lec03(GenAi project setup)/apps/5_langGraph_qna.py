
from dotenv import load_dotenv
load_dotenv()

from pydantic import BaseModel
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages   
from langgraph.checkpoint.memory import InMemorySaver
from typing import Annotated



class ChatState(BaseModel):
    messages:Annotated[list,add_messages]


llm = ChatGroq(model="openai/gpt-oss-20b")



def chatBotNode(state:ChatState) -> ChatState:
    res = llm.invoke(state.messages)
    state.messages = [res]  ## res will atomatically append in the state.messages list by add_messages
    return state



memory = InMemorySaver()


graph = StateGraph(ChatState)
graph.add_node("chatBot",chatBotNode)


## build Edge : we hv build the flow
graph.add_edge(START,"chatBot")
graph.add_edge("chatBot",END)



finalGraph = graph.compile(checkpointer=memory)


while True:
    query = input("User: ")
    if query.lower() in ["quit", "exit","bye"]:
        print("Thanks for using me!")
        break

    res = finalGraph.invoke(
    {"messages" : [{"role":"user", "content":query}]},
    {"configurable":{"thread_id":"1"}}
    )

    ans = res["messages"][-1].content

    print("ai: ",ans)
    