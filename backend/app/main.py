# backend/app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import json
import os
from together import Together
from mangum import Mangum  # For AWS Lambda compatibility

app = FastAPI()
handler = Mangum(app)  # AWS Lambda handler

# Initialize Together client
together_client = Together()

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

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

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
        
        model_output = together_client.chat.completions.create(
            model="meta-llama/Llama-3-70b-chat-hf",
            messages=messages
        )

        return {"response": model_output.choices[0].message.content}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# For local testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
