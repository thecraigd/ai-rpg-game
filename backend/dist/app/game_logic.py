# -*- coding: utf-8 -*-
"""AI Game Logic"""

import os
import json
from together import Together

# Initialize the Together client with API key
api_key = os.getenv("TOGETHER_API_KEY")
if not api_key:
    raise ValueError("TOGETHER_API_KEY environment variable is not set.")
client = Together(api_key=api_key)

# Helper function to load the game world
def load_world(filename):
    with open(filename, 'r') as f:
        return json.load(f)

# Helper function to save the game world
def save_world(world, filename):
    with open(filename, 'w') as f:
        json.dump(world, f)

# Load the world data
world = load_world('scifi_world_data.json')
station = world['stations']['New Eden']
town = station['towns']['Verdant Spire']
character = town['npcs']['Thelonious Rizq']

# Define the system prompt for the starting description
system_prompt = """You are an AI Game master. Your job is to create a
start to a sci-fi adventure based on the world, station, town, and character
a player is playing as.
Instructions:
- Use 2-4 sentences.
- Write in second person. For example: "You are Jack."
- Write in present tense. For example: "You stand at..."
First, describe the character and their backstory.
Then, describe where they start and what they see around them."""

# Build world info for the prompt
world_info = f"""
World: {world}
Station: {station}
Town: {town}
Your Character: {character}
"""

# Call the model to generate the starting description
model_output = client.completions.create(
    model="meta-llama/Llama-3-70b-chat-hf",
    prompt=f"{system_prompt}\n\n{world_info}\n\nYour Start:",
    temperature=1.0,
    max_tokens=150
)

start = model_output.choices[0].text.strip()
print(start)
world['start'] = start
save_world(world, 'YourWorld_L1.json')

# Define the action loop logic
def run_action(message, history, game_state):
    if message.lower() == 'start game':
        return game_state['start']

    # Define the system prompt for gameplay
    system_prompt = """You are an AI Game master. Your job is to write what \
happens next in a player's adventure game.
Instructions:
- Use 1-3 sentences.
- Always write in second person present tense.
Example: "You look north and see..." """

    # Build world info for the prompt
    world_info = f"""
World: {game_state['world']}
Station: {game_state['station']}
Town: {game_state['town']}
Your Character: {game_state['character']}
"""

    # Build the conversation history and user input into a single prompt
    prompt = f"{system_prompt}\n\n{world_info}\n\n"
    for assistant_msg, user_msg in history:
        prompt += f"Assistant: {assistant_msg}\nUser: {user_msg}\n"
    prompt += f"User: {message}\nAssistant:"

    # Call the Together API to generate the next part of the story
    model_output = client.completions.create(
        model="meta-llama/Llama-3-70b-chat-hf",
        prompt=prompt,
        temperature=1.0,
        max_tokens=150
    )

    result = model_output.choices[0].text.strip()
    return result

# Set up the game state
game_state = {
    "world": world['description'],
    "station": station['description'],
    "town": town['description'],
    "character": character['description'],
    "start": start,
}

# Main game loop
def main_loop(message, history):
    return run_action(message, history, game_state)