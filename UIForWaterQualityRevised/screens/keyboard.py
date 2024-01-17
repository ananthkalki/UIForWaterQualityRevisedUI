import tkinter as tk


class Keyboard(tk.Frame):
    def __init__(self, parent, text_widget):
        super().__init__(parent)
        self.text_widget = text_widget
        self.create_keyboard()

    def create_keyboard(self):
        # Define the keyboard layout
        keys = [
            ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', 'Backspace', '='],
            ['Tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\\'],
            ['Caps ', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'", 'Enter', 'DONE'],
            ['Shift', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'Shift', 'Space'],
        ]

        for i, row in enumerate(keys):
            for j, key in enumerate(row):
                button_height = 2
                button_width = 2  # Set width for regular keys to 3 characters
                column_span = 2
                if len(key) > 2:
                    button_height = 2
                    button_width = 3  # Adjust the width for keys with names longer than two characters
                button = tk.Button(self, text=key, command=lambda k=key: self.press(k), height=button_height,
                                   width=button_width if key != 'Space' else 20)  # Adjust width for the space key
                button.grid(row=i, column=j, sticky='nsew', padx=1, pady=1)
                self.grid_columnconfigure(j, weight=1)
            self.grid_rowconfigure(i, weight=1)

    def press(self, key):
        if key == 'Backspace':
            if isinstance(self.text_widget, tk.Entry):
                current_text = self.text_widget.get()
                self.text_widget.delete(len(current_text) - 1)
            else:  # Assuming it's a Text widget or similar
                current_text = self.text_widget.get("1.0", tk.END)
                self.text_widget.delete("1.0", tk.END)
                self.text_widget.insert(tk.END, current_text[:-2])  # Remove the last character and newline
        elif key == 'Space':
            self.text_widget.insert(tk.END, ' ')
        elif key == 'Enter':
            self.text_widget.insert(tk.END, '\n')
        elif key == 'DONE':
            self.destroy()  # Close the keyboard
        else:
            self.text_widget.insert(tk.END, key)

    def show(self, x, y):
        # Position the keyboard at the given x and y coordinates
        self.place(x=x, y=y)

    def hide(self):
        # Hide the keyboard
        self.place_forget()
