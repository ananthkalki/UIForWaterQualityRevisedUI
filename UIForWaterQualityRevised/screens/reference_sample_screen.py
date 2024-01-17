import os
import tkinter as tk

from .base_screen import BaseScreen
from .config_handler import ConfigHandler
from .processor import Processor

BuzzerPin = 21 ###BCM is 21 PIN 40


class ReferenceSample(BaseScreen):

    def __init__(self, master, app_instance):
        super().__init__(master, "", app_instance, background="../images/ref.png")
        self.curr_dir = os.path.dirname(os.path.abspath(__file__))
        current_directory = os.path.dirname(os.path.abspath(__file__))
        self.config_handler=ConfigHandler()
        self.processor = Processor()

        self.timer_label = tk.Label(self, text="Wait for "+str(self.config_handler.get_acquisition_duration_in_secs())+" seconds")
        self.timer_label.place(relx=0.45, rely=0.50)


        # NEW EXPERIMENT
        start_button_path = os.path.join(current_directory, "../buttons/start-measurement.png")
        self.start_image = tk.PhotoImage(file=start_button_path)
        self.start_button = tk.Button(self, image=self.start_image, command=self.start_reference_measurement, borderwidth=0, highlightthickness=0)
        self.start_button.image = self.start_image  # Keep a reference to avoid garbage collection
        self.start_button.place(relx=0.25, rely=0.7)  # Center the button

        # Home Button
        home_image_path = os.path.join(current_directory, "../buttons/homeButton.png")
        self.home_image = tk.PhotoImage(file=home_image_path)
        self.home_button = tk.Button(self, image=self.home_image, command=self.back_to_home, borderwidth=0,
                                     highlightthickness=0)
        self.home_button.place(relx=0.55, rely=0.7)

        self.remaining_time = self.config_handler.get_acquisition_duration_in_secs()  # Initial timer value in seconds
        print(self.remaining_time)

    def update_timer_label(self):
        self.timer_label.config(text=f"Wait for {self.remaining_time} seconds")
        # if self.remaining_time > 0:
        #     self.remaining_time -= 1
        #     self.after(1000, self.update_timer_label)  # Update timer label every second

    def start_reference_measurement(self):
        self.update_timer_label()
        self.start_button.config(state="disabled")
        # timerLabel.start()
        self.processor.StartTestForReference()
        self.start_button.config(text="Measurement in progress...")
        # testForReference.start()
        self.after((1000)+150,self.start_bio_burden_sample)  # Simulate measurement delay
        
        # Implement start_reference_measurement logic
        # For demonstration purposes, let's simulate a measurement delay
                
    def start_bio_burden_sample(self):
        from .bio_burden_sample_screen import BioBurdenSample  # Import inside the function
        self.app_instance.switch_screen(BioBurdenSample)

    def back_to_home(self):
        from .home_screen import HomeScreen  # Import inside the function
        self.app_instance.switch_screen(HomeScreen)

# Note: You need to implement the actual timer and reference measurement logic
