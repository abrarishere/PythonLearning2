from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.uix.popup import Popup
import pyautogui
import pyperclip
from tqdm import tqdm
import time

class AutotyperApp(App):
    def build(self):
        self.text_to_type = ""
        self.typing_speed = 0
        self.typing_process = None
        self.progress_value = 0

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Label and entry for text input
        text_label = Label(text="Enter the text you want to type:")
        layout.add_widget(text_label)
        self.text_entry = TextInput(multiline=False)
        layout.add_widget(self.text_entry)

        # Label and entry for typing speed
        speed_label = Label(text="Enter the typing speed (characters per second):")
        layout.add_widget(speed_label)
        self.speed_entry = TextInput(multiline=False)
        layout.add_widget(self.speed_entry)

        # Start and stop buttons
        self.start_button = Button(text="Start Typing")
        self.start_button.bind(on_press=self.start_typing)
        layout.add_widget(self.start_button)

        self.stop_button = Button(text="Stop Typing", disabled=True)
        self.stop_button.bind(on_press=self.stop_typing)
        layout.add_widget(self.stop_button)

        # Progress bar
        self.progress_bar = ProgressBar(max=100)
        layout.add_widget(self.progress_bar)

        return layout

    def start_typing(self, instance):
        # Get text and speed from entries
        self.text_to_type = self.text_entry.text
        typing_speed_str = self.speed_entry.text

        # Validate speed input
        try:
            self.typing_speed = float(typing_speed_str)
            if self.typing_speed <= 0:
                raise ValueError("Speed must be positive")
        except ValueError as e:
            self.show_popup("Error", f"Invalid typing speed: {e}")
            return

        # Disable the start button and enable the stop button
        self.start_button.disabled = True
        self.stop_button.disabled = False

        # Start typing process in a separate thread
        self.typing_process = Clock.schedule_once(self.type_text, 1)

    def type_text(self, dt):
        # Copy text to clipboard and type it out
        pyperclip.copy(self.text_to_type)

        # Calculate the total time needed
        total_time = len(self.text_to_type) / self.typing_speed

        # Start typing with a progress bar
        for _ in tqdm(range(int(total_time * 10)), position=1, leave=False):
            pyautogui.typewrite(pyperclip.paste(), interval=0.1 / self.typing_speed)
            self.progress_value = (_ + 1) * 100 / (total_time * 10)
            self.progress_bar.value = self.progress_value

        # Enable the start button and disable the stop button
        self.start_button.disabled = False
        self.stop_button.disabled = True

        # Reset progress bar
        self.progress_value = 0
        self.progress_bar.value = 0

    def stop_typing(self, instance):
        # Cancel the typing process and enable the start button
        Clock.unschedule(self.typing_process)
        self.start_button.disabled = False
        self.stop_button.disabled = True

        # Reset progress bar
        self.progress_value = 0
        self.progress_bar.value = 0

    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=message))
        close_button = Button(text="Close")
        close_button.bind(on_press=lambda *args: popup.dismiss())
        content.add_widget(close_button)

        popup = Popup(title=title, content=content, size_hint=(None, None), size=(300, 150))
        popup.open()

if __name__ == '__main__':
    AutotyperApp().run()