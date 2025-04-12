// Chat UI Component
document.addEventListener('DOMContentLoaded', function() {
    // Check if user is logged in
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = 'login.html';
        return;
    }

    // DOM Elements
    const chatMessages = document.getElementById('chat-messages');
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const sendMessageBtn = document.getElementById('send-message-btn');
    const newChatBtn = document.getElementById('new-chat-btn');
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebar = document.querySelector('.sidebar');
    const conversationsList = document.getElementById('conversations-list');
    const userInfo = document.getElementById('user-info');
    const logoutBtn = document.getElementById('logout-btn');
    const conversationTitle = document.getElementById('conversation-title');

    // State
    let currentConversationId = null;
    let conversations = [];
    let user = null;

    // Initialize
    init();

    // Functions
    async function init() {
        try {
            // Get user info
            user = JSON.parse(localStorage.getItem('user'));
            if (user) {
                renderUserInfo();
            }

            // Load conversations
            await loadConversations();

            // Auto-resize textarea
            chatInput.addEventListener('input', function() {
                this.style.height = 'auto';
                this.style.height = (this.scrollHeight) + 'px';
            });

            // Event listeners
            setupEventListeners();
        } catch (error) {
            console.error('Initialization error:', error);
        }
    }

    function setupEventListeners() {
        // Send message
        chatForm.addEventListener('submit', handleSendMessage);

        // New chat
        newChatBtn.addEventListener('click', handleNewChat);

        // Toggle sidebar
        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.toggle('collapsed');
        });

        // Logout
        logoutBtn.addEventListener('click', handleLogout);


    }

    async function loadConversations() {
        try {
            conversations = await getConversations();
            renderConversations();

            // If there are conversations, load the first one
            if (conversations.length > 0) {
                await loadConversation(conversations[0].id);
            } else {
                // Show welcome message
                showWelcomeMessage();
            }
        } catch (error) {
            console.error('Error loading conversations:', error);
        }
    }

    function renderConversations() {
        conversationsList.innerHTML = '';

        if (conversations.length === 0) {
            conversationsList.innerHTML = `
                <div class="empty-conversations">
                    <p>No conversations yet</p>
                </div>
            `;
            return;
        }

        conversations.forEach(conversation => {
            const conversationItem = document.createElement('div');
            conversationItem.className = 'conversation-item';
            if (currentConversationId === conversation.id) {
                conversationItem.classList.add('active');
            }

            conversationItem.innerHTML = `
                <div class="conversation-title">${conversation.title}</div>
            `;

            conversationItem.addEventListener('click', () => loadConversation(conversation.id));

            conversationsList.appendChild(conversationItem);
        });
    }

    async function loadConversation(id) {
        try {
            const conversation = await getConversation(id);
            currentConversationId = conversation.id;
            conversationTitle.textContent = conversation.title;

            // Render messages
            renderMessages(conversation.messages);

            // Update active conversation in sidebar
            const conversationItems = document.querySelectorAll('.conversation-item');
            conversationItems.forEach(item => {
                item.classList.remove('active');
                if (item.querySelector(`[data-id="${id}"]`)) {
                    item.classList.add('active');
                }
            });

            // Hide welcome message
            const welcomeMessage = document.querySelector('.welcome-message');
            if (welcomeMessage) {
                welcomeMessage.style.display = 'none';
            }
        } catch (error) {
            console.error('Error loading conversation:', error);
        }
    }

    function renderMessages(messages) {
        chatMessages.innerHTML = '';

        if (messages.length === 0) {
            return;
        }

        messages.forEach(message => {
            appendMessage(message);
        });

        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function appendMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = `message message-${message.role === 'user' ? 'user' : 'assistant'}`;

        messageElement.innerHTML = `
            <div class="message-content">${message.content}</div>
        `;

        chatMessages.appendChild(messageElement);

        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function showWelcomeMessage() {
        chatMessages.innerHTML = `
            <div class="welcome-message">
                <h2>Welcome to AI Assistant</h2>
                <p>Start a conversation by typing a message below.</p>
            </div>
        `;
        conversationTitle.textContent = 'New Conversation';
        currentConversationId = null;
    }

    function renderUserInfo() {
        if (!user) return;

        const initials = user.name.split(' ').map(n => n[0]).join('').toUpperCase();

        userInfo.innerHTML = `
            <div class="user-avatar">${initials}</div>
            <div class="user-name">${user.name}</div>
        `;
    }

    async function handleSendMessage(e) {
        e.preventDefault();

        const message = chatInput.value.trim();
        if (!message) return;

        try {
            // Clear input
            chatInput.value = '';
            chatInput.style.height = 'auto';

            // If no conversation, create one
            if (!currentConversationId) {
                // Show user message immediately
                appendMessage({
                    role: 'user',
                    content: message
                });

                // Send message to API
                const response = await sendMessage(message);

                // Get the conversation ID from the response
                if (response && response.length > 0) {
                    const userMessage = response[0];
                    currentConversationId = userMessage.conversation_id;

                    // Append AI response
                    appendMessage(response[1]);

                    // Reload conversations to get the new one
                    await loadConversations();
                }
            } else {
                // Show user message immediately
                appendMessage({
                    role: 'user',
                    content: message
                });

                // Send message to API with conversation ID
                const response = await sendMessage(message, currentConversationId);

                // Append AI response
                if (response && response.length > 0) {
                    appendMessage(response[1]);
                }
            }
        } catch (error) {
            console.error('Error sending message:', error);
        }
    }

    async function handleNewChat() {
        currentConversationId = null;
        showWelcomeMessage();
    }

    function handleLogout() {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = 'login.html';
    }


});
