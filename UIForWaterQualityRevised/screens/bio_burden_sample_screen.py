import tkinter as tk
import time
from .base_screen import BaseScreen
from .config_handler import ConfigHandler
from .processor import Processor
import os
import threading

class BioBurdenSample(BaseScreen):
    def __init__(self, master,app_instance):
        super().__init__(master, "BioBurden Sample", app_instance, background="../images/sample.png")
        self.curr_dir = os.path.dirname(os.path.abspath(__file__))
        current_directory = os.path.dirname(os.path.abspath(__file__))
        self.config_handler=ConfigHandler()
        self.processor = Processor()

        self.timer_label = tk.Label(self, text="Timer: "+str(self.config_handler.get_acquisition_duration_in_secs())+" seconds")
        self.timer_label.place(relx=0.45, rely=0.50)

        # NEW EXPERIMENT
        start_button_path = os.path.join(current_directory, "../buttons/start-measurement.png")
        self.start_image = tk.PhotoImage(file=start_button_path)
        self.start_button = tk.Button(self, image=self.start_image, command=self.start_bio_burden_measurement, borderwidth=0, highlightthickness=0)
        self.start_button.image = self.start_image  # Keep a reference to avoid garbage collection
        self.start_button.place(relx=0.37, rely=0.7)  # Center the button


        self.remaining_time = self.config_handler.get_acquisition_duration_in_secs()  # Initial timer value in seconds
        print(self.remaining_time)
    def update_timer_label(self):
        self.timer_label.config(text=f"Wait for {self.remaining_time} seconds")
        # if self.remaining_time > 0:
        #     self.remaining_time -= 1
        #     self.after(1000, self.update_timer_label)  # Update timer label every second


    def start_bio_burden_measurement(self):
        self.update_timer_label()
        self.start_button.config(state="disabled")
        # timerLabel.start()
        self.processor.StartTestForSample()
        self.start_button.config(text="Measurement in progress...")
        # testForSample.start()
        self.after((1000)+150, self.navTOResults)  # Simulate measurement delay
        

    def navTOResults(self):
        self.processor.Result()
        time.sleep(1)
        from .result_page_screen import ResultPage  # Import inside the function
        self.app_instance.switch_screen(ResultPage)

# Note: You need to implement the actual timer and measurement logic
