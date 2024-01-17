import tkinter as tk
import os

class BaseScreen(tk.Frame):
    def __init__(self, master, title, app_instance, background="../images/background.png"):
        super().__init__(master)
        self.app_instance = app_instance

        # Use an absolute file path for the background image
        current_directory = os.path.dirname(os.path.abspath(__file__))
        background_image_path = os.path.join(current_directory,background )
        self.background_image = tk.PhotoImage(file=background_image_path)

        # Create a label to display the background image
        background_label = tk.Label(self, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Resize the label to fit the window

        # Set the title
        # title_label = tk.Label(self, text=title, font=("Helvetica", 24))
        # title_label.pack()
