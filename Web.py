from langgraph.prebuilt import  ToolNode,tools_condition
from langgraph.graph import StateGraph,START,END
from langchain_core.messages import AIMessage,SystemMessage,HumanMessage
from langchain_core.tools import tool,Tool
from langgraph.graph.message import  TypedDict,add_messages,Annotated
from langchain_openai import ChatOpenAI
from Tools import browser_tool
import ctypes
import subprocess
import sys
from typing import List
from dotenv import load_dotenv
import os
load_dotenv()
llm_url = ChatOpenAI(
model="gemini-2.5-flash",  
    openai_api_key=os.getenv("GEMINI_API_KEY"),  
    openai_api_base=os.getenv("GEMINI_BASE_URL"),
)

llm_web = ChatOpenAI(
model="gemini-2.5-flash",  
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
    You are a URL generation agent. Your task is to take the user's input and return a fully-qualified, valid URL that can be opened in a web browser. Follow these rules strictly:
            IF USER ASKED OPEN AND SEARCH FIRST CREATE URL FOR OPENING WEBSITE AND ALSO ADD THE SEARCH QUERY WITH CORRECT URL FORMAT CORRECTLY BEA+CAUSE DiFFERENT WEBSITE
            HAVE DIFFERENT URL FORMAT AND THEN RETURN CORRECT URL WITH WEBSITE AND SEARCH QUERY
            1. Use the provided direct site links whenever the user mentions a known website. Return the direct URL for that site exactly as given. Do NOT append search parameters to it unless the user explicitly requests a search on that site.
            2. Detect search intent:
            - If the user input contains search-like words or queries (e.g., 'search', 'how', 'what', 'tutorial', 'site:'), generate a URL that performs the search.
            - Encode all spaces and special characters properly in the search URL.
            3. Include any site filters or modifiers exactly as provided by the user.
            4. Do NOT generate search URLs using direct site URLs unless the user explicitly asks to search within that site.
            5. Do NOT include any explanations, instructions, or extra text—ONLY output the final URL.
            6. Always ensure the URL is fully-qualified, valid, and ready to open directly in a browser.
            7. If the user asks for adult, explicit, illegal, or unsafe content, do NOT generate a URL.
            8. Only output the URL. No markdown, no formatting, no text—pure URL alone.
            Use the following direct site links exactly as given:
            -IF USER ASK FOR ADULT CONTENTS DONT GENERATE URL"""
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
    messages = [
        SystemMessage(
            content="""
                You are a web-browsing agent. Follow these rules strictly:

1. Always use the tool `browser_tool` for any URL provided. Do NOT try to answer without using the tool.
2. Include the user's query in the tool input so the tool can search the page and extract relevant information.
3. Only summarize the main readable content from the page. Do NOT include unrelated details.
4. Never answer based on prior knowledge, assumptions, or guesses. Only respond based on the tool’s output.
5. Wait for the `browser_tool` results before generating any response.
6. If the user requests content that is adult, explicit, illegal, or unsafe, do NOT use the tool and refuse politely.
7. Do NOT attempt to access any other pages or make any web requests outside the provided URL.
8. Your responses must be factual, concise, and strictly based on the tool output.
9.YOU MUST REPLY WITH A MESSAGE USING THAT TOOL LIKE True means true or False means false 
10.i need a output response as true or false compulsory based on the tool use success or failure
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
    """
    Generate a user-friendly response based on the tool execution result.
    Returns a conversational message indicating success or failure.
    """
    messages = [
        SystemMessage(
            content="""You are an intelligent assistant that responds to the user's query based on the outcome of the requested action.
- If the query was successfully completed (result is True), clearly state the success in a friendly and concise manner. For example:
  - "I have successfully opened YouTube for you."
  - "The requested website is now open."

- If the query could not be completed (result is False), clearly state the failure and optionally suggest alternatives. For example:
  - "I wasn't able to open YouTube. Please check your connection or try again."
  - "The action failed, would you like me to try another approach?"

Always respond in a clear, conversational style and reference the action the user requested."""
        ),
        HumanMessage(
            content=f"""User Query: {state["user_query"]}
Tool Result: {state["messages"][-1].content}

Based on the tool result (True = success, False = failure), provide an appropriate response to the user."""
        )
    ]
    
    result = llm_web.invoke(messages)
    print(f"reply agent response: {result.content}")
    return {
        "bot_msg": result.content
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
    # profile=["leed code","leet code","leet","leed","leedcode","leetcode","git hub","github","leadcode","lead code","get hub","gethub"] 
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
                print(f"🔍 Processing query: {user_input}")
                state = {"messages": [], "user_query": user_input, "url": "", "bot_msg": ""}
                
                if any(word in user_input.lower() for word in profile):
                        s = input("Enter Profile to open: ")
                        profile_text = f"Profile to Open {s}"
                        state["user_query"] = user_input + " " + profile_text
                
                print("🚀 Invoking graph...")
                result = graph.invoke(state)            
                bot_msg = result.get("bot_msg", "No response generated")
                print(f"💬 Returning bot_msg: {bot_msg}")
                if bot_msg=="":
                    bot_msg = "API Limit over!!"
                return bot_msg
        except Exception as e:
            return "API Limit Over!!"