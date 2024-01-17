import tkinter as tk
from .base_screen import BaseScreen
import os
from .config_handler import ConfigHandler
from .keyboard import Keyboard
from tkinter import messagebox




class ConfigPage(BaseScreen):

    def __init__(self, master, app_instance):
        self.keyboard_instance = None
        super().__init__(master, "", app_instance, background="../images/config.png")
        self.current_directory = os.path.dirname(os.path.abspath(__file__))
        self.config_handler = ConfigHandler()

        # Parent frame to hold the grid
        parent_frame = tk.Frame(self)
        parent_frame.place(relx=0.5, rely=0.40, anchor=tk.CENTER)

        # Acquisition Duration Widgets
        acquisition_duration_label = tk.Label(parent_frame, text="Acquisition Duration (Seconds)")
        acquisition_duration_label.grid(row=0, column=0, padx=10, pady=10)
        self.acquisition_duration_edittext = tk.Entry(parent_frame, name="acquisition_duration")
        self.acquisition_duration_edittext.grid(row=0, column=1, padx=10, pady=10)
        self.acquisition_duration_edittext.insert(0, self.config_handler.get_acquisition_duration_in_secs())

        # mu1 Widgets
        mu1_label = tk.Label(parent_frame, text="mu1")
        mu1_label.grid(row=1, column=0, padx=10, pady=10)
        self.mu1_edittext = tk.Entry(parent_frame, name="mu1")
        self.mu1_edittext.grid(row=1, column=1, padx=10, pady=10)
        self.mu1_edittext.insert(0, self.config_handler.get_mu1())

        # mu2 Widgets
        mu2_label = tk.Label(parent_frame, text="mu2")
        mu2_label.grid(row=2, column=0, padx=10, pady=10)
        self.mu2_edittext = tk.Entry(parent_frame, name="mu2")
        self.mu2_edittext.grid(row=2, column=1, padx=10, pady=10)
        self.mu2_edittext.insert(0, self.config_handler.get_mu2())

        # std1 Widgets
        std1_label = tk.Label(parent_frame, text="std1")
        std1_label.grid(row=3, column=0, padx=10, pady=10)
        self.std1_edittext = tk.Entry(parent_frame, name="std1")
        self.std1_edittext.grid(row=3, column=1, padx=10, pady=10)
        self.std1_edittext.insert(0, self.config_handler.get_std1())

        # std2 Widgets
        std2_label = tk.Label(parent_frame, text="std2")
        std2_label.grid(row=4, column=0, padx=10, pady=10)
        self.std2_edittext = tk.Entry(parent_frame, name="std2")
        self.std2_edittext.grid(row=4, column=1, padx=10, pady=10)
        self.std2_edittext.insert(0, self.config_handler.get_std2())

        # Save Button
        save_image_path = os.path.join(self.current_directory, "../buttons/save.png")
        self.save_image = tk.PhotoImage(file=save_image_path)
        save_button = tk.Button(parent_frame, image=self.save_image, command=self.save_config, borderwidth=0,
                                highlightthickness=0)
        save_button.grid(row=5, column=0, pady=10)

        # Home Button
        home_image_path = os.path.join(self.current_directory, "../buttons/homeButton.png")
        self.home_image = tk.PhotoImage(file=home_image_path)
        home_button = tk.Button(parent_frame, image=self.home_image, command=self.back_to_home, borderwidth=0,
                                highlightthickness=0)
        home_button.grid(row=5, column=1, pady=10)

        # Bindings for the keyboard
        self.acquisition_duration_edittext.bind('<FocusIn>', self.show_keyboard)
        self.mu1_edittext.bind('<FocusIn>', self.show_keyboard)
        self.mu2_edittext.bind('<FocusIn>', self.show_keyboard)
        self.std1_edittext.bind('<FocusIn>', self.show_keyboard)
        self.std2_edittext.bind('<FocusIn>', self.show_keyboard)

    def show_entry_widgets(self, entry_widget):
        entry_widget.pack()  # Show the entry widget when the label is clicked

    def save_config(self):
        # Get the values from the Entry widgets
        acquisition_duration_value = self.acquisition_duration_edittext.get()
        mu1 = self.mu1_edittext.get()
        mu2 = self.mu2_edittext.get()
        std1 = self.std1_edittext.get()
        std2 = self.std2_edittext.get()

        # Update the JSON object
        self.config_handler.set_acquisition_duration_in_secs(acquisition_duration_value)
        self.config_handler.set_mu1(mu1)
        self.config_handler.set_mu2(mu2)
        self.config_handler.set_std1(std1)
        self.config_handler.set_std2(std2)

        # Show a messagebox to inform the user
        messagebox.showinfo("Info", "Configuration saved successfully!")

    def show_keyboard(self, event):
        if not self.keyboard_instance:
            self.keyboard_instance = Keyboard(self, event.widget)
            self.keyboard_instance.grid(row=1, column=0, columnspan=2, sticky="we")
        elif not self.keyboard_instance.winfo_exists():  # Check if the widget still exists
            self.keyboard_instance.destroy()  # Destroy the old instance
            self.keyboard_instance = Keyboard(self, event.widget)  # Create a new instance
            self.keyboard_instance.grid(row=1, column=0, columnspan=2, sticky="we")
        widget_x = 10
        widget_y = 400
        self.keyboard_instance.show(widget_x, widget_y)

    def back_to_home(self):
        from .home_screen import HomeScreen  # Import inside the function
        self.app_instance.switch_screen(HomeScreen)
