function setStatus(message) {
    const status = document.getElementById("status");
    if (status) status.innerText = message;
}

function speakText(text) {
    if (!('speechSynthesis' in window) || !text) {
        return;
    }

    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1;
    utterance.pitch = 1;
    utterance.lang = 'en-US';
    window.speechSynthesis.speak(utterance);
}

function sendMessage() {
    const userInput = document.getElementById("userInput");
    const response = document.getElementById("response");
    const input = userInput.value.trim();

    if (!input) {
        response.innerText = "Please type your question first.";
        return;
    }

    setStatus("Thinking...");

    fetch('/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input })
    })
    .then(res => res.json())
    .then(data => {
        const responseText = data.response || "I couldn't understand that.";
        response.innerText = responseText;
        setStatus("");
        speakText(responseText);
    })
    .catch(() => {
        response.innerText = "Something went wrong. Please try again.";
        setStatus("");
        speakText("Something went wrong. Please try again.");
    });
}

function openCall() {
    const response = document.getElementById("response");
    const firstMessage = "Use this when you want to speak with someone directly. Open the dialer and call +91 1800 123 4567. If the call does not open, copy the number and dial it manually.";
    const fallbackMessage = "Use your phone to dial +91 1800 123 4567. This connects you to customer support.";

    response.innerText = firstMessage;
    speakText(firstMessage);

    try {
        window.location.href = "tel:+9118001234567";
    } catch (error) {
        response.innerText = fallbackMessage;
        speakText(fallbackMessage);
    }

    setTimeout(() => {
        if (response.innerText === firstMessage) {
            response.innerText = fallbackMessage;
            speakText(fallbackMessage);
        }
    }, 1200);
}

function openWhatsApp() {
    const response = document.getElementById("response");
    const message = "Use this if you prefer chatting. Open WhatsApp and send 'Hi' to +91 99999 99999 so the team can reply.";
    response.innerText = message;
    speakText(message);
    window.open("https://wa.me/919999999999", "_blank");
}

function openUPI() {
    const response = document.getElementById("response");
    const message = "Use this when you want to pay. Open a UPI app such as PhonePe, Google Pay, or Paytm, enter the amount, and confirm the payment.";
    response.innerText = message;
    speakText(message);
    window.open("https://pay.google.com/", "_blank");
}

function connectAgent() {
    const response = document.getElementById("response");
    const message = "Use this when you want guided help. Type your question in the chat box and press Ask so the agent can explain each step.";
    response.innerText = message;
    speakText(message);
}

function copyResponse() {
    const response = document.getElementById("response");
    if (!response || !response.innerText) return;
    navigator.clipboard.writeText(response.innerText);
}

function listenResponse() {
    const response = document.getElementById("response");
    if (response && response.innerText) {
        speakText(response.innerText);
    }
}

function useSuggestion(event) {
    const chip = event.target.closest('.suggestion-chip');
    if (!chip) return;
    const suggestion = chip.dataset.suggestion;
    const input = document.getElementById('userInput');
    if (input) {
        input.value = suggestion;
        sendMessage();
    }
}

function updateTime() {
    const timeElement = document.getElementById('currentTime');
    if (!timeElement) return;
    const now = new Date();
    const hours = now.getHours();
    const minutes = now.getMinutes();
    const suffix = hours >= 12 ? 'PM' : 'AM';
    const displayHours = hours % 12 || 12;
    const displayMinutes = minutes < 10 ? '0' + minutes : minutes;
    timeElement.innerText = `${displayHours}:${displayMinutes} ${suffix}`;
}

function toggleTheme() {
    document.body.classList.toggle('dark-theme');
}

function addToHistory(text) {
    const historyList = document.getElementById('historyList');
    if (!historyList || !text) return;
    const item = document.createElement('li');
    item.innerText = text;
    historyList.prepend(item);
    while (historyList.children.length > 5) {
        historyList.removeChild(historyList.lastChild);
    }
}

const userInput = document.getElementById("userInput");
if (userInput) {
    userInput.addEventListener("keydown", function(event) {
        if (event.key === "Enter") {
            event.preventDefault();
            sendMessage();
        }
    });
}

const searchButton = document.getElementById("searchButton");
if (searchButton) {
    searchButton.addEventListener("click", () => {
        sendMessage();
        const input = document.getElementById('userInput');
        if (input && input.value.trim()) {
            addToHistory(input.value.trim());
        }
    });
}

const callButton = document.getElementById("callButton");
if (callButton) {
    callButton.addEventListener("click", openCall);
}

const whatsappButton = document.getElementById("whatsappButton");
if (whatsappButton) {
    whatsappButton.addEventListener("click", openWhatsApp);
}

const upiButton = document.getElementById("upiButton");
if (upiButton) {
    upiButton.addEventListener("click", openUPI);
}

const agentButton = document.getElementById("agentButton");
if (agentButton) {
    agentButton.addEventListener("click", connectAgent);
}

const copyButton = document.getElementById("copyButton");
if (copyButton) {
    copyButton.addEventListener("click", copyResponse);
}

const listenButton = document.getElementById("listenButton");
if (listenButton) {
    listenButton.addEventListener("click", listenResponse);
}

const suggestionPanel = document.querySelector('.suggestions-panel');
if (suggestionPanel) {
    suggestionPanel.addEventListener('click', useSuggestion);
}

const themeToggle = document.getElementById('themeToggle');
if (themeToggle) {
    themeToggle.addEventListener('click', toggleTheme);
}

updateTime();
setInterval(updateTime, 60000);
