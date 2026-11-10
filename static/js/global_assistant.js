const assistantToggle = document.getElementById("assistantToggle");
const assistantPanel = document.getElementById("assistantPanel");
const assistantClose = document.getElementById("assistantClose");

const assistantRecord = document.getElementById("assistantRecord");
const assistantForm = document.getElementById("assistantForm");
const assistantInput = document.getElementById("assistantInput");
const assistantSend = document.getElementById("assistantSend");
const assistantReset = document.getElementById("assistantReset");

const assistantStatus = document.getElementById("assistantStatus");
const assistantTranscript = document.getElementById("assistantTranscript");
const assistantReply = document.getElementById("assistantReply");
const assistantAudio = document.getElementById("assistantAudio");

let mediaRecorder = null;
let audioChunks = [];
let isRecording = false;
let isBusy = false;

assistantToggle.addEventListener("click", () => {
    assistantPanel.hidden = !assistantPanel.hidden;
});

assistantClose.addEventListener("click", () => {
    assistantPanel.hidden = true;
});

function setBusy(busy) {
    isBusy = busy;
    assistantInput.disabled = busy;
    assistantSend.disabled = busy;
    assistantReset.disabled = busy;
    assistantRecord.disabled = busy || isRecording;
}

function displayResponse(data) {
    assistantTranscript.textContent = data.transcript;
    assistantReply.textContent = data.response;

    if (data.audio_url) {
        assistantAudio.src = data.audio_url;
        assistantAudio.hidden = false;
        assistantAudio.play().catch(() => {});
    }
}

async function sendMessage(message) {
    setBusy(true);
    assistantStatus.textContent = "VoxPath is thinking...";

    try {
        const result = await fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message })
        });

        const data = await result.json();

        if (!result.ok) {
            throw new Error(data.error || "Message failed.");
        }

        displayResponse(data);
        assistantStatus.textContent = "Response received successfully!";

    } catch (error) {
        assistantStatus.textContent = error.message;
    } finally {
        setBusy(false);
    }
}

assistantForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const message = assistantInput.value.trim();

    if (!message || isBusy) return;

    assistantInput.value = "";
    await sendMessage(message);
});

assistantRecord.addEventListener("click", async () => {

    if (isBusy) return;

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

            mediaRecorder.onstop = processAssistantAudio;

            mediaRecorder.start();
            isRecording = true;

            assistantRecord.textContent = "⏹ Stop Recording";
            assistantStatus.textContent = "Listening... Speak now!";

        } catch (error) {
            assistantStatus.textContent =
                "Microphone access denied or unavailable.";
        }

    } else {
        mediaRecorder.stop();
        isRecording = false;
        assistantRecord.disabled = true;
        assistantRecord.textContent = "🎤 Start Recording";
        assistantStatus.textContent = "Processing your voice...";
    }
});

async function processAssistantAudio() {

    const formData = new FormData();

    const extension = mediaRecorder.mimeType.includes("ogg")
        ? "ogg"
        : "webm";

    const audioBlob = new Blob(audioChunks, {
        type: mediaRecorder.mimeType
    });

    formData.append("audio", audioBlob, `recording.${extension}`);

    setBusy(true);

    try {
        const result = await fetch("/api/voice", {
            method: "POST",
            body: formData
        });

        const data = await result.json();

        if (!result.ok) {
            throw new Error(data.error || "Voice processing failed.");
        }

        displayResponse(data);
        assistantStatus.textContent = "Voice response received!";

    } catch (error) {
        assistantStatus.textContent = error.message;

    } finally {
        mediaRecorder.stream.getTracks().forEach(track => track.stop());
        setBusy(false);
        assistantRecord.disabled = false;
    }
}

assistantReset.addEventListener("click", async () => {

    if (isBusy) return;

    setBusy(true);
    assistantStatus.textContent = "Resetting conversation...";

    try {
        const result = await fetch("/api/reset", {
            method: "POST"
        });

        const data = await result.json();

        if (!result.ok) {
            throw new Error(data.message || "Reset failed.");
        }

        assistantTranscript.textContent = "Your message will appear here.";
        assistantReply.textContent = "Your response will appear here.";

        assistantAudio.pause();
        assistantAudio.removeAttribute("src");
        assistantAudio.hidden = true;

        assistantStatus.textContent = "Conversation reset successfully!";

    } catch (error) {
        assistantStatus.textContent = error.message;

    } finally {
        setBusy(false);
    }
});