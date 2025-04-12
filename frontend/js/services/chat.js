// Chat Service
const API_URL = 'http://localhost:8000/api';

// Get all conversations
async function getConversations() {
    try {
        const token = localStorage.getItem('token');
        if (!token) {
            throw new Error('Not authenticated');
        }

        const response = await fetch(`${API_URL}/conversations`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            }
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.detail || 'Failed to fetch conversations');
        }

        return await response.json();
    } catch (error) {
        console.error('Error fetching conversations:', error);
        throw error;
    }
}

// Get a specific conversation with messages
async function getConversation(conversationId) {
    try {
        const token = localStorage.getItem('token');
        if (!token) {
            throw new Error('Not authenticated');
        }

        const response = await fetch(`${API_URL}/conversations/${conversationId}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            }
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.detail || 'Failed to fetch conversation');
        }

        return await response.json();
    } catch (error) {
        console.error('Error fetching conversation:', error);
        throw error;
    }
}

// Create a new conversation
async function createConversation(title = 'New Conversation') {
    try {
        const token = localStorage.getItem('token');
        if (!token) {
            throw new Error('Not authenticated');
        }

        const response = await fetch(`${API_URL}/conversations`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ title })
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.detail || 'Failed to create conversation');
        }

        return await response.json();
    } catch (error) {
        console.error('Error creating conversation:', error);
        throw error;
    }
}

// Send a message and get AI response
async function sendMessage(message, conversationId = null) {
    try {
        const token = localStorage.getItem('token');
        if (!token) {
            throw new Error('Not authenticated');
        }

        const payload = {
            role: 'user',
            content: message
        };

        if (conversationId) {
            payload.conversation_id = conversationId;
        }

        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.detail || 'Failed to send message');
        }

        return await response.json();
    } catch (error) {
        console.error('Error sending message:', error);
        throw error;
    }
}

// Delete a conversation
async function deleteConversation(conversationId) {
    try {
        const token = localStorage.getItem('token');
        if (!token) {
            throw new Error('Not authenticated');
        }

        const response = await fetch(`${API_URL}/conversations/${conversationId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            }
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.detail || 'Failed to delete conversation');
        }

        return await response.json();
    } catch (error) {
        console.error('Error deleting conversation:', error);
        throw error;
    }
}

// Update conversation title
async function updateConversationTitle(conversationId, title) {
    try {
        const token = localStorage.getItem('token');
        if (!token) {
            throw new Error('Not authenticated');
        }

        const response = await fetch(`${API_URL}/conversations/${conversationId}?title=${encodeURIComponent(title)}`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            }
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.detail || 'Failed to update conversation title');
        }

        return await response.json();
    } catch (error) {
        console.error('Error updating conversation title:', error);
        throw error;
    }
}
