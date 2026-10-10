

from langgraph.graph  import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command


from state import BlogState
from agent import get_llm, researcherAgent,writerAgent,editorAgent


MAX_REVISION = 3



###  Node build kro 
def researcher_node(state: BlogState):
    """Researcher Agent generates(or revises) the research outline"""   ### giving info about the Node

    llm = get_llm()

    research_data = researcherAgent(
        llm = llm,
        topic= state.topic,
        audience= state.audience,
        feedback=state.research_feedback
    )

    state.research = research_data
    state.research_feedback  = ""

    return state




def Human_review_research_node(state:BlogState):
    """Pause and ask the human to approve the research or send the feedback"""

    decision = interrupt({
        "stage":"researcher_review",
        "research": state.research,
        "instruction": (
            "Reply with 'approve' to continue to writing",
            "or describe what to change to send it back to the researcher."
        )
    })


    

