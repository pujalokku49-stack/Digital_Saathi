/**
 * Digital Saathi – Voice Assistant
 * Speech-to-text (STT) and text-to-speech (TTS) using Web Speech API
 */

const VoiceAssistant = {
    recognition: null,
    isListening: false,
    synth: window.speechSynthesis,

    /**
     * Initialize voice recognition if supported
     */
    init() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

        if (!SpeechRecognition) {
            this.showStatus('Voice input not supported in this browser. Try Chrome.');
            return;
        }

        this.recognition = new SpeechRecognition();
        this.recognition.continuous = false;
        this.recognition.interimResults = true;
        this.recognition.maxAlternatives = 1;

        // Set language based on current i18n setting
        this.setLanguage(I18n?.currentLang || 'en');

        this.recognition.onstart = () => {
            this.isListening = true;
            this.updateVoiceButton(true);
            this.showStatus(I18n?.t('chatbot_voice_start') || 'Listening...');
        };

        this.recognition.onend = () => {
            this.isListening = false;
            this.updateVoiceButton(false);
            this.showStatus('');
        };

        this.recognition.onerror = (event) => {
            this.isListening = false;
            this.updateVoiceButton(false);
            const errors = {
                'no-speech': 'No speech detected. Please try again.',
                'not-allowed': 'Microphone access denied. Please allow microphone.',
                'network': 'Network error. Check your connection.'
            };
            this.showStatus(errors[event.error] || `Error: ${event.error}`);
        };

        this.recognition.onresult = (event) => {
            let transcript = '';
            for (let i = event.resultIndex; i < event.results.length; i++) {
                transcript += event.results[i][0].transcript;
            }

            const chatInput = document.getElementById('chatInput');
            if (chatInput) chatInput.value = transcript;

            // Send when final result received
            if (event.results[event.results.length - 1].isFinal) {
                if (window.Chatbot && transcript.trim()) {
                    window.Chatbot.sendMessage(transcript.trim());
                }
            }
        };

        // Voice button handler
        const voiceBtn = document.getElementById('voiceBtn');
        if (voiceBtn) {
            voiceBtn.addEventListener('click', () => this.toggleListening());
        }
    },

    /**
     * Map app language codes to speech recognition locales
     */
    setLanguage(lang) {
        if (!this.recognition) return;
        const langMap = {
            en: 'en-IN',
            hi: 'hi-IN',
            te: 'te-IN'
        };
        this.recognition.lang = langMap[lang] || 'en-IN';
    },

    /**
     * Start or stop voice recognition
     */
    toggleListening() {
        if (!this.recognition) {
            this.showStatus('Voice not supported. Use Chrome browser.');
            return;
        }

        if (this.isListening) {
            this.recognition.stop();
        } else {
            this.setLanguage(I18n?.currentLang || 'en');
            this.recognition.start();
        }
    },

    /**
     * Text-to-speech: read text aloud
     */
    speak(text) {
        if (!this.synth) return;

        // Cancel any ongoing speech
        this.synth.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        const langMap = {
            en: 'en-IN',
            hi: 'hi-IN',
            te: 'te-IN'
        };
        utterance.lang = langMap[I18n?.currentLang] || 'en-IN';
        utterance.rate = 0.9;  // Slightly slower for elders
        utterance.pitch = 1;
        utterance.volume = 1;

        this.synth.speak(utterance);
    },

    /**
     * Update microphone button visual state
     */
    updateVoiceButton(listening) {
        const voiceBtn = document.getElementById('voiceBtn');
        if (!voiceBtn) return;

        voiceBtn.classList.toggle('listening', listening);
        voiceBtn.innerHTML = listening
            ? '<i class="bi bi-mic-mute-fill"></i>'
            : '<i class="bi bi-mic-fill"></i>';
        voiceBtn.setAttribute('aria-label', listening ? 'Stop listening' : 'Start voice input');
    },

    /**
     * Show status message below chat input
     */
    showStatus(message) {
        const statusEl = document.getElementById('voiceStatus');
        if (statusEl) statusEl.textContent = message;
    }
};

window.VoiceAssistant = VoiceAssistant;

document.addEventListener('DOMContentLoaded', () => {
    // Wait for I18n to init first
    setTimeout(() => VoiceAssistant.init(), 100);
});
