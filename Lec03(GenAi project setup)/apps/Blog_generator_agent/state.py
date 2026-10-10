

from pydantic import BaseModel


class BlogState(BaseModel):        
    ### user Input
    topic: str = ""
    audience:str = ""


    ### Researcher Output
    research: str = ""
    research_feedback: str = ""


    ### Writer Output
    draft: str = ""
    draft_feedback: str = ""


    ### Editor Output
    final_blog: str = ""


    ### Metadata
    revision_count: int = 0     ## kitni barr improvements ki hai  // so that we can prevent the llm from infinite loop