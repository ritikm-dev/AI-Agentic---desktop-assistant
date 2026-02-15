from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from Web import main
app = FastAPI()
origin = [
        "http://localhost:5173",
        "http://localhost:5173/"
]
app.add_middleware(
        CORSMiddleware,
        allow_origins = origin,
        allow_credentials=True,
        allow_headers =["*"],
        allow_methods = ["*"]
)
class Root_Message(BaseModel):
        user_input : str

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
                        print(bot_response)
                return {
                        "message" : "recieved",
                        "bot_msg" : bot_response 
                }
        except Exception as e:
                return "Some error has happened please check your connection"