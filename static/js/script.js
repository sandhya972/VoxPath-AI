const recordBtn = document.getElementById("recordBtn");
const resetBtn = document.getElementById("resetBtn");
const typedForm = document.getElementById("typedForm");
const typedInput = document.getElementById("typedInput");
const sendBtn = document.getElementById("sendBtn");
const statusText = document.getElementById("status");

const transcriptText = document.getElementById("transcript");
const responseText = document.getElementById("response");
const audioPlayer = document.getElementById("audioPlayer");

let mediaRecorder;
let audioChunks = [];
let isRecording = false;
function setProcessing(isBusy) {
    typedInput.disabled = isBusy;
    sendBtn.disabled = isBusy;
    resetBtn.disabled = isBusy;
}

recordBtn.addEventListener("click", async () => {

    if (!isRecording) {

        try {

            const stream = await navigator.mediaDevices.getUserMedia({
                audio: true
            });

            mediaRecorder = new MediaRecorder(stream);

            audioChunks = [];

            mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    audioChunks.push(event.data);
                }
            };

            mediaRecorder.onstop = processAudio;

            mediaRecorder.start();

isRecording = true;

setProcessing(true);

            recordBtn.textContent = "⏹ Stop Recording";
            statusText.textContent = "Listening... Speak now!";

        } catch (error) {

            statusText.textContent = "Microphone access denied or unavailable.";
            console.error(error);

        }

    } else {

        mediaRecorder.stop();

isRecording = false;
recordBtn.disabled = true;

        recordBtn.textContent = "🎤 Start Recording";
        statusText.textContent = "Processing your voice...";

    }

});


async function processAudio() {

    const audioBlob = new Blob(audioChunks, {
        type: mediaRecorder.mimeType
    });

    const formData = new FormData();

    let extension = "webm";

    if (mediaRecorder.mimeType.includes("ogg")) {
        extension = "ogg";
    }

    formData.append(
        "audio",
        audioBlob,
        `recording.${extension}`
    );

    try {

        const result = await fetch("/api/voice", {
            method: "POST",
            body: formData
        });

        const data = await result.json();

        if (!result.ok) {
            throw new Error(data.error || "Voice processing failed.");
        }

        transcriptText.textContent = data.transcript;
        responseText.textContent = data.response;

        audioPlayer.src = data.audio_url;
        audioPlayer.hidden = false;

        statusText.textContent = "VoxPath has responded successfully!";

       audioPlayer.play().catch(error => {
    console.log("Audio autoplay was blocked:", error);
});

    } catch (error) {

    statusText.textContent = error.message || 
        "Unable to process your voice. Please try again.";

    console.error("Voice processing error:", error);

    } finally {

        mediaRecorder.stream.getTracks().forEach(track => track.stop());

setProcessing(false);
recordBtn.disabled = false;

    }

}
// Reset Conversation
resetBtn.addEventListener("click", async () => {

    try {

        statusText.textContent = "Resetting conversation...";

        const result = await fetch("/api/reset", {
            method: "POST"
        });

        const data = await result.json();

        if (!result.ok) {
            throw new Error(data.message || "Reset failed.");
        }

        transcriptText.textContent = "Your speech will appear here...";
        responseText.textContent = "Your AI response will appear here...";

        audioPlayer.pause();
        audioPlayer.removeAttribute("src");
        audioPlayer.hidden = true;

        statusText.textContent = "Conversation reset! Start a new conversation.";

    } catch (error) {

        statusText.textContent = "Unable to reset conversation.";
        console.error(error);

    }

});
// Typed Message Feature
typedForm.addEventListener("submit", async (event) => {

    event.preventDefault();

    const message = typedInput.value.trim();

    if (!message) {
        statusText.textContent = "Please enter a message.";
        return;
    }

    // Prevent duplicate submissions
    sendBtn.disabled = true;
    typedInput.disabled = true;
    sendBtn.textContent = "Sending...";
    statusText.textContent = "VoxPath is thinking...";

    try {

        const result = await fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message
            })
        });

        const data = await result.json();

        if (!result.ok) {
            throw new Error(data.error || "Message failed.");
        }

        transcriptText.textContent = data.transcript;
        responseText.textContent = data.response;

        audioPlayer.src = data.audio_url;
        audioPlayer.hidden = false;

        statusText.textContent = "VoxPath has responded successfully!";

        typedInput.value = "";

        audioPlayer.play().catch(error => {
            console.log("Audio autoplay was blocked:", error);
        });

    } catch (error) {

        statusText.textContent = error.message;
        console.error(error);

    } finally {

        // Restore the controls
        sendBtn.disabled = false;
        typedInput.disabled = false;
        sendBtn.textContent = "Send Message";

    }

});