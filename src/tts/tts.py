import time
import os
import pyttsx3
import pygame

#ORIGINAL TTS, this is not needed as we are only sending text as before i was told that mqtt will be able to send files
# def save_text(text_box):
#     # text = text_box.get("1.0", "end-1c")  # Get the text from the text box
#     
#     # Initialize the TTS engine
#     engine = pyttsx3.init()

#     # to slow down the speech
#     engine.setProperty('rate', 120)

#     # Convert text to speech
#     engine.save_to_file(text_box, "saved_audio.wav")
#     engine.runAndWait()

def playNdelete(text):
    # Initialize the TTS engine
    engine = pyttsx3.init()

    # to slow down the speech
    engine.setProperty('rate', 120)

    # Convert text to speech
    engine.save_to_file(text, "saved_audio.wav")
    engine.save_to_file(text, "saved_audio.wav")
    engine.runAndWait()
    pygame.mixer.init()
    pygame.mixer.music.load("saved_audio.wav")

    # Play the audio
    pygame.mixer.music.play()

    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    # Close the audio mixer
    pygame.mixer.music.stop()
    pygame.mixer.quit()

    # Remove the file after a brief delay
    time.sleep(0.1)
    os.remove("saved_audio.wav")
    return "Audio played and deleted successfully."


# # Create the main window
# window = tk.Tk()
# window.title("TTS")

# # Create a text box
# text_box = tk.Text(window)
# text_box.pack()

# # Create a button to save the text as speech
# save_button = tk.Button(window, text="Save Text", command=save_text)
# save_button.pack()

# # Create a button to play and delete the saved audio
# play_button = tk.Button(window, text="Play and Delete", command=playNdelete)
# play_button.pack()

# # Run the main window loop
# window.mainloop()
