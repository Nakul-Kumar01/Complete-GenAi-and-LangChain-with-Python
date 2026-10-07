

"""
- Revision : Lec 17, 24


##### Lec03  #####:
- groq : it is not LLM ,it provides the platform to run LLM







### Lec04 - what is LangChain ???   ####:         ###### File : notebook 1

- if we want to use diff LLMs in our project -> it may be difficult since, every llm has diff liberary and coding structure
- its soln is Langchain : opensource framework simplify building applications powered by LLMs 

LangGraph : used to build multi-agent systems
LangSmit : provide support to deploy application on cloud


Langchain k sath hmm different LLMs integrate kr skte hai


pip install -r .\requirements.txt      --> used to install all dependencies we will use present in requirements.txt


.ipynb means Jupyter Notebook file  : used for experiments and learning
Kernel = the Python environment/process that runs your notebook code


for first time install ipykernel :
Your virtual environment may already work perfectly for normal .py files, but Jupyter notebooks need ipykernel to use that environment as their Python kernel




from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash"
)


res = llm.invoke("who is pm of india??") 
res.content[0]["text"]







### Lec05 - Multiple LLM Models with LangChain   #########

- we can use multiple LLMs with same syntax using langchain



- we pass input as string but this is not standart way
- so we use prompts

prompts = [    // list of tuples or dict
("system","you are a python developer"),               #### (type, prompt)    type: system, ai, user
("user", "How to sort the array")
]

system prompt:  how LLM hv to behave
ai prompt: answered by LLM
user prompt: LLM has to answer this query









###  Lec06 - Dynamic Prompts & LLM's with LangChain    ###### File : notebook 2

- standard way of prompts is list of dict
prompts = [
{},
{}
]


- For Dynamic Prompts we use :
from langchain_core.prompts import ChatPromptTemplate


- Standard way of Dynamic prompts : by Chains

Runnable : jis data ko hm invoke kr sake vo runnable hai


prompts = ChatPromptTemplate.from_messages([
    {"role":"system", "content" : "u are {language} Translator"},
        {"role":"user", "content" : "{query}"},
])

chains = prompts | llm   
res = chains.invoke({"language":"hindi","query":"I love you"})
print(res.content[0]["text"])











####  Lec07 - LLM QnA Chatbot ( LangChain and Streamlit )         ### File : apps 1


Streamlit : give pre build UI component for genai

st.title()
st.markdown()
st.chat_message(role).markdown(content)



- when a new question is asked the server will reload itself
- then a new MemorySaver() object is created if we want to save history of conversation
- solution: st.session_state   ye preserve rahega so yaha history store kro














####   Lec 08 - Add Memory to AI Chatbot      ####  File :  notebook 3
- providing previous conversation  data to any LLM









####  Lec 09 - Structured Output In LangChain          ## File : notebook 4

lyberary used : pydantic

if we want to make any field as List of something  
i.e. list of movie name  : lyberary used : typing


f"Hello {name}"   # Python replaces {name}
"Hello {name}"    # Keeps {name} as text        // like this we use while dynamic prompt
                 # LangChain can replace it later


- it is useful when i want to use an API, then we can send this structured o/p as payload

- when llm work with structured o/p, it always return answer in structure, whehter we ask question off topic or not










### Lec 10 - Ollama        ## File : notebook 5

- tool for running AI language models locally on your own computer
 rather than sending every request to a cloud AI service

- jis model ko aap locally  install krte ho usse hi app usko use kr skte ho langchain mei


- for ollama also syntax of langchain will remain same 




gemma3:1b  : llm of google trained on 1 billion parameters





###  Lec 11 - Open Source LLM Models using Groq         ##  File : notebook 6


- Groq : Ai company, which has designed its chip called LPU(language processing unit)
- LPU : optimised for running LLMs with low latency and high throughput
        they provide this speed via their cloud infra(GroqCloud) -> allow to scale real-time AI applications


openai/gpt-oss-20b  // we hv used this and it is fast


- if we want to run llm very fast then we use Groq platform











### Lec 12 - Stream LLM Responses       ## File : notebook 7

in pyton : Normally print() automatically adds a newline after printing

Internally, the default is basically:
print("Hello", end="\n")

When we write: 
print("Hello", end="")    #### after printing, add nothing










####  Lec 13 - AI Agents         


LLM bss kuch generate kr skte hai jaise Text

LLM cannot do :  DB_ACCESS, api calls, google search


then what is soln : Tools (python functions)



ex:  tool1 for DBaccess , tool2 for weather API, etc

1) 
now query is temperature of Bhopal ??
llm will first check whether it can answer it or not.
if not then check which tool can perform this task.


2)
llm will generate the required arguments for that tool.
and then call that tool and wait for result.
now tool will send result to llm, now llm will check
whether it is required result if not then again call the tool, after the required result then llm will reform it 
in human language



so this is a pattern :   Thinking (tool??)  ->  Action(performing task)   ->   observation(req. o/p or not  , if not then again they will loop T -> A -> O)
this pattern is called 'ReAct'  = Reasoning + Action



Agents : combination of prompts + LLM + tools
- when LLM hv access to tools then it is an agent


when we buy subscription of openAI then we get access to LLM and tools
but when we buy API key we get access to LLM only














##### Lec 14 - Building AI Agents         ### File : notebook 8


we need : create_agent, tool

from langchain.agents import create_agent
from langchain_core.tools import tool


- build tool :
@tool
def add_number(a:int ,b:int):
    #here is doc string

    return a + b



- create agent :
agent = create_agent(  # agent is combination of these 3 things
    model=llm,
    tools = [add_number,multiply_number],
    system_prompt="You are a math teacher, and always use tool for calculation."
)



- give prompt to agent :
res = agent.invoke({"messages":[{"role":"user","content":"what is sum of 2 and 3"}]})











###  Lec 15 - Build Google Search AI Agent        ## File : notebook 9


tool used : google serper to search on google


search = GoogleSerperAPIWrapper()

agent = create_agent(
    model= llm,
    tools = [search.run],
    system_prompt= "You are an agent and can search any question on google."
)

res = agent.invoke({"messages": [{"role":"user","content":question}]})
here this will follow all 3 phases : T -> A -> O

                  ┌──────────────┐
                  │    User      │
                  └──────┬───────┘
                         ↓
                  ┌──────────────┐
                  │     LLM      │
                  └──────┬───────┘
                         ↓
                  Need a tool?
                   /         \
                 No           Yes
                 ↓             ↓
              Answer      Google Search
                               ↓
                              LLM
                               ↓
                            Answer











### Lec - 16   Build AI Agent with Memory & Conversation History        ## File : notebook 9

we hv used langgraph.checkpoint.memory for this



there are 2 methods for mentaining the History :


1) Manual Method : we hv used earlier
   its cons : - manage history yourself, 
              - *** an agent can also generate tool messages : If you manually save only the final AI answer, you're throwing away the intermediate tool-call history.



2) langgraph's Checkpointer :    You don't manually create this dictionary   // here this creation of MemorySaver address is inmemory
conversations = {
    "1": [                                        // for thread_id : "1"
        HumanMessage("My name is Nakul"),
        AIMessage("Nice to meet you Nakul"),
        HumanMessage("What is my name?"),
        AIMessage("Your name is Nakul")
    ],

    "2": [                                        // for thread_id : "2"
        HumanMessage("My name is Rahul"),
        AIMessage("Nice to meet you Rahul")
    ]
}


- for a particular id we will maintain seperate history, 
    if id changed then maintain another seperate history


    






    
###  Lec 17 - QnA Chatbot using Groq         ## File : apps 2

# llm
# tool - google search
# agent
# memory
# streaming 
# web Interface




- when we are asking next question then server will reload again, 
  then different memory object is made:
  memory = MemorySaver()


solution: st.session_state   ye preserve rahega so yaha history store kro


st.session_state.memory = MemorySaver()   // to preserve chat history for llm context
st.session_state.conversation = []     // to preserve conversation to display on browser















###  Lec 19 - What is RAG ??

- Retrieval Augmented Generation:
- enhances LLMs models by connecting them to external knowledge bases
- allowing them to retrieve relevent up to date data into before generating ans
- making answer more domain specific





- LLM is trained over pre-trained data

- But if we want to train LLM for particular company: high cost
- we can fin-tune the LLM -> but require high memory and context window also token cost will be very high

- if a company has 1000 page pdf document, and need to answer the query on the basis of this document
- if we directly attach this file , then we need much higher context window  -> not possible


soln : RAG based system


# RAG pipeline:
    'Indexing Phase(store)'
1) Load the Document
2) split the docs in Chunks
3) generate Vector Embeddings
4) store in Vector DB  (vector Embeddings + respective document)

this is One Time Process

    'Query phase(retrival)'
1) now when user asks question, we search for most relevent ans in vector DB, this is called Similarity search
2) Data which we get from DB is stored in variable , named similar data
3) now give  question + similar data  to LLM   -> Generate final answer


this whole process is 'RAG Pipeline'

pros : token cost is low(since, sending only relevent data to LLM, insted of whole pdf)
       No question on context window full

       












###  Lec 20 - Data Loading in RAG Pipeline          ## File : notebook 10

- all loaders will be get from:  langchain_community.document_loaders

- every loader in langchain treats a File as list of documents
- hence, give result in list form : hving objects of Document
- each object hv 2 agruments : metadata , page_content


texts = loader.load()
print(len(texts))     ### gives no. of documents

if pdf hv 9 pages , then length of list will be 9.




- web loader require 2 packages :
langchain_community.document_loaders   and beautifulsoup4 (for parsing HTML)

URL
 ↓
WebBaseLoader
 ↓
downloads HTML
 ↓
extracts text from HTML
 ↓
LangChain Document
 ↓
docs = [Document(...)]

















###   Lec 21 - Text Splitting for RAG Systems      ## File : notebook 11

- chunk_size = 50 : each chunk should hv 50 characters
- chunk_overlap = 20 : ek chunk ke 20 characters next chunk ke 20 characters ke sath overlap krna chaiye



langchain_text_splitters  package is used 

















### Lec 22 -    Vector Embeddings & Vector Databases          ## File :  notebook 12

Vector Embeddings : numerical representation that capture meaning and relationship
of complex data like words, sentences, images or audio  , where similar items are 
clustered together


| Feature           | Rahul | Anuj | Priya |
| ----------------- | ----: | ---: | ----: |
| **ID**            |   101 |  102 |   103 |
| **Height**        |   5.8 |  6.0 |   5.5 |
| **Coding Skills** |  9/10 | 3/10 |  8/10 |
| **Communication** |  8/10 | 4/10 |  8/10 |
| **Intelligence**  |  9/10 | 6/10 |  7/10 |
| **Age**           |    22 |   21 |    21 |
| **Sports**        |  3/10 | 9/10 |  2/10 |



Rahul = [5.8, 0.9, 0.8, 0.9, 22, 0.3]

Anuj = [6.0, 0.3, 0.4, 0.6, 21, 0.9]

Priya = [5.5, 0.8, 0.8, 0.7, 21, 0.2]     these are vectors


and converting text into vector is called Vector Embeddings



- in multidimention we find the Angle b/w various vectors
- with less angle are more similar
- this is called similarity search or cosine similarity(measure angle b/w 2 vectors)
- i.e.  rahul and priya are more similar


- in sql or mongodb we are using these for exact search, but here we have to find the 
  similar vectors so we hv to use vector Database



- Vector store : stores embedded data and performs similarity search
i.e. chromaDB 

# Indexing phase-
documents  ->  embedding model -> embedding vecor  ->  vector store



what Chroma does ??

documents
    ↓
Chroma.from_texts()
    ↓
embeddings.embed_documents(documents)     #convert text to embeddings
    ↓
3072-dimensional vectors
    ↓
Store vectors + documents in Chroma












### Lec 23 - Build Complete RAG-Based PDF QnA Chatbot         ## File : notebook 13

1) load document
2) split
3) embedd 
4) store in vector DB


- then we will create chain of : context_generater | prompt | llm | strParser












#### Lec 24 - Agentic RAG System     ## File - notebook 14

- Indexing phase is same as of normal rag system

- Retrival phase : when user asks multiple questions in single query:-
then in simple RAG their may be chances that it will fetch only data related to single query
but in Agentic Rag it will fetch data related to both question

- also when their is multiple Vector Db then also AI agent will help us to tell from which DB we hv to fetch the embeddings 


- In notebook 13 project , we call get_context function always, it is simply a function not tool, also it is called once only(context mila ho ya na mila ho)

- In this project retriever_tool is called when it is needed, and can be called multiple times, ye ek llm ka tool hai jisko llm jb chahe call kr skta hai 
- bss hmne tool banake llm ko dedeya abb langchain khud sbb sambhal lega: jese tool ko agrgument pass krna / tool ka return hua data ko handle krna


- jb tk Agent ko required data nhi mill jata tb tk tool ko call krte rahenge


- tool ko hmm directly call nhi kr skte tool() ,no
- tool ko hmm invoke kr skte hai , tool.invoke(arguments)












### Lec 25 - Agentic RAG Chatbot with PDF Upload      ## File : apps 4

-- PROJECT











### Lec 27 - LangGraph         ## File: notebook 14

- with langChain we can build AI Agent and can perform specific task with that AI Agent

- with LangGraph we can build multi AI Agent system




------  How LangChain works ??   ----------
- when user asks a query then LLM
- now LLM hv 2 choices , if LLM is capable of answering then it will answer oterwise it take help of tools then answer
- we are connecting language model in linear chain
- Usually more straightforward/linear


User
 ↓
LLM Agent
 ↓
Tool 1 / Tool 2 / Tool 3
 ↓
Response




------  How LangGraph works ??   ---------
- good for multiple agents working together
- Supports loops, branching, retries, human approval, memory/state

- ** Here, you define how different agents interact and control the flow  **



- in LangGraph we have to maintain the state : like user questoin, requirement, result of every state  -> we hv to store all this data in Global state



- when user asks any query then final result of langGraph is the state
   basically state hi return hoti hai at last












### Lec 28 - QnA Chatbot with Memory using LangGraph       ## File: notebook 17    and    app 5

 - storing data:
   - list of history
   - langGraph Checkpoint
   - chroma Vector DB  (to store embedding)
   - langchain_community.vectorstores import InMemoryVectorStore  (to store embedding)



- to build graph : build all nodes  -> build edges -> finalGraph



- In LangGraph, every node returns a state update, not necessarily the entire global state.
- LangGraph merges that update into the existing state:

Before:
messages = [...]
count = 5

          ↓ node

Update:
count = 6

          ↓ LangGraph

After:
messages = [...]
count = 6










### Lec29 - Multi AI Agentic System          ## File : notebook 18

┌─────────────────────────────────┐
│           User Input            │
└────────────────┬────────────────┘
                 │
                 │ Coding, Weather, Google Search
                 ▼
┌─────────────────────────────────┐
│        Question Category        │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│              Route              ├────────► Conditional Node
└────────────────┬────────────────┘
                 │
        ┌────────┼────────┐
        │        │        │
        ▼        ▼        ▼
 ┌──────────────┐│┌──────────────┐
 │Google Search │││ Weather Node │
 └──────┬───────┘│└──────┬───────┘
        │   ┌────┴────┐  │
        │   │ Coding  │  │
        │   └────┬────┘  │
        │        │       │
        └───────►▼◄──────┘
            ┌─────────┐
            │   END   │
            └─────────┘










###   Lec 30 : Build RAG Pipeline using LangGraph     ## File : notebook 19


- ##### Node  :    question -> retrive  ->  context  ->  generate  ->  end




"""