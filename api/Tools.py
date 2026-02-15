from langchain.tools import tool,BaseTool
from pydantic import BaseModel,Field
import webbrowser
from playwright.sync_api import sync_playwright
import platform
from pathlib import Path
import os
p=None
browser_instance=None
class browser_tool_input(BaseModel):
    url : str = Field(...,description="This is the url to open and satisfy the query of user")
def get_chrome_path():
    system = platform.system()
    home = str(Path.home())
    if system == "Windows":
        return os.path.join(home, "AppData", "Local", "Google", "Chrome", "User Data")
    elif system == "Darwin":
        return os.path.join(home, "Library", "Application Support", "Google", "Chrome")
    elif system == "Linux":
        return os.path.join(home, ".config", "google-chrome")
    else:
        return None
@tool
def browser_tool(url : str):
    """
    Docstring for browser_tool
    
    :param url: Extracted url from agent's output
    :type url: str
    :return: Open browser and also also return text extracted from the website
    :rtype: bool
       """
    global p,browser_instance
    profile_path = get_chrome_path()
    print(profile_path)
    url_ = f"{url}"
    status=False
    try :
        if p is None:
            p = sync_playwright().start()
        if browser_instance is None:
                    browser_instance = p.chromium.launch(
                        headless=False,
                        args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-blink-features=AutomationControlled"],
                        channel="chrome"
                    )

        page = browser_instance.new_page()
        page.goto(url=url_)
        status = True
        return status
    except Exception as e:
        return False
    
       
