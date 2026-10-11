

from langgraph.graph  import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command
from typing import Literal


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


    if isinstance(decision,dict):
        action = decision.get("action","approve")
        feedback = decision.get("feedback","")
    else:
        text = str(decision)
        action = "approve" if text.lower() in ["approve","approved","ok","yes"] else "revised"

        feedback = "" if action == "approve" else text   ## agr action is 'approve' then feedback will be empty


    state.research_feedback = feedback
    return state 







def writer_node(state: BlogState):
    """Writer Agent produce the full draft blog (or revise it)"""  

    llm = get_llm()

    draft_data = writerAgent(
        llm = llm,
        topic= state.topic,
        audience= state.audience,
        feedback=state.draft_feedback
    )

    state.draft = draft_data
    state.draft_feedback  = ""

    return state





def Human_review_draft_node(state:BlogState):
    """Pause and ask the human to 'approve' the draft or send the feedback"""

    decision = interrupt({
        "stage":"draft_review",
        "draft": state.draft,
        "instruction": (
            "Reply with 'approve' to continue to Editor",
            "or describe what to change to send it back to the writer."
        )
    })


    if isinstance(decision,dict):
        action = decision.get("action","approve")
        feedback = decision.get("feedback","")
    else:
        text = str(decision)
        action = "approve" if text.lower() in ["approve","approved","ok","yes"] else "revised"

        feedback = "" if action == "approve" else text   ## agr action is 'approve' then feedback will be empty


    state.draft_feedback = feedback
    return state 








def editor_node(state:BlogState) :
    llm = get_llm()
    final = editorAgent(
        llm = llm,
        topic=state.topic,
        draft=state.draft
    )


    state.final_blog = final
    return state 





####   Conditional Node

def route_after_research_review(state:BlogState) -> Literal["research","writer"]:
    if state.research_feedback:
        return "research"
    else:
        return "writer"



