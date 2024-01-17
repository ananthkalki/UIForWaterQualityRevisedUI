import tkinter as tk
from .base_screen import BaseScreen
import os
import json
from .config_handler import ConfigHandler
import pickle

class ResultPage(BaseScreen):
    def __init__(self, master, app_instance):
        super().__init__(master, "", app_instance, background="../images/results.png")
        current_directory = os.path.dirname(os.path.abspath(__file__))
        self.config_handler=ConfigHandler()
        # NEW EXPERIMENT
        start_button_path = os.path.join(current_directory, "../buttons/homeButton.png")
        self.start_image = tk.PhotoImage(file=start_button_path)
        self.start_button = tk.Button(self, image=self.start_image, command=self.back_to_home, borderwidth=0, highlightthickness=0)
        self.start_button.image = self.start_image  # Keep a reference to avoid garbage collection
        self.start_button.place(relx=0.75, rely=0.74)  # Center the button

        # Text view to the right of the back button
        self.result_text = tk.Text(self, height=2, width=18,  bg="#01002b", font=("Arial", 24), fg="red",
                           borderwidth=0, highlightthickness=0)
        self.result_text.tag_configure("center", justify='center')  # Step 1
        self.result_text.place(relx=0.42, rely=0.76)  # Place to the right of the button




        # Read and parse JSON file
        with open(os.path.join(current_directory,self.config_handler.get_current_experiment_path()+"/results.json"), "r") as file:
            data = json.load(file)

        if data["bioBurden"] == "Positive":
            self.result_text.config(fg="red")
            self.result_text.insert(tk.END, "BioBurden Positive")
        elif data["bioBurden"] == "Negative" :
            self.result_text.config(fg="green")
            self.result_text.insert(tk.END, "BioBurden Negative")
        else:
            self.result_text.config(fg="green")
            self.result_text.insert(tk.END, "NaN error!!")

        self.result_text.config(state=tk.DISABLED)


        #Other Text Boxes:
        self.refPeakCount = self.create_text_box(0.39, 0.40, str(int(data["refPeakCount"])))
        self.refTotalCount = self.create_text_box(0.65, 0.40, str(int(data["refTotalCount"])))
        self.samPeakCount = self.create_text_box(0.39, 0.60, str(int(data["samPeakCount"])))
        self.samTotalCount = self.create_text_box(0.65, 0.60, str(int(data["samTotalCount"])))

    def back_to_home(self):
        from .home_screen import HomeScreen  # Import inside the function
        self.app_instance.switch_screen(HomeScreen)

    def create_text_box(self, relx, rely, content=""):
        """Helper function to create and place a Text widget."""
        text_box = tk.Text(self, height=2, width=10, bg="#01002b", font=("Arial", 18), fg="white",
                           borderwidth=0, highlightthickness=0)
        text_box.insert(tk.END, str(content))
        text_box.config(state=tk.DISABLED)
        text_box.place(relx=relx, rely=rely)
        return text_box

