document.addEventListener('DOMContentLoaded', () => {
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const messagesContainer = document.getElementById('messages-container');

    sendButton.addEventListener('click', () => {
        const messageText = messageInput.value;
        if (messageText.trim()) {
            sendMessage(messageText);
            addMessageToUI(messageText, 'sent');
            messageInput.value = '';
        }
    });

    function sendMessage(message) {
        fetch('/send_message/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message, recipient_id: '7812277818885789' }) // Replace with dynamic recipient_id
        })
        .then(response => response.json())
        .then(data => {
            console.log('Message sent:', data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    function addMessageToUI(message, type) {
        const messageElement = document.createElement('div');
        messageElement.className = `message ${type}`;
        messageElement.textContent = message;
        messagesContainer.appendChild(messageElement);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
});
