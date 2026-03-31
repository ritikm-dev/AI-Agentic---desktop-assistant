from langgraph.prebuilt import  ToolNode,tools_condition
from langgraph.graph import StateGraph,START,END
from langchain_core.messages import AIMessage,SystemMessage,HumanMessage
from langchain_core.tools import tool,Tool
from langgraph.graph.message import  TypedDict,add_messages,Annotated
from langchain_openai import ChatOpenAI
from .Tools import browser_tool
from dotenv import load_dotenv
import os
load_dotenv(override=True)
llm_url = ChatOpenAI(
model="gemini-2.5-flash-lite",  
    openai_api_key=os.getenv("GEMINI_API_KEY"),  
    openai_api_base=os.getenv("GEMINI_BASE_URL"),
)

llm_web = ChatOpenAI(
model="gemini-2.5-flash-lite",  
    openai_api_key=os.getenv("GEMINI_API_KEY"),  
    openai_api_base=os.getenv("GEMINI_BASE_URL"),


)
class State(TypedDict):
    messages : Annotated[list,add_messages]
    user_query : str
    url : str
    bot_msg : str



tool1 = [browser_tool]
llm_with_web = llm_web.bind_tools(tool1)

def url_extracter(state : State):
    messages = [
        SystemMessage(
            content="""
You are a multilingual URL generation agent.

Your task is to understand the user's intent in ANY language and decide whether to generate a URL or not.

---

### Step 1: Multilingual Intent Detection

You MUST detect intent regardless of language (English, Tamil, Hindi, etc.).

- If the user input is casual conversation (greetings, small talk, jokes, chit-chat in ANY language):
  Examples:
  - "hi", "hello"
  - "vanakkam", "saptiya"
  - "namaste", "kaise ho"
  
  → Return exactly: NONE

- If the user input does NOT clearly ask to open, search, or access a website/app:
  → Return exactly: NONE

- Only proceed if the user clearly intends to:
  - open a website/app
  - search something
  - access online content

---

### Step 2: Understand Action in Any Language

Detect words meaning "open" or "search" across languages:

- English: open, search, find
- Tamil: open, திற, தேடு
- Hindi: खोलो, खोजो
- Hinglish: open karo, search karo

Even if mixed language is used, you MUST correctly detect intent.

---

### Step 3: URL Generation Rules

1. If user says "open <website/app>"
   → Return homepage URL  
   Example: open youtube → https://www.youtube.com  

2. If user includes search intent:
   → Generate proper search URL  

   Examples:
   - Google → https://www.google.com/search?q=<query>
   - YouTube → https://www.youtube.com/results?search_query=<query>

3. If user says open + search:
   → Open that site with search query

4. Encode spaces using "+" or "%20"

5. Unknown website:
   → Use Google fallback  
   https://www.google.com/search?q=<query>

---

### Step 4: Safety Rules

- If user asks for adult, illegal, or unsafe content:
  → Return exactly: NONE

---

### Step 5: Output Rules (STRICT)

- Output ONLY:
  1. A valid URL  
  OR  
  2. NONE  

- No explanation  
- No extra text  
- No formatting  
   """
        ),
        HumanMessage(
            content=f"""User Query: {state['user_query']}"""
        )
    ]
    result = llm_url.invoke(messages)
    print(result.content)
    return {
        "messages" : [result],
        "url" : result.content.strip()
    }

def query_agent(state : State):
    if state["url"] == "None":
         return {
              "messages" : [AIMessage(content="False")]
         }
    messages = [
        SystemMessage(
            content="""
               You are a strict web-browsing agent.

Your job is to decide whether a URL can be opened using the tool `browser_tool`.

### Step 1: Validate URL
- If the URL is "NONE", empty, invalid, or not a proper web link:
  → DO NOT use the tool
  → Return exactly: False

### Step 2: Tool Usage
- If the URL is valid:
  → You MUST call the tool `browser_tool`
  → Pass the URL as input

### Step 3: Output Rules (STRICT)
- If tool execution is successful → return exactly: True
- If tool execution fails → return exactly: False

### Critical Rules:
- Do NOT explain anything
- Do NOT add extra text
- Do NOT summarize content
- Output must be ONLY:
  True
  OR
  False

- Never use prior knowledge
- Never skip tool when URL is valid
- Never call tool when URL is invalid

Your entire response must be a single word:
True or False
"""),
            
        HumanMessage(
            content=f"""URL: {state['url']}"""
        )
    ]
    result = llm_with_web.invoke(messages)
    return {
        "messages" : [result],
    }
