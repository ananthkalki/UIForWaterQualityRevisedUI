import tkinter as tk
import os
import shutil
from tkinter import messagebox
from .base_screen import BaseScreen
class ViewExperimentPage(BaseScreen):
    def __init__(self, master, app_instance):
        super().__init__(master, "", app_instance, background="../images/exps.png")
        self.current_directory = os.path.dirname(os.path.abspath(__file__))
        self.raw_data_path = os.path.abspath(os.path.join(self.current_directory, "../RAW_DATA"))

        # Calculate dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        frame_width = 0.4 * screen_width  # 40% of the screen width for each frame
        frame_height = 0.6 * screen_height  # 60% of the screen height
        vertical_padding = 0.2 * screen_height  # 20% of the screen height for top padding
        horizontal_padding = 0.1 * screen_width  # 10% of the screen width for left and right padding

        # Frame for Date folders with a title
        self.date_frame = ScrollableFrame(self, bg=None, width=frame_width, height=frame_height)  # Set background to None for transparency
        self.date_frame.grid(row=0, column=0, sticky="nsew", pady=vertical_padding, padx=(horizontal_padding, 0))



        # Frame for ExpName_DateTime subfolders with a title
        self.subfolder_frame = ScrollableFrame(self, bg=None, width=frame_width, height=frame_height)
        self.subfolder_frame.grid(row=0, column=2, sticky="nsew", pady=vertical_padding, padx=(0, horizontal_padding))

        # Allow frames to expand and adjust according to window size
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)


        # Setup scrollable content for date_frame
        self.setup_scrollable_frame(self.date_frame)

        # Setup scrollable content for subfolder_frame
        self.setup_scrollable_frame(self.subfolder_frame)

        # Display folders initially
        self.show_date_folders()
        # Home Button
        Home_image_path = os.path.join(self.current_directory, "../buttons/homeButton.png")
        self.Home_image = tk.PhotoImage(file=Home_image_path)
        Home_button = tk.Button(self, image=self.Home_image, command=self.back_to_home, borderwidth=0)
        Home_button.image = self.Home_image  # Keep a reference to avoid garbage collection
        Home_button.place(relx=0.65, rely=0.015)  # Center the button

    def setup_scrollable_frame(self, parent_frame):
        canvas = tk.Canvas(parent_frame)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(parent_frame, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=scrollbar.set)

        frame_inside_canvas = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame_inside_canvas, anchor='nw')
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

        # Assign the frame inside the canvas to an attribute of the parent frame for easy access
        setattr(parent_frame, "content_frame", frame_inside_canvas)

    def show_date_folders(self):
        for widget in self.date_frame.content_frame.winfo_children():
            widget.destroy()

        folders = os.listdir(self.raw_data_path)
        for i, date_folder in enumerate(folders):
            date_button = tk.Button(self.date_frame.scrollable_frame, text=date_folder, width=20, anchor='w', command=lambda folder=date_folder: self.show_subfolders(folder))
            date_button.pack(fill=tk.X)
            export_button = tk.Button(self.date_frame.scrollable_frame, text="Export", command=lambda folder=date_folder: self.export_item(folder))
            export_button.pack(fill=tk.X)
            if i < len(folders) - 1:  # Don't add line after the last folder
                line = tk.Canvas(self.date_frame.scrollable_frame, height=1, bg="red")
                line.pack(fill=tk.X)

    def show_subfolders(self, date_folder):
        for widget in self.subfolder_frame.content_frame.winfo_children():
            widget.destroy()

        date_folder_path = os.path.join(self.raw_data_path, date_folder)
        subfolders = os.listdir(date_folder_path)
        for i, subfolder in enumerate(subfolders):
            subfolder_button = tk.Button(self.subfolder_frame.scrollable_frame, text=subfolder, width=20, anchor='w', command=lambda folder=os.path.join(date_folder, subfolder): self.export_item(folder))
            subfolder_button.pack(fill=tk.X)
            export_button = tk.Button(self.subfolder_frame.scrollable_frame, text="Export", command=lambda folder=os.path.join(date_folder, subfolder): self.export_item(folder))
            export_button.pack(fill=tk.X)
            if i < len(subfolders) - 1:  # Don't add line after the last subfolder
                line = tk.Canvas(self.subfolder_frame.scrollable_frame, height=1, bg="white")
                line.pack(fill=tk.X)

    def export_item(self, folder_name):
        # Define the paths
        source_path = os.path.join(self.raw_data_path, folder_name)

        # Check if a pen drive is connected
        mounted_devices = os.listdir('/media/pi/')

        if not mounted_devices:
            messagebox.showerror("Error", "No pen drives are connected!")
            return

        # If multiple devices are connected, you might want to let the user choose
        # For now, we just select the first device
        target_path = os.path.join('/media/pi/', mounted_devices[0], folder_name)

        # Copy the folder to the pen drive
        try:
            shutil.copytree(source_path, target_path)
            messagebox.showinfo("Success", f"Exported {folder_name} to pen drive!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export. Error: {str(e)}")

    def back_to_home(self):
        from .home_screen import HomeScreen  # Import inside the function
        self.app_instance.switch_screen(HomeScreen)


class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas)

        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

