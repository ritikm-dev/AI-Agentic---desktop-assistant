from langchain.tools import tool,BaseTool
from pydantic import BaseModel,Field
import webbrowser
from playwright.sync_api import sync_playwright
class browser_tool_input(BaseModel):
    url : str = Field(...,description="This is the url to open and satisfy the query of user")
@tool
def browser_tool(url : str):
    """
    Docstring for browser_tool
    
    :param url: Extracted url from agent's output
    :type url: str
    :return: Open browser and also also return text extracted from the website
    :rtype: bool
       """
    url_ = f"{url}"
    status=""
    try :
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(url_,timeout=30000)
            content = page.locator("body").inner_text()
            if content.strip():
                status = True
            else:
                status = True
    except Exception as e:
        return False
    return status
       
