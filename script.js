document.addEventListener("DOMContentLoaded", function() {
    const voiceButton = document.getElementById('voice-input-btn');
    const assistantMessage = document.getElementById('assistant-message');

    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    const synth = window.speechSynthesis;

    // Speech Recognition Setup
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onstart = () => {
        assistantMessage.innerText = "Listening...";
    };

    recognition.onresult = (event) => {
        const userSpeech = event.results[0][0].transcript;
        assistantMessage.innerText = `You said: ${userSpeech}`;
        respondToUser(userSpeech); // Make the assistant respond
    };

    recognition.onerror = (event) => {
        assistantMessage.innerText = "Error: " + event.error;
    };

    // Start Listening when button is clicked
    voiceButton.addEventListener('click', () => {
        assistantMessage.innerText = "Listening...";
        recognition.start(); // Start speech recognition
    });

    function respondToUser(userSpeech) {
        let response = "I'm sorry, I didn't quite get that.";

        if (userSpeech.toLowerCase().includes("hello")) {
            response = "Hello! How can I assist you today?";
        } else if (userSpeech.toLowerCase().includes("what is your name")) {
            response = "I am your AI assistant!";
        } else if (userSpeech.toLowerCase().includes("how are you")) {
            response = "I'm doing great, thank you for asking!";
        }

        assistantMessage.innerText = response;
        speak(response);  // Make assistant speak the response
    }

    // Speech Synthesis to Speak the Response
    function speak(message) {
        const utterance = new SpeechSynthesisUtterance(message);
        utterance.lang = "en-US";
        synth.speak(utterance);
    }
});
