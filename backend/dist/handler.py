import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from pydantic import BaseModel, field_validator
from typing import List
from together import Together

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.craigdoesdata.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Initialize Together client with API key from environment variable
API_KEY = os.getenv("TOGETHER_API_KEY")
if not API_KEY:
    raise ValueError("TOGETHER_API_KEY environment variable is not set.")
client = Together(api_key=API_KEY)


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
        # Handle "start game" command
        if game_action.message.lower() == 'start game':
            return {"response": game_action.game_state.start}

        # Define the system prompt
        system_prompt = """You are an AI Game master. Your job is to write what happens next in a player's adventure game.
        Instructions:
        - Use 1-3 sentences per response.
        - Always write in second person present tense.
        Example: (You look north and see...)"""

        # Add game-specific world information
        world_info = f"""
        World: {game_action.game_state.world}
        Station: {game_action.game_state.station}
        Town: {game_action.game_state.town}
        Your Character: {game_action.game_state.character}
        """

        # Build the prompt for the Together API
        prompt = f"{system_prompt}\n\n{world_info}\n\n"
        for assistant_msg, user_msg in game_action.history:
            prompt += f"Assistant: {assistant_msg}\nUser: {user_msg}\n"
        prompt += f"User: {game_action.message}\nAssistant:"

        # Call Together API using completions endpoint
        try:
            response = client.completions.create(
                model="meta-llama/Llama-3-70b-chat-hf",
                prompt=prompt,
                temperature=1.0,
                max_tokens=150
            )
            # Return the AI's response
            return {"response": response.choices[0].text.strip()}
        except Exception as api_error:
            print(f"Together API Error: {str(api_error)}")
            raise HTTPException(status_code=500, detail=f"Together API Error: {str(api_error)}")

    except Exception as e:
        # Log the error and return a generic failure message
        print(f"Error processing action: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while processing your action.")


# Handler for AWS Lambda
handler = Mangum(app)