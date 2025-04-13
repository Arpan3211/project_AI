import { chatApi, authApi } from '../services/api.service.js';

class ChatController {
    constructor() {
        // DOM Elements
        this.chatMessages = document.getElementById('chat-messages');
        this.chatForm = document.getElementById('chat-form');
        this.chatInput = document.getElementById('chat-input');
        this.newChatBtn = document.getElementById('new-chat-btn');
        this.sidebarToggle = document.getElementById('sidebar-toggle');
        this.sidebar = document.querySelector('.sidebar');
        this.conversationsList = document.getElementById('conversations-list');
        this.userInfo = document.getElementById('user-info');
        this.logoutBtn = document.getElementById('logout-btn');
        this.conversationTitle = document.getElementById('conversation-title');

        // State
        this.conversations = [];
        this.currentConversationId = null;
        this.isInitialized = false;

        // Bind methods to this instance
        this.init = this.init.bind(this);
        this.loadConversations = this.loadConversations.bind(this);
        this.loadConversation = this.loadConversation.bind(this);
        this.handleSendMessage = this.handleSendMessage.bind(this);
        this.handleNewChat = this.handleNewChat.bind(this);
        this.handleLogout = this.handleLogout.bind(this);
        this.renderConversations = this.renderConversations.bind(this);
        this.renderMessages = this.renderMessages.bind(this);
        this.showWelcomeMessage = this.showWelcomeMessage.bind(this);
        this.loadUserInfo = this.loadUserInfo.bind(this);
    }

    // Initialize the chat UI
    async init() {
        try {
            // Check if user is authenticated
            const token = localStorage.getItem('token');
            if (!token) {
                window.location.href = 'login.html';
                return;
            }

            // Load user info
            await this.loadUserInfo();

            // Check URL for conversation ID
            const urlParams = new URLSearchParams(window.location.search);
            const conversationId = urlParams.get('id');

            // Load conversations
            await this.loadConversations();

            // If conversation ID is in URL, load that conversation
            if (conversationId) {
                // Find by conversation_id (UUID string)
                const conversation = this.conversations.find(c => c.conversation_id === conversationId);

                if (conversation) {
                    // Use conversation_id (UUID) for loading
                    await this.loadConversation(conversation.conversation_id);
                } else {
                    // If conversation not found, clear the URL parameter
                    this.updateUrlWithConversationId(null);
                }
            }

            // Add event listeners
            if (this.chatForm) {
                this.chatForm.addEventListener('submit', this.handleSendMessage);
            } else {
                console.error('Chat form not found');
            }

            if (this.newChatBtn) {
                this.newChatBtn.addEventListener('click', this.handleNewChat);
            }

            if (this.logoutBtn) {
                this.logoutBtn.addEventListener('click', this.handleLogout);
            }

            if (this.sidebarToggle && this.sidebar) {
                this.sidebarToggle.addEventListener('click', () => {
                    this.sidebar.classList.toggle('collapsed');
                });
            }

            // Handle browser back/forward navigation
            window.addEventListener('popstate', this.handlePopState.bind(this));

            this.isInitialized = true;
        } catch (error) {
            console.error('Error initializing chat:', error);
        }
    }

    // Handle browser back/forward navigation
    async handlePopState(event) {
        const state = event.state;
        if (state && state.conversationId) {
            await this.loadConversation(state.conversationId);
        } else {
            // If no state or no conversation ID, show welcome message
            this.showWelcomeMessage();
        }
    }

    // Update URL with conversation ID
    updateUrlWithConversationId(conversationId) {
        // Use the conversation_id (UUID) for the URL if available
        const url = conversationId
            ? `${window.location.pathname}?id=${conversationId}`
            : window.location.pathname;

        window.history.pushState(
            { conversationId },
            '',
            url
        );
    }

