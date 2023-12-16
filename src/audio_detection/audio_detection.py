import aubio
import numpy as np
import pyaudio

# Parameters for audio stream
sample_rate = 44100
buffer_size = 1024

# Initialize Aubio pitch detection
hop_size = buffer_size
pitch_detection = aubio.pitch("default", buffer_size, hop_size, sample_rate)

# Create PyAudio stream
audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=sample_rate,
                    frames_per_buffer=buffer_size,
                    input=True)

# Main loop for real-time analysis
while True:
    # Read audio data from the stream
    audio_data = stream.read(buffer_size)
    audio_data = np.frombuffer(audio_data, dtype=np.float32)

    # Perform pitch detection on the audio chunk
    pitch = pitch_detection(audio_data)[0]

    # Check if a valid pitch was detected
    if pitch != 0.0:
        # Convert pitch value to MIDI note number
        midi_note = aubio.freqtomidi(pitch)

        # Convert MIDI note number to frequency
        frequency = 440 * (2 ** ((midi_note - 69) / 12))

        # Basic human/non-human sound classification based on pitch and frequency
        if frequency > 80 and frequency < 300:
            classification = "Human"
        else:
            classification = "Non-human"

        # Print the detected pitch, frequency, and classification
        print("Detected pitch: {:.2f}".format(pitch))
        print("Corresponding frequency: {:.2f} Hz".format(frequency))
        print("Classification: {}".format(classification))