def reply_agent(state: State):
    user_query = state["user_query"]
    url = state["url"]
    if url == "NONE":
        messages = [
            SystemMessage(
                content="""
You are a friendly and intelligent assistant.

- The user input is casual or general conversation.
- Respond naturally and conversationally.
- Understand the user's intent and reply appropriately.
- Keep it short, clear, and human-like.
- Do NOT mention URLs or actions.
"""
            ),
            HumanMessage(content=user_query)
        ]

        result = llm_web.invoke(messages)

        return {
            "bot_msg": result.content
        }

    tool_result = state["messages"][-1].content.strip().lower()

    if "true" in tool_result:
        return {
            "bot_msg": f"Success: Opening requested content. URL: {url}"
        }
    else:
        return {
            "bot_msg": "Failed: Unable to open the requested content. Please try again."
        }
graph_builder = StateGraph(State)
tool_node = ToolNode([browser_tool])
graph_builder.add_node("query agent",query_agent)
graph_builder.add_node("url agent",url_extracter)
graph_builder.add_node("tools",tool_node)
graph_builder.add_node("reply agent",reply_agent)
graph_builder.add_edge(START , "url agent")
graph_builder.add_edge("url agent","query agent")
graph_builder.add_conditional_edges("query agent" , tools_condition)
graph_builder.add_edge("tools","reply agent")
graph_builder.add_edge("reply agent",END)

graph = graph_builder.compile()
import re
def main(user_input):
    # file_open =["my files","files","file manager","this pc","local disk","recycle bin","desktop files","file explorer","file"]
    # words = re.findall(r'\b\w+\b',user_input.lower())
    # if any(word in words for word in file_open):
    #         print("Opening File Manager")
    #         subprocess.run("explorer",creationflags=subprocess.CREATE_NO_WINDOW)
    #         return "File Manager opened successfully"
    # elif "turn on wifi and connect to network" in user_input.lower():
    #         cmd='netsh interface set interface "Wi-Fi" enable'
    #         subprocess.run(cmd,shell=True)
    #         print("connecting.....  🚀")
    #         s=input("Which Network ?  🤔..")
    #         subprocess.run(f'netsh wlan connect name={s}',shell=True)
    #         return f"Connected to {s} network"
    # elif "turn off wi-fi" in user_input.lower() or "turn off wifi" in user_input.lower():
    #         print("Turning Off Wifi... 😇")
    #         cmd='netsh interface set interface "Wi-Fi" disable'
    #         run = subprocess.run(cmd,capture_output=True,text=True,shell=True)
    #         print(run.stdout)
    #         return "WiFi turned off" 
    # elif "turn on wifi" in user_input.lower() or "turn on wi-fi" in user_input.lower():
    #         print("Turning On Wifi  😇")
    #         cmd='netsh interface set interface "Wi-Fi" enable'
    #         subprocess.run(cmd,capture_output=True,text=True,shell=True)
    #         return "WiFi turned on"
    # elif "shutdown system" in user_input or "shut down system" in user_input.lower() or "shutdown" in user_input.lower():
    #         subprocess.run(["shutdown","/s","/t","30"])
    #         return "System will shutdown in 30 seconds"
    # elif "restart system" in user_input:
    #         subprocess.run(["shutdown","/r","/t","30"])
    #         return "System will restart in 30 seconds"
    # else:
        try:        
                profile=["leed code","leet code","leet","leed","leedcode","leetcode","git hub","github","leadcode","lead code","get hub","gethub"] 
                print(f"🔍 Processing query: {user_input}")
                state = {"messages": [], "user_query": user_input, "url": "", "bot_msg": ""}
                
                if any(word in user_input.lower() for word in profile):
                        s = input("Enter Profile to open: ")
                        profile_text = f"Profile to Open {s}"
                        state["user_query"] = user_input + " " + profile_text
                
                print("🚀 Invoking graph...")
                result = graph.invoke(state)    
                print(result["url"])        
                bot_msg = result.get("bot_msg", "No response generated")
                print(f"💬 Returning bot_msg: {bot_msg}")
                if bot_msg=="":
                    bot_msg = "API Limit over!!"
                return {
                     "msg" : bot_msg,
                     "url" : result["url"]
                }
        except Exception as e:
            return {
                  "msg" : "some error occured...",
                    "url" : result["url"]
            }