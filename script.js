// async function sendMessage(message) {
//     const response = await fetch('http://localhost:8000/chatbot', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({ question: message })
//     });
//     const data = await response.json();
//     return data.response;
// }

// document.getElementById('chat-form').addEventListener('submit', async function (e) {
//     e.preventDefault();
//     const userInput = document.getElementById('user-input').value;
//     const chatBox = document.getElementById('chat-box');

//     chatBox.innerHTML += `<div class="chat-message user-message">${userInput}</div>`;

//     const botResponse = await sendMessage(userInput);

//     chatBox.innerHTML += `<div class="chat-message bot-message">${botResponse}</div>`;
//     document.getElementById('user-input').value = '';
// });

document.getElementById('chatbot-button').addEventListener('click', () => {
    const chatbotPopup = document.getElementById('chatbot-popup');
    const chatbotButton = document.getElementById('chatbot-button');

    if (chatbotPopup.style.display === 'none' || chatbotPopup.style.display === '') {
        chatbotPopup.style.display = 'flex';
        chatbotButton.textContent = 'Chiudi';
    } else {
        chatbotPopup.style.display = 'none';
        chatbotButton.textContent = 'Chat';
    }
});

document.getElementById('chatbot-send').addEventListener('click', async () => {
    const userMessage = document.getElementById('chatbot-input').value;
    if (userMessage.trim() !== "") {
        addMessage(userMessage, 'user-message');
        document.getElementById('chatbot-input').value = '';

        // Chiamata al backend per ottenere la risposta
        const response = await fetch('/chatbot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question: userMessage })
        });
        
        const data = await response.json();
        addMessage(data.response, 'bot-message');
    }
});

function addMessage(text, className) {
    const messageContainer = document.getElementById('chatbot-messages');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', className);
    messageElement.textContent = text;
    messageContainer.appendChild(messageElement);
    messageContainer.scrollTop = messageContainer.scrollHeight;
}

// Optional: Mostra il chatbot automaticamente al caricamento della pagina
window.onload = () => {
    const chatbotPopup = document.getElementById('chatbot-popup');
    const chatbotButton = document.getElementById('chatbot-button');
    chatbotPopup.style.display = 'none';  // Inizia nascosto
    chatbotButton.textContent = 'Chat';
};