    // Load user information
    async loadUserInfo() {
        try {
            const userData = localStorage.getItem('user');
            if (userData) {
                const user = JSON.parse(userData);
                this.userInfo.innerHTML = `
                    <div class="user-avatar">${user.name.charAt(0)}</div>
                    <div class="user-name">${user.name}</div>
                `;
            } else {
                // Fetch user data if not in localStorage
                const user = await authApi.getProfile();
                localStorage.setItem('user', JSON.stringify(user));
                this.userInfo.innerHTML = `
                    <div class="user-avatar">${user.name.charAt(0)}</div>
                    <div class="user-name">${user.name}</div>
                `;
            }
        } catch (error) {
            console.error('Error loading user info:', error);
        }
    }

    // Load all conversations
    async loadConversations() {
        try {
            this.conversations = await chatApi.getConversations();
            this.renderConversations();

            // If there are conversations, load the first one
            if (this.conversations.length > 0) {
                await this.loadConversation(this.conversations[0].conversation_id);
            } else {
                // Show welcome message
                this.showWelcomeMessage();
            }
        } catch (error) {
            console.error('Error loading conversations:', error);
        }
    }

    // Load a specific conversation
    async loadConversation(conversationId) {

        try {
            const conversation = await chatApi.getConversation(conversationId);
            this.currentConversationId = conversation.conversation_id;
            this.conversationTitle.textContent = conversation.title;

            // Update URL with conversation ID (UUID)
            this.updateUrlWithConversationId(conversation.conversation_id);

            // Render messages
            this.renderMessages(conversation.messages);

            // Update active conversation in sidebar
            const conversationItems = document.querySelectorAll('.conversation-item');
            conversationItems.forEach(item => {
                item.classList.remove('active');
                if (item.dataset.id === this.currentConversationId) {
                    item.classList.add('active');
                }
            });

            // Hide welcome message
            const welcomeMessage = document.querySelector('.welcome-message');
            if (welcomeMessage) {
                welcomeMessage.style.display = 'none';
            }

            // Show chat messages container
            if (this.chatMessages) {
                this.chatMessages.style.display = 'flex';
            }
        } catch (error) {
            console.error('Error loading conversation:', error);
        }
    }

    // Render conversations in the sidebar
    renderConversations() {
        this.conversationsList.innerHTML = '';

        if (this.conversations.length === 0) {
            this.conversationsList.innerHTML = `
                <div class="empty-conversations">
                    <p>No conversations yet</p>
                </div>
            `;
            return;
        }

        this.conversations.forEach(conversation => {
            const conversationItem = document.createElement('div');
            conversationItem.className = 'conversation-item';
            conversationItem.dataset.id = conversation.conversation_id;

            if (this.currentConversationId === conversation.conversation_id) {
                conversationItem.classList.add('active');
            }

            // Ensure the title is properly escaped for HTML
            const title = conversation.title || 'New Conversation';

            conversationItem.innerHTML = `
                <div class="conversation-title" title="${this.escapeHtml(title)}">${this.escapeHtml(title)}</div>
            `;

            conversationItem.addEventListener('click', () => this.loadConversation(conversation.conversation_id));

            this.conversationsList.appendChild(conversationItem);
        });
    }

