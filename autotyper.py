import tkinter as tk
from tkinter import ttk
import time
import pyautogui
import threading
import speech_recognition as sr

class AutoTyperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoTyper")

        self.text_to_type = tk.StringVar(value="")
        self.speed = tk.StringVar(value="60")
        self.delay = tk.StringVar(value="3")

        # Entry for user input or clipboard option
        self.text_label = ttk.Label(root, text="Text to type or select 'Copy from Clipboard':")
        self.text_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.text_entry = ttk.Entry(root, textvariable=self.text_to_type, width=30)
        self.text_entry.grid(row=0, column=1, padx=10, pady=5)
        self.clipboard_checkbox = ttk.Checkbutton(root, text="Copy from Clipboard", command=self.get_clipboard_text)
        self.clipboard_checkbox.grid(row=0, column=2, padx=10, pady=5, sticky="w")

        # Entry for typing speed
        self.speed_label = ttk.Label(root, text="Typing speed (words per minute):")
        self.speed_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.speed_entry = ttk.Entry(root, textvariable=self.speed, width=10)
        self.speed_entry.grid(row=1, column=1, padx=10, pady=5)

        # Entry for delay time
        self.delay_label = ttk.Label(root, text="Delay time (in seconds):")
        self.delay_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.delay_entry = ttk.Entry(root, textvariable=self.delay, width=10)
        self.delay_entry.grid(row=2, column=1, padx=10, pady=5)

        # Buttons
        self.start_button = ttk.Button(root, text="Start Autotyping", command=self.start_autotyping)
        self.start_button.grid(row=3, column=0, columnspan=3, pady=10, sticky="we")

        self.stop_button = ttk.Button(root, text="Stop Autotyping", command=self.stop_autotyping)
        self.stop_button.grid(row=4, column=0, columnspan=3, pady=5, sticky="we")

        # Initialize speech recognition
        self.recognizer = sr.Recognizer()

    def get_clipboard_text(self):
        try:
            self.text_to_type.set(self.root.clipboard_get())
        except tk.TclError:
            print("Failed to get text from clipboard.")

    def start_autotyping(self):
        text_to_type = self.get_text_to_type()
        speed = float(self.speed.get())
        delay_time = float(self.delay.get())

        self.root.iconify()  # Iconify (minimize) the main window during autotyping

        # Countdown before autotyping starts
        for i in range(int(delay_time), 0, -1):
            self.root.title(f"Autotyping in {i} seconds...")
            self.root.update()
            time.sleep(1)

        # Calculate typing duration based on speed
        words_per_second = speed / 60
        typing_duration = len(text_to_type.split()) / words_per_second

        # Type the text at the current cursor position using a separate thread
        autotype_thread = threading.Thread(target=self.autotype_thread, args=(text_to_type, typing_duration))
        autotype_thread.start()

    def stop_autotyping(self):
        pyautogui.typewrite("")  # Stop autotyping
        self.root.deiconify()  # Deiconify (restore) the main window
        self.root.title("AutoTyper")  # Reset window title

    def autotype_thread(self, text_to_type, typing_duration):
        # Type the text at the current cursor position
        pyautogui.typewrite(text_to_type, interval=0.1)  # You can adjust the interval if needed
        time.sleep(typing_duration)  # Wait for the typing to complete

        # Restore the main window after autotyping
        self.root.deiconify()
        self.root.title("AutoTyper")  # Reset window title

        print("Autotyping completed.")

    def get_text_to_type(self):
        # Get text from the entry field
        return self.text_to_type.get()

def main():
    root = tk.Tk()
    app = AutoTyperApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
