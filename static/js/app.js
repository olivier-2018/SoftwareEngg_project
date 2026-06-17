// Audio recording for browser microphone capture using MediaRecorder API

let mediaRecorder;
let audioChunks = [];
let recordedAudioBlob = null;

const recordButton = document.getElementById("recordButton");
const stopButton = document.getElementById("stopButton");
const pauseButton = document.getElementById("pauseButton");

recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);
pauseButton.addEventListener("click", pauseRecording);

function startRecording() {
  console.log("recordButton clicked");

  recordButton.disabled = true;
  stopButton.disabled = false;
  pauseButton.disabled = false;
  audioChunks = [];

  // Clear previous prediction
  const predictionDiv = document.querySelector(".card.text-white.bg-primary");
  if (predictionDiv) {
    predictionDiv.parentElement.remove();
  }

  navigator.mediaDevices
    .getUserMedia({ audio: true, video: false })
    .then(function (stream) {
      console.log("getUserMedia() success, stream created, initializing MediaRecorder...");

      // MediaRecorder with default encoding (WebM/Opus)
      mediaRecorder = new MediaRecorder(stream);

      // Collect audio data chunks
      mediaRecorder.addEventListener("dataavailable", function (event) {
        audioChunks.push(event.data);
      });

      // Handle recording stop
      mediaRecorder.addEventListener("stop", function () {
        console.log("Recording stopped, processing audio blob");
        recordedAudioBlob = new Blob(audioChunks, { type: "audio/webm" });
        uploadAudio(recordedAudioBlob);

        // Stop microphone access
        stream.getAudioTracks()[0].stop();
      });

      // Display sample rate
      const audioContext = new (window.AudioContext || window.webkitAudioContext)();
      document.getElementById("formats").innerHTML = "Format: 1 channel WebM @ " + audioContext.sampleRate / 1000 + "kHz";

      // Start recording
      mediaRecorder.start();
      console.log("Recording started");
    })
    .catch(function (err) {
      console.error("getUserMedia() error:", err);
      recordButton.disabled = false;
      stopButton.disabled = true;
      pauseButton.disabled = true;
      alert("Microphone access denied. Please enable microphone permissions.");
    });
}

function pauseRecording() {
  console.log("pauseButton clicked, mediaRecorder.state=" + mediaRecorder.state);
  if (mediaRecorder.state === "recording") {
    mediaRecorder.pause();
    pauseButton.innerHTML = "Resume";
  } else if (mediaRecorder.state === "paused") {
    mediaRecorder.resume();
    pauseButton.innerHTML = "Pause";
  }
}

function stopRecording() {
  console.log("stopButton clicked");

  stopButton.disabled = true;
  recordButton.disabled = false;
  pauseButton.disabled = true;
  pauseButton.innerHTML = "Pause";

  mediaRecorder.stop();
}

function uploadAudio(audioBlob) {
  console.log("Uploading audio blob to server...");

  const formData = new FormData();
  formData.append("file", audioBlob, "recording.webm");

  fetch(window.location.pathname, {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Upload failed: " + response.statusText);
      }
      console.log("Audio uploaded successfully, parsing JSON response...");
      return response.json();
    })
    .then((data) => {
      console.log("Prediction received:", data.prediction);

      // Update prediction card
      const predictionDiv = document.querySelector(".card.text-white.bg-primary");
      if (!predictionDiv) {
        // Card doesn't exist, create it
        const predictionSection = document.querySelector(".column");
        const newCard = document.createElement("div");

        // Create blob URL for audio playback
        const audioURL = URL.createObjectURL(recordedAudioBlob);

        newCard.innerHTML = `
          <br />
          <h3>Play Recording</h3>
          <audio controls autoplay style="width: 100%; max-width: 300px;">
            <source src="${audioURL}" type="audio/webm">
            Your browser does not support the audio element.
          </audio>
          <br />
          <br />
          <h3>Prediction Result</h3>
          <div class="card text-white bg-primary mb-3" style="max-width: 10rem;">
            <div class="card-header">Predicted Digit</div>
            <div class="card-body">
              <h4 class="card-title">${data.prediction}</h4>
            </div>
          </div>
          <br />
          <div>
            <p>
              <strong>Disclaimer:</strong> The ML model was trained to 94% test accuracy but does not
              generalize on all real-life test cases due to the reduced dataset size.
            </p>
          </div>
        `;
        predictionSection.appendChild(newCard);
      } else {
        // Update existing card
        const titleElement = predictionDiv.querySelector(".card-title");
        if (titleElement) {
          titleElement.textContent = data.prediction;
        }

        // Update audio player
        const audioURL = URL.createObjectURL(recordedAudioBlob);
        const audioElement = predictionDiv.parentElement.querySelector("audio");
        if (audioElement) {
          audioElement.src = audioURL;
        }
      }

      // Update waveform image with cache-busting timestamp
      if (data.filename) {
        const timestamp = new Date().getTime();
        const waveformDiv = document.querySelector(".column:last-child");
        const imgElement = waveformDiv.querySelector("img");
        if (imgElement) {
          imgElement.src = `/display/${data.filename}?t=${timestamp}`;
        } else {
          const newImg = document.createElement("div");
          newImg.innerHTML = `<img src="/display/${data.filename}?t=${timestamp}" />`;
          waveformDiv.appendChild(newImg);
        }
      }

      recordButton.disabled = false;
    })
    .catch((error) => {
      console.error("Error uploading audio:", error);
      alert("Error uploading audio: " + error.message);
      recordButton.disabled = false;
    });
}