    // Render messages in the chat area
    renderMessages(messages) {
        this.chatMessages.innerHTML = '';

        messages.forEach(message => {
            const messageElement = document.createElement('div');
            messageElement.className = `message ${message.role}`;

            messageElement.innerHTML = `
                <div class="message-content">${this.formatMessageContent(message.content)}</div>
            `;

            this.chatMessages.appendChild(messageElement);
        });

        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    // Format message content (convert newlines to <br>, etc.)
    formatMessageContent(content) {
        return content
            .replace(/\\n/g, '\n')
            .replace(/\n/g, '<br>')
            .replace(/```(.*?)```/gs, (_match, code) => {
                return `<pre><code>${code}</code></pre>`;
            });
    }

    // Escape HTML to prevent XSS
    escapeHtml(text) {
        if (!text) return '';
        return text
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }

    showWelcomeMessage() {
        this.updateUrlWithConversationId(null);

        const welcomeMessage = document.createElement('div');
        welcomeMessage.className = 'welcome-message';
        welcomeMessage.innerHTML = `
            <h2>Welcome to AI Assistant</h2>
            <p>Start a conversation by typing a message below.</p>
        `;

        if (this.chatMessages) {
            this.chatMessages.innerHTML = '';
            this.chatMessages.appendChild(welcomeMessage);
            this.chatMessages.style.display = 'block';
        }

        this.currentConversationId = null;
        if (this.conversationTitle) {
            this.conversationTitle.textContent = 'New Conversation';
        }
    }

    // Handle sending a message
    async handleSendMessage(e) {
        e.preventDefault();
        e.stopPropagation();


        if (!this.chatInput) return;

        const message = this.chatInput.value.trim();
        if (!message) return;

        // Clear input
        this.chatInput.value = '';

        try {
            // Make sure chat messages container is visible and using flex layout
            if (this.chatMessages) {
                this.chatMessages.style.display = 'flex';

                // Hide welcome message if visible
                const welcomeMessage = document.querySelector('.welcome-message');
                if (welcomeMessage) {
                    welcomeMessage.style.display = 'none';
                }

                // Add user message to UI immediately
                const userMessageElement = document.createElement('div');
                userMessageElement.className = 'message user';
                userMessageElement.innerHTML = `
                    <div class="message-content">${this.formatMessageContent(message)}</div>
                `;
                this.chatMessages.appendChild(userMessageElement);

                // Scroll to bottom
                this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
            }

            let response;

            if (!this.currentConversationId) {
                // Create new conversation
                response = await chatApi.sendMessage(message);

                // Update conversation ID and title
                const conversation = response.conversation;
                this.currentConversationId = conversation.conversation_id;

                if (this.conversationTitle) {
                    // Use the conversation title from the backend (which is now the first message)
                    this.conversationTitle.textContent = conversation.title || 'New Conversation';
                }

                // Update URL with the new conversation ID (UUID)
                this.updateUrlWithConversationId(conversation.conversation_id);

                // Reload conversations to update sidebar
                await this.loadConversations();
            } else {
                // Send message to existing conversation (using UUID)
                response = await chatApi.sendMessage(message, this.currentConversationId);
            }

            if (this.chatMessages) {
                // Get the AI response message (second message in the array)
                const aiMessage = response.messages[1];

                // Add AI response to UI
                const aiMessageElement = document.createElement('div');
                aiMessageElement.className = 'message assistant';
                aiMessageElement.innerHTML = `
                    <div class="message-content">${this.formatMessageContent(aiMessage.content)}</div>
                `;
                this.chatMessages.appendChild(aiMessageElement);

                // Scroll to bottom
                this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
            }
        } catch (error) {
            console.error('Error sending message:', error);

            if (this.chatMessages) {
                // Show error message
                const errorElement = document.createElement('div');
                errorElement.className = 'message error';
                errorElement.innerHTML = `
                    <div class="message-content">Error: ${error.message}</div>
                `;
                this.chatMessages.appendChild(errorElement);

                // Scroll to bottom
                this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
            }
        }
    }

    // Handle creating a new chat
    async handleNewChat() {
        try {
            // Show welcome message and clear URL
            this.showWelcomeMessage();

            // No need to create a conversation yet - it will be created when the first message is sent
            // This allows the backend to generate a UUID when needed
        } catch (error) {
            console.error('Error creating new chat:', error);
        }
    }

    // Handle logout
    async handleLogout() {
        try {
            await authApi.logout();
            window.location.href = 'login.html';
        } catch (error) {
            console.error('Error logging out:', error);
        }
    }
}

// Initialize controller when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const chatController = new ChatController();
    chatController.init();
});

export default ChatController;
