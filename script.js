document.getElementById('send-button').addEventListener('click', async function() {
    let userInput = document.getElementById('user-input').value;
    if (userInput) {
        // Display user's message
        let userMessage = document.createElement('div');
        userMessage.classList.add('user-message');
        userMessage.textContent = userInput;
        document.getElementById('chat-box').appendChild(userMessage);

        // Send user input to backend (Flask API) and get bot response
        const botResponse = await sendChatMessage(userInput);

        // Display bot's response
        setTimeout(function() {
            let botMessage = document.createElement('div');
            botMessage.classList.add('bot-message');
            botMessage.textContent = botResponse || "…I don’t know what to say. Everything feels so heavy right now.";
            document.getElementById('chat-box').appendChild(botMessage);

            // Scroll to the bottom
            document.getElementById('chat-box').scrollTop = document.getElementById('chat-box').scrollHeight;
        }, 1000);

        // Clear input field
        document.getElementById('user-input').value = '';
    }
});

// Function to send chat message to the backend
async function sendChatMessage(userInput) {
    const response = await fetch('http://localhost:5000/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_input: userInput }),
    });

    const data = await response.json();
    return data.response;  // Return the response from the backend
}
