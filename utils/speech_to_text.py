import whisper
import pyaudio
import webrtcvad
import numpy as np
import torch

# Load Whisper model and send it to GPU
#model = whisper.load_model("base").to("cuda")

import torch

device = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model("base").to(device)


# Audio config
RATE = 16000
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
VAD_MODE = 3

vad = webrtcvad.Vad(VAD_MODE)

def is_speech(frame, rate):
    return vad.is_speech(frame, rate)

def is_loud_enough(frame, threshold=500):
    audio = np.frombuffer(frame, dtype=np.int16)
    return np.abs(audio).mean() > threshold

def record_audio():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    frames = []
    silence_count = 0
    max_silence_frames = 50  # Adjust as needed

    frame_duration_ms = 20
    frame_bytes = int(RATE * (frame_duration_ms / 1000.0) * 2)  # 2 bytes per sample (16-bit audio)

    buffer = b''

    while True:
        data = stream.read(CHUNK)
        buffer += data

        while len(buffer) >= frame_bytes:
            frame = buffer[:frame_bytes]
            buffer = buffer[frame_bytes:]

            frames.append(frame)

            if is_loud_enough(frame) and is_speech(frame, RATE):
                silence_count = 0
            else:
                silence_count += 1

            if silence_count > max_silence_frames:
                print("Speech ended.")
                stream.stop_stream()
                stream.close()
                p.terminate()

                audio_data = b''.join(frames)
                audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
                return audio_np

def transcribe_audio(audio_np):
    audio_tensor = torch.from_numpy(audio_np).to("cuda")
    audio_tensor = whisper.pad_or_trim(audio_tensor)
    mel = whisper.log_mel_spectrogram(audio_tensor).to("cuda")
    options = whisper.DecodingOptions(fp16=True)
    result = whisper.decode(model, mel, options)
    return result.text

def stt():
    audio = record_audio()
    if(audio.shape[0] < 5000): return ""
    return transcribe_audio(audio)

if __name__ == "__main__":
    # while True:
    audio = record_audio()
    print(audio.shape)
    text = transcribe_audio(audio)
    print("You said:", text)

