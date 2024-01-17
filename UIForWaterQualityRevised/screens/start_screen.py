from .base_screen import BaseScreen
import os
import tkinter as tk
class StartScreen(BaseScreen):
    def __init__(self, master, app_instance):
        super().__init__(master, "", app_instance, background="../images/start.png")
        # ... [rest of the initialization code remains unchanged]
        current_directory = os.path.dirname(os.path.abspath(__file__))
        start_image_path = os.path.join(current_directory, "../buttons/start.png")
        self.start_image = tk.PhotoImage(file=start_image_path)

        # Create a button with the image
        start_button = tk.Button(self, image=self.start_image, command=self.NavToHome, borderwidth=0, highlightthickness=0)
        start_button.image = self.start_image  # Keep a reference to avoid garbage collection
        start_button.place(relx=0.15, rely=0.6, anchor="w")  # Center the button

    def NavToHome(self):
        from .home_screen import HomeScreen  # Import inside the function
        self.app_instance.switch_screen(HomeScreen)
