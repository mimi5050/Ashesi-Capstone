import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import pygame
from gtts import gTTS
import tempfile


def text_to_speech():
    user_text = text_entry.get("1.0", tk.END).strip()

    if not user_text:
        status_label.config(text="Please enter text or upload a document.", foreground="red")
        return

    language = 'en'

    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        file_path = temp_file.name

    # Generate audio using gTTS and save it to the temporary file
    tts_object = gTTS(text=user_text, lang=language, slow=False)
    tts_object.save(file_path)

    # Play the audio using pygame
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    status_label.config(text="Audio generated and playing.", foreground="green")


def upload_document():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            content = file.read()
            text_entry.delete("1.0", tk.END)
            text_entry.insert(tk.END, content)


def restart_interface():
    # Clear text entry
    text_entry.delete("1.0", tk.END)

    # Stop any current playback
    pygame.mixer.music.stop()

    # Clear status label
    status_label.config(text="", foreground="black")


# Initialize pygame mixer
pygame.mixer.init()

# Create the main window
root = tk.Tk()
root.title("Text-to-Speech Application")

# Create and pack GUI elements
text_entry = tk.Text(root, wrap="word", width=40, height=5)
text_entry.pack(pady=10)

upload_button = ttk.Button(root, text="Upload Document", command=upload_document)
upload_button.pack()

play_button = ttk.Button(root, text="Play Audio", command=text_to_speech)
play_button.pack()

restart_button = ttk.Button(root, text="Restart Interface", command=restart_interface)
restart_button.pack()

status_label = ttk.Label(root, text="", foreground="black")
status_label.pack(pady=10)

# Run the main loop
root.mainloop()
