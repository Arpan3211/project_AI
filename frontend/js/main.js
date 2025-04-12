// Main JavaScript file
document.addEventListener('DOMContentLoaded', function() {
    // Initialize the chat functionality
    initChat();

    // Initialize auth functionality
    // Note: Auth initialization is handled in auth.js

    // Handle sidebar navigation
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', function() {
            navItems.forEach(i => i.classList.remove('active'));
            this.classList.add('active');
        });
    });

    // Handle new chat button
    const newChatBtn = document.querySelector('.new-chat-btn');
    newChatBtn.addEventListener('click', function() {
        clearChat();
    });

    // Handle sidebar toggle
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebar = document.getElementById('sidebar');

    sidebarToggle.addEventListener('click', function() {
        sidebar.classList.toggle('collapsed');
        // Save the state to localStorage
        localStorage.setItem('sidebarCollapsed', sidebar.classList.contains('collapsed'));
    });

    // Check if sidebar was collapsed previously
    if (localStorage.getItem('sidebarCollapsed') === 'true') {
        sidebar.classList.add('collapsed');
    }

    // Handle mobile chat button
    const chatButton = document.querySelector('.chat-button');

    chatButton.addEventListener('click', function() {
        sidebar.style.display = sidebar.style.display === 'none' || sidebar.style.display === '' ? 'flex' : 'none';
    });

    // Handle window resize for responsive design
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768) {
            sidebar.style.display = 'flex';
        } else {
            sidebar.style.display = 'none';
        }
    });

    // Initialize with correct sidebar display based on screen size
    if (window.innerWidth <= 768) {
        sidebar.style.display = 'none';
    }
});

// Function to clear chat
function clearChat() {
    const chatMessages = document.getElementById('chat-messages');
    const welcomeMessage = document.querySelector('.welcome-message');

    chatMessages.innerHTML = '';
    document.getElementById('chat-input').value = '';

    // Show welcome message again
    if (welcomeMessage) {
        welcomeMessage.classList.remove('hidden');
    }

    // Reset chat state
    if (window.resetChatState) {
        window.resetChatState();
    }
}
