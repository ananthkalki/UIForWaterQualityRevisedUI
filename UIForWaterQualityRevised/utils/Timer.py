import tkinter as tk
from threading import Thread
import time


class TimerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Timer App")
        self.geometry("300x100")

        self.timer_label = tk.Label(self, text="00:00")
        self.timer_label.pack(pady=20)

        self.start_button = tk.Button(self, text="Start", command=self.start_timer)
        self.start_button.pack()

        self.timer_running = False
        self.seconds_left = 0

    def start_timer(self):
        if not self.timer_running:
            self.seconds_left = 60  # Set the initial timer duration (60 seconds in this example)
            self.timer_running = True
            self.start_button.config(state=tk.DISABLED)  # Disable the button while the timer is running
            self.update_timer_label()
            self.timer_thread = Thread(target=self.run_timer)
            self.timer_thread.start()

    def run_timer(self):
        while self.seconds_left > 0:
            self.seconds_left -= 1
            self.update_timer_label()
            time.sleep(1)  # Sleep for 1 second to create a 1-second timer tick
        self.timer_running = False
        self.start_button.config(state=tk.NORMAL)  # Enable the button when the timer is done
        # Perform your other process here while the timer is ticking

    def update_timer_label(self):
        minutes = self.seconds_left // 60
        seconds = self.seconds_left % 60
        timer_text = f"{minutes:02}:{seconds:02}"
        self.timer_label.config(text=timer_text)


if __name__ == "__main__":
    app = TimerApp()
    app.mainloop()
