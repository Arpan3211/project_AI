// Chat Controller
// Handles all chat page functionality

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

            // Load conversations
            await this.loadConversations();

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

            // Toggle sidebar
            if (this.sidebarToggle && this.sidebar) {
                this.sidebarToggle.addEventListener('click', () => {
                    this.sidebar.classList.toggle('collapsed');
                });
            }

            this.isInitialized = true;
        } catch (error) {
            console.error('Error initializing chat:', error);
        }
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
                await this.loadConversation(this.conversations[0].id);
            } else {
                // Show welcome message
                this.showWelcomeMessage();
            }
        } catch (error) {
            console.error('Error loading conversations:', error);
        }
    }

    // Load a specific conversation
    async loadConversation(id) {
        try {
            const conversation = await chatApi.getConversation(id);
            this.currentConversationId = conversation.id;
            this.conversationTitle.textContent = conversation.title;

            // Render messages
            this.renderMessages(conversation.messages);

            // Update active conversation in sidebar
            const conversationItems = document.querySelectorAll('.conversation-item');
            conversationItems.forEach(item => {
                item.classList.remove('active');
                if (parseInt(item.dataset.id) === id) {
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
            conversationItem.dataset.id = conversation.id;

            if (this.currentConversationId === conversation.id) {
                conversationItem.classList.add('active');
            }

            conversationItem.innerHTML = `
                <div class="conversation-title">${conversation.title}</div>
            `;

            conversationItem.addEventListener('click', () => this.loadConversation(conversation.id));

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

        // Scroll to bottom
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

    // Show welcome message
    showWelcomeMessage() {
        const welcomeMessage = document.createElement('div');
        welcomeMessage.className = 'welcome-message';
        welcomeMessage.innerHTML = `
            <h2>Welcome to AI Assistant</h2>
            <p>Start a conversation by typing a message below.</p>
        `;

        this.chatMessages.innerHTML = '';
        this.chatMessages.appendChild(welcomeMessage);
        this.currentConversationId = null;
        this.conversationTitle.textContent = 'New Conversation';
    }

    // Handle sending a message
    async handleSendMessage(e) {
        e.preventDefault();

        const message = this.chatInput.value.trim();
        if (!message) return;

        // Clear input
        this.chatInput.value = '';

        try {
            // Add user message to UI immediately
            const userMessageElement = document.createElement('div');
            userMessageElement.className = 'message user';
            userMessageElement.innerHTML = `
                <div class="message-content">${this.formatMessageContent(message)}</div>
            `;
            this.chatMessages.appendChild(userMessageElement);

            // Scroll to bottom
            this.chatMessages.scrollTop = this.chatMessages.scrollHeight;

            // Hide welcome message if visible
            const welcomeMessage = document.querySelector('.welcome-message');
            if (welcomeMessage) {
                welcomeMessage.style.display = 'none';
            }

            let response;

            if (!this.currentConversationId) {
                // Create new conversation
                response = await chatApi.sendMessage(message);

                // Update conversation ID and title
                this.currentConversationId = response.conversation_id;
                this.conversationTitle.textContent = response.conversation_title || 'New Conversation';

                // Reload conversations to update sidebar
                await this.loadConversations();
            } else {
                // Send message to existing conversation
                response = await chatApi.sendMessage(message, this.currentConversationId);
            }

            // Add AI response to UI
            const aiMessageElement = document.createElement('div');
            aiMessageElement.className = 'message assistant';
            aiMessageElement.innerHTML = `
                <div class="message-content">${this.formatMessageContent(response.content)}</div>
            `;
            this.chatMessages.appendChild(aiMessageElement);

            // Scroll to bottom
            this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        } catch (error) {
            console.error('Error sending message:', error);

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

    // Handle creating a new chat
    async handleNewChat() {
        try {
            // Create new conversation
            const conversation = await chatApi.createConversation();

            // Update current conversation
            this.currentConversationId = conversation.id;
            this.conversationTitle.textContent = conversation.title;

            // Clear messages
            this.chatMessages.innerHTML = '';

            // Reload conversations
            await this.loadConversations();
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
