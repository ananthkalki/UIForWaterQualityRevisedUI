import tkinter as tk
import tkinter.messagebox as messagebox
from .base_screen import BaseScreen
import os
import subprocess
import re
from .keyboard import Keyboard


class WifiPage(BaseScreen):
    def __init__(self, master, app_instance):
        super().__init__(master, "", app_instance, background="../images/empty.png")
        self.current_directory = os.path.dirname(os.path.abspath(__file__))

        # Title Label
        self.title_label = tk.Label(self, text="Available Networks")
        self.title_label.pack(pady=10)

        # Listbox for networks
        self.network_listbox = tk.Listbox(self)
        self.network_listbox.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        self.network_listbox.bind('<<ListboxSelect>>', self.on_network_select)

        self.home_image_path = os.path.join(self.current_directory, "../buttons/homeButton.png")
        self.home_image = tk.PhotoImage(file=self.home_image_path)
        self.home_button = tk.Button(self, image=self.home_image, command=self.back_to_home, borderwidth=0, highlightthickness=0)
        self.home_button.place(relx=0.6, rely=0.85)  # You can adjust the position as required
        
        # Password Entry
        self.password_label = tk.Label(self, text="Enter Password")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self, show='*')
        self.password_entry.pack(pady=5)

        # Connect Button
        self.connect_btn = tk.Button(self, text="Add to WPA_SUPPLICANT", command=self.connect_to_network)
        self.connect_btn.pack(pady=10)

        # Load networks on initialization
        self.load_networks()
        self.keyboard_instance = None  # Initialize keyboard instance as None

    def load_networks(self):
        # Run the command to get available networks
        try:
            result = subprocess.check_output(['sudo', 'iwlist', 'wlan0', 'scan'])
            networks = re.findall(r'ESSID:"(.*?)"', result.decode('utf-8'))
            for net in networks:
                self.network_listbox.insert(tk.END, net)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to retrieve networks. Error: {e}")

    def on_network_select(self, event):
        # Show the keyboard for the password entry when a network is selected
        if not self.keyboard_instance:
            self.keyboard_instance = Keyboard(self, self.password_entry)
            self.keyboard_instance.pack(side=tk.BOTTOM, fill=tk.BOTH)

    def connect_to_network(self):
        selected_network = self.network_listbox.get(self.network_listbox.curselection())
        password = self.password_entry.get()

        try:
            # Update wpa_supplicant.conf with network details
            with open("/etc/wpa_supplicant/wpa_supplicant.conf", "a") as conf_file:
                conf_file.write(f'network={{\n\tssid="{selected_network}"\n\tpsk="{password}"\n\tkey_mgmt=WPA-PSK\n}}')

            # Restart the network interface
            subprocess.call(['sudo', 'wpa_cli', 'reconfigure'])
            messagebox.showinfo("Success", f"ADDED {selected_network} to wpa_supplicant. Please reboot for Auto Connect.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect to {selected_network}. Error: {e}")

    def show_keyboard(self, event):
        if not self.keyboard_instance:
            self.keyboard_instance = Keyboard(self, event.widget)
            self.keyboard_instance.pack(side=tk.BOTTOM, fill=tk.BOTH)
    
    def back_to_home(self):
        from .home_screen import HomeScreen  # Import inside the function
        self.app_instance.switch_screen(HomeScreen)
