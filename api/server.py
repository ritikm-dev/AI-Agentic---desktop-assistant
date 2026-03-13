from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from .Web import main
app = FastAPI()
origin = [
        "http://localhost:5173",
        "https://ai-agentic-desktop-assistant.vercel.app/",
        "https://ai-agentic-desktop-assistant.onrender.com",
]
app.add_middleware(
        CORSMiddleware,
        allow_origins = ["*"],
        allow_credentials=True,
        allow_headers =["*"],
        allow_methods = ["*"]
)
class Root_Message(BaseModel):
        user_input : str
app.mount("/assets",StaticFiles(directory="dist/assets",html=True),name="assets")
@app.get("/")
def serve():
        return FileResponse("dist/index.html")
@app.get("/{path : path}")
async def catch_all(path : str):
        return FileResponse("dist/index.html")



@app.get("/")
async def root():
        return {
                "message" : "hi"
        }
@app.post("/usermsg")
async def root_post(data : dict):
        try:
                msg = data["user_msg"]
                print(msg)
                if msg!="":
                        bot_response = main(msg)
                        print(f"bot msg : {bot_response}")
                if bot_response["url"] == "not open":
                        return {
                        "message" : "recieved",
                        "bot_msg" : bot_response["msg"],
                        "url" : "not open"
                }
                else:
                        return {
                                "message" : "recieved",
                                "bot_msg" : bot_response["msg"],
                                "url" : bot_response["url"]
                        }
        except Exception as e:
                return {
                        "message" : "recieved",
                        "bot_msg" : bot_response["msg"],
                        "url" : "not open"
                }