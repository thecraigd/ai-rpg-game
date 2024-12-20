# AI RPG Adventure Game 🎮

A modern web-based RPG powered by advanced AI technology, delivering dynamic and personalized gaming experiences through the Llama 3 70B language model.

## 🌟 Features

- **AI-Powered Storytelling**: Utilizes Meta's Llama 3 70B model through the Together API to generate dynamic, contextual responses to player actions
- **Real-Time Interaction**: Seamless interface for player commands and game responses
- **Serverless Architecture**: Built on AWS Lambda for scalable, cost-effective backend operations
- **Cross-Origin Resource Sharing**: Configured for secure cross-domain communication
- **Error Handling**: Robust error management for API calls and game state operations

## 🛠️ Technology Stack

### Frontend
- HTML5
- CSS3
- JavaScript (Vanilla)
- Responsive Design

### Backend
- Python 3.9
- FastAPI
- Mangum (AWS Lambda handler)
- Together AI API
- Serverless Framework

### Infrastructure
- AWS Lambda
- API Gateway
- Docker (for lambda layer management)

## 🚀 Getting Started

### Prerequisites
- Node.js and npm
- Python 3.9
- AWS CLI configured with appropriate credentials
- Together AI API key

### Installation

1. Clone the repository
```bash
git clone https://github.com/thecraigd/ai-rpg-game.git
cd ai-rpg
```

2. Install backend dependencies
```bash
cd backend
pip install -r requirements.txt
```

3. Set up environment variables
```bash
# Add your Together AI API key to your environment
export TOGETHER_API_KEY='your-api-key'
```

4. Deploy the backend
```bash
serverless deploy
```

5. Configure the frontend
- Update the API endpoint in `frontend/game-client.js` with your deployed API Gateway URL
- Serve the frontend files using your preferred web server

## 🎮 Usage

1. Open the game in your web browser
2. Click "Start New Game" to begin
3. Enter commands in the text input to interact with the game
4. Receive AI-generated responses based on your actions

## 🏗️ Project Structure

```
ai-rpg/
├── backend/
│   ├── app/
│   ├── lambda-layer/
│   ├── handler.py        # Main FastAPI application
│   ├── requirements.txt  # Python dependencies
│   └── serverless.yml    # AWS Lambda configuration
├── frontend/
│   ├── index.html       # Game interface
│   ├── styles.css       # Game styling
│   ├── game-client.js   # Game logic
│   └── interface.js     # UI interactions
└── package.json
```

## 🔧 API Endpoints

### POST /api/game/action
Process player actions and generate game responses.

**Request Body:**
```json
{
  "message": "string",
  "history": [["string", "string"]],
  "game_state": {
    "world": "string",
    "station": "string",
    "town": "string",
    "character": "string",
    "start": "string"
  }
}
```

## 🛡️ Security

- CORS configuration limits access to specified origins
- Environment variables used for sensitive data
- API Gateway authentication and authorization
- Input validation using Pydantic models

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🎯 Future Improvements

- Add user authentication
- Implement save game functionality
- Expand the game world and possible interactions
- Add multiplayer capabilities
- Enhance error handling and recovery
- Implement game state persistence

## 👨‍💻 Developer

Craig Dickson
- Portfolio: [craigdoesdata.com](https://www.craigdoesdata.com)
- GitHub: [@yourusername](https://github.com/thecraigd)

---

*Note: This is a portfolio project demonstrating full-stack development skills, API integration, and cloud infrastructure management.*