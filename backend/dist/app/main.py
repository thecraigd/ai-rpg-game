# backend/app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from typing import List
import os
from together import Together
from mangum import Mangum  # For AWS Lambda compatibility

app = FastAPI()
handler = Mangum(app)  # AWS Lambda handler

# Initialize Together client
API_KEY = os.getenv("TOGETHER_API_KEY")
if not API_KEY:
    raise ValueError("TOGETHER_API_KEY environment variable is not set.")
together_client = Together(api_key=API_KEY)


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
        # Handle "start game" command
        if game_action.message.lower() == "start game":
            return {"response": game_action.game_state.start}

        # Define the system prompt
        system_prompt = """You are an AI Game master. Your job is to write what \
happens next in a player's adventure game.\
Instructions: \
You must only write 1-3 sentences in response. \
Always write in second person present tense. \
Ex. (You look north and see...)"""

        # Add game-specific world information
        world_info = f"""
        World: {game_action.game_state.world}
        Station: {game_action.game_state.station}
        Town: {game_action.game_state.town}
        Your Character: {game_action.game_state.character}
        """

        # Build the prompt with history
        prompt = f"{system_prompt}\n\n{world_info}\n\n"
        for assistant_msg, user_msg in game_action.history:
            prompt += f"Assistant: {assistant_msg}\nUser: {user_msg}\n"
        prompt += f"User: {game_action.message}\nAssistant:"

        # Call the Together API
        model_output = together_client.completions.create(
            model="meta-llama/Llama-3-70b-chat-hf",
            prompt=prompt,
            temperature=1.0,
            max_tokens=150
        )

        # Return the response
        return {"response": model_output.choices[0].text.strip()}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# For local testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)