class GameClient {
    constructor(apiEndpoint) {
        this.apiEndpoint = apiEndpoint;
        this.history = [];
        this.gameState = null;
    }

    async startGame() {
        // Initialize game state
        this.gameState = {
            world: "A mysterious cyberpunk world where advanced technology meets mystical forces. Neon lights pierce through the perpetual haze while ancient spirits drift through digital realms.",
            station: "Nexus Station 7, a sprawling space station that serves as a gateway between Earth's colonies and deep space. It's a melting pot of cultures, technologies, and species.",
            town: "The Chrome District, a bustling neighborhood where street vendors sell augmented reality experiences alongside traditional street food. Holographic advertisements float above the crowded streets.",
            character: "A skilled tech-shaman, capable of manipulating both technology and spiritual energies. You wear a weathered synth-leather jacket adorned with glowing circuit patterns.",
            start: "You find yourself standing in a dimly lit alley of the Chrome District. The neon signs above cast a rainbow of colors across the wet pavement. What would you like to do?"
        };

        this.history = [];

        try {
            const response = await this.sendAction("start game");
            return response;
        } catch (error) {
            console.error("Error starting the game:", error);
            throw error;
        }
    }

    async sendAction(message) {
        try {
            const payload = {
                message: message,
                history: this.history,
                game_state: this.gameState
            };

            console.log("Sending request with payload:", payload);

            const response = await fetch(`${this.apiEndpoint}/api/game/action`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                credentials: "include",
                body: JSON.stringify(payload)
            });

            console.log("Response status:", response.status);

            if (!response.ok) {
                const errorText = await response.text();
                console.error("Error response:", errorText);
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            // Add to history only if it's not the "start game" message
            if (message.toLowerCase() !== "start game") {
                this.history.push([data.response, message]);
            }

            return data.response;
        } catch (error) {
            console.error("Detailed request error:", error);
            throw error;
        }
    }
}