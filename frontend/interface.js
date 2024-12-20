document.addEventListener("DOMContentLoaded", () => {
    // Initialize game client with your API endpoint
    const gameClient = new GameClient("https://9cv8i9onw2.execute-api.eu-central-1.amazonaws.com/dev");

    // Get DOM elements
    const chatbox = document.getElementById("chatbox");
    const playerInput = document.getElementById("playerInput");
    const sendButton = document.getElementById("sendAction");
    const startButton = document.getElementById("startGame");

    // Function to append messages to the chat
    function appendMessage(message, isPlayer = false) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("message");
        messageDiv.classList.add(isPlayer ? "player-message" : "game-message");
        messageDiv.textContent = message;
        chatbox.appendChild(messageDiv);
        chatbox.scrollTop = chatbox.scrollHeight;
    }

    // Function to handle loading state
    function setLoading(isLoading) {
        playerInput.disabled = isLoading;
        sendButton.disabled = isLoading;
        if (isLoading) {
            sendButton.classList.add("loading");
        } else {
            sendButton.classList.remove("loading");
        }
    }

    // Function to handle player input
    async function handleInput(message) {
        if (!message.trim()) return;

        playerInput.value = "";
        appendMessage(message, true);
        setLoading(true);

        try {
            const response = await gameClient.sendAction(message);
            appendMessage(response);
        } catch (error) {
            appendMessage("Sorry, there was an error processing your action. Please try again.");
            console.error("Error:", error);
        } finally {
            setLoading(false);
        }
    }

    // Event listener for start button
    startButton.addEventListener("click", async () => {
        chatbox.innerHTML = ""; // Clear previous messages
        playerInput.disabled = false;
        sendButton.disabled = false;

        try {
            const startMessage = await gameClient.startGame();
            appendMessage(startMessage);
        } catch (error) {
            appendMessage("Error starting the game. Please try again.");
            console.error("Error:", error);
        }
    });

    // Event listener for send button
    sendButton.addEventListener("click", () => {
        handleInput(playerInput.value);
    });

    // Event listener for Enter key
    playerInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            handleInput(playerInput.value);
        }
    });
});