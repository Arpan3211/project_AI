// Chat Component

// Initialize chat functionality
function initChat() {
    const chatInput = document.getElementById('chat-input');
    const sendButton = document.getElementById('send-btn');
    const chatMessages = document.getElementById('chat-messages');
    const welcomeMessage = document.querySelector('.welcome-message');
    let isFirstMessage = true;

    // Expose the reset function to the global scope
    window.resetChatState = function() {
        isFirstMessage = true;
    };
    // Send message when button is clicked
    sendButton.addEventListener('click', sendMessage);

    // Send message when Enter key is pressed
    chatInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // Voice button functionality removed as requested

    // Function to send message
    function sendMessage() {
        const message = chatInput.value.trim();

        if (message === '') return;

        // Hide welcome message on first message
        if (isFirstMessage && welcomeMessage) {
            welcomeMessage.classList.add('hidden');
            isFirstMessage = false;
        }

        // Add user message to chat
        addMessageToChat('user', message);

        // Clear input
        chatInput.value = '';

        // Show typing indicator
        showTypingIndicator();

        // Send message to API
        apiService.sendMessage(message)
            .then(response => {
                // Remove typing indicator
                removeTypingIndicator();

                // Add bot response to chat
                addMessageToChat('bot', response.message);
            })
            .catch(error => {
                // Remove typing indicator
                removeTypingIndicator();

                // Add error message
                addMessageToChat('bot', 'Sorry, I encountered an error. Please try again.');
                console.error('Error:', error);
            });
    }

    // Function to add message to chat
    function addMessageToChat(sender, content) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', sender);

        const messageContent = document.createElement('div');
        messageContent.classList.add('message-content');
        messageContent.textContent = content;

        messageElement.appendChild(messageContent);
        chatMessages.appendChild(messageElement);

        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Function to show typing indicator
    function showTypingIndicator() {
        const typingElement = document.createElement('div');
        typingElement.classList.add('message', 'bot', 'typing-indicator');

        const typingContent = document.createElement('div');
        typingContent.classList.add('message-content');
        typingContent.innerHTML = '<span>.</span><span>.</span><span>.</span>';

        typingElement.appendChild(typingContent);
        chatMessages.appendChild(typingElement);

        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Function to remove typing indicator
    function removeTypingIndicator() {
        const typingIndicator = document.querySelector('.typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
}
