

import os 
from langchain_groq  import ChatGroq
from langchain_core.prompts import ChatPromptTemplate




####   Get LLM
def get_llm(modelName :str = "openai/gpt-oss-20b",temperature: float = 0.5):
    api_key = os.getenv("GROQ_API_KEY")
    llm = ChatGroq(model=modelName,temperature= temperature,api_key=api_key)
    return llm 





###   Researcher Agent
RESEARCHER_PROMPT = ChatPromptTemplate.from_messages([           ## Preparing Dynamic Prompts    ## we will also use Chains
    {
        "role": "system",
        "content": """
            "You are a Research Agent. Given a blog topic and target audience, produce a clear, "
            "structured research outline. Include:\n"
            "1. 5-7 key points the blog should cover\n"
            "2. Important facts, stats, or examples for each point\n"
            "3. Suggested angle or hook\n"
            "Be concise. Use bullet points. Do NOT write the full blog yet."
        """
    },
    {"role": "user", "content": "Topic: {topic}, Audience: {audience}, {revisionHint}, write the research outline now"}
])


def researcherAgent(llm:ChatGroq, topic:str, audience:str, feedback:str = "") -> str :
    revisionHint = f"The Human provided this feedback on your previous research - please address it: {feedback}."

    if not feedback:
        revisionHint = "This is your first attemt"


    chain = RESEARCHER_PROMPT | llm 


    res = chain.invoke({
        "topic":topic,
        "audience": audience,
        "revisionHint":revisionHint
    })


    return res.content





###  Writer Agent

WRITER_PROMPT = ChatPromptTemplate.from_messages([
    {
        "role": "system",
        "content": (
            "You are a Blog Writer Agent. Using the research notes provided, write a complete, "
            "engaging blog post.\n"
            "Rules:\n"
            "- Length 500-800 words\n"
            "- Structure: catchy title, intro hook, 3-5 sections with H2 headings, conclusion\n"
            "- Tone: clear, friendly, suited to the target audience\n"
            "- Use markdown formatting\n"
            "- Do NOT add a 'word count' line at the end"
        ),
    },
    {
        "role": "user",
        "content": """
                 Topic : {topic},
                 Audience: {audience},
                 Research Notes: {research}

                 {revisionHint}

                 write the full Blog post now.
        """
    },
])


def writerAgent(llm:ChatGroq, topic:str, audience:str, research:str="", feedback:str = "") -> str :
    revisionHint = f"The Human provided this feedback on your previous Draft and asked for these changes: - please address it: {feedback}."

    if not feedback:
        revisionHint = "This is your first attemt"


    chain = WRITER_PROMPT | llm 


    res = chain.invoke({
        "topic":topic,
        "audience": audience,
        "research": research,
        "revisionHint":revisionHint
    })


    return res.content





###  Editor Agent
EDITOR_PROMPT = ChatPromptTemplate.from_messages([
    {
        "role": "system",
        "content": """
            "You are an Editor Agent - the final quality gate before publishing.\n"
            "Take the draft and produce the FINAL polished version. Specifically:\n"
            "- Fix grammar, spelling, and awkward phrasing\n"
            "- Tighten wordy sentences\n"
            "- Improve flow and transitions between sections\n"
            "- Make the title and intro more compelling if needed\n"
            "- Keep the same structure and markdown formatting\n"
            "- Blog wording should look like human, not a AI and don't use any special chars and complex / fancy words. \n"
            "Output only the final polished blog post - no commentary."
        """
    },
    {
        "role": "user",
        "content": """
            "Topic: {topic},\n"
            "Draft" : {draft}
            Return the published blog post
        """
    }
])



def editorAgent(llm:ChatGroq, topic:str,draft:str) -> str :


    chain = EDITOR_PROMPT | llm 


    res = chain.invoke({
        "topic":topic,
        "draft":draft
    })


    return res.content


