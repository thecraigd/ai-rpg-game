import os
from fastapi import FastAPI, HTTPException
from mangum import Mangum
from pydantic import BaseModel
from typing import List, Optional
import together
import json

app = FastAPI()

# Initialize Together client with API key from environment variable
together.api_key = os.environ.get("TOGETHER_API_KEY")

class GameState(BaseModel):
    world: str
    station: str
    town: str
    character: str
    start: str

class GameAction(BaseModel):
    message: str
    history: List[List[str]] = []
    game_state: GameState

@app.get("/test")
async def read_root():
    return {"message": "Hello from FastAPI!"}

@app.post("/api/game/action")
async def process_action(game_action: GameAction):
    try:
        if game_action.message.lower() == 'start game':
            return {"response": game_action.game_state.start}

        system_prompt = """You are an AI Game master. Your job is to write what \
happens next in a player's adventure game.\
Instructions: \
You must on only write 1-3 sentences in response. \
Always write in second person present tense. \
Ex. (You look north and see...)"""

        world_info = f"""
World: {game_action.game_state.world}
Station: {game_action.game_state.station}
Town: {game_action.game_state.town}
Your Character: {game_action.game_state.character}"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": world_info}
        ]
        
        # Add conversation history
        for action in game_action.history:
            messages.append({"role": "assistant", "content": action[0]})
            messages.append({"role": "user", "content": action[1]})

        messages.append({"role": "user", "content": game_action.message})
        
        model_output = together.Complete.create(
            model="meta-llama/Llama-2-70b-chat-hf",
            messages=messages
        )

        return {"response": model_output.choices[0].message.content}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

handler = Mangum(app)