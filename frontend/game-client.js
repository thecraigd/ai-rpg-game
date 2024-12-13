class GameClient {
    constructor(apiEndpoint) {
        this.apiEndpoint = apiEndpoint;
        this.history = [];
        this.gameState = null;
    }

    async startGame() {
        // Initialize with your game state
        this.gameState = {
            world: "Your world description",  // Replace with actual world data
            station: "Your station description",
            town: "Your town description",
            character: "Your character description",
            start: "Your start message"
        };

        this.history = [];
        return "Welcome to the AI RPG Adventure. Type 'start game' to begin.";
    }

    async sendAction(message) {
        try {
            const response = await fetch(`${this.apiEndpoint}/api/game/action`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    history: this.history,
                    game_state: this.gameState
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            this.history.push([message, data.response]);
            return data.response;
        } catch (error) {
            console.error('Error:', error);
            throw error;
        }
    }
}