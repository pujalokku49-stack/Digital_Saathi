/**
 * Digital Saathi – AI Chatbot Frontend
 * Handles message sending, display, and API communication
 */

document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chatMessages');
    const chatInput = document.getElementById('chatInput');
    const sendBtn = document.getElementById('sendBtn');
    const typingIndicator = document.getElementById('typingIndicator');

    if (!chatMessages || !chatInput) return;

    let lastBotResponse = '';

    /**
     * Append a message bubble to the chat
     */
    function appendMessage(text, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${isUser ? 'user-message' : 'bot-message'}`;

        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = isUser
            ? '<i class="bi bi-person-fill"></i>'
            : '<i class="bi bi-robot"></i>';

        const bubble = document.createElement('div');
        bubble.className = 'message-bubble';
        bubble.textContent = text;

        messageDiv.appendChild(avatar);
        messageDiv.appendChild(bubble);
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;

        if (!isUser) lastBotResponse = text;
    }

    /**
     * Send message to backend API
     */
    async function sendMessage(message) {
        if (!message.trim()) return;

        appendMessage(message, true);
        chatInput.value = '';
        typingIndicator.classList.remove('d-none');

        try {
            const response = await fetch('/chatbot/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: message,
                    language: I18n.currentLang || 'en'
                })
            });

            const data = await response.json();
            typingIndicator.classList.add('d-none');

            if (response.ok) {
                appendMessage(data.response);
                // Auto read aloud for accessibility (optional)
                if (window.VoiceAssistant && localStorage.getItem('saathi_auto_speak') === 'true') {
                    VoiceAssistant.speak(data.response);
                }
            } else {
                appendMessage(data.error || 'Something went wrong. Please try again.');
            }
        } catch (error) {
            typingIndicator.classList.add('d-none');
            appendMessage('Unable to connect to server. Please check your internet connection.');
            console.error('Chat error:', error);
        }
    }

    // Send button click
    sendBtn.addEventListener('click', () => sendMessage(chatInput.value));

    // Enter key to send
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage(chatInput.value);
    });

    // Read aloud button
    const speakBtn = document.getElementById('speakBtn');
    if (speakBtn) {
        speakBtn.addEventListener('click', () => {
            if (lastBotResponse && window.VoiceAssistant) {
                VoiceAssistant.speak(lastBotResponse);
            }
        });
    }

    // Expose sendMessage for voice integration
    window.Chatbot = { sendMessage, appendMessage };
});
