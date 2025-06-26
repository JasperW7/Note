import pyaudio
import wave
import threading
import keyboard  # For listening to key events

# Audio parameters
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 60  # optional limit

# Global flags and storage
frames = []
is_recording = threading.Event()

def record_audio():
    global frames
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    
    print("Recording started.")
    frames = []

    while is_recording.is_set():
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)

    print("Recording stopped.")
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save to file
    wf = wave.open("output.wav", "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    print("Audio saved to output.wav")

def on_key_event(e):
    if e.name == 'r' and not is_recording.is_set():
        is_recording.set()
        threading.Thread(target=record_audio).start()
    elif e.name == 's' and is_recording.is_set():
        is_recording.clear()

# Register hotkeys
print("Press 'r' to start recording, 's' to stop.")
keyboard.on_press(on_key_event)

# Keep the main thread alive
keyboard.wait('esc')  # Press ESC to exit
