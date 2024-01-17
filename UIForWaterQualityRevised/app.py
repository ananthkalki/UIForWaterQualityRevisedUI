import tkinter as tk
from screens.home_screen import HomeScreen
from screens.start_screen import StartScreen


global currentExperiment
global currentExperimentPath
currentExperiment = ""
currentExperimentPath = ""

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Multi-Screen App")
        self.geometry("1024x600")

        self.bg_frame = tk.Frame(self, bg="#00022F")
        self.bg_frame.pack(fill="both", expand=True)

        self.current_screen = None
        self.switch_screen(StartScreen)

    def switch_screen(self, screen_class):
        if self.current_screen:
            self.current_screen.destroy()
        self.current_screen = screen_class(self.bg_frame, self)  # Passing self as app_instance
        self.current_screen.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = App()
    app.mainloop()
