#!/bin/bash

# Create project folder
mkdir UIForWaterQualityRevised
cd UIForWaterQualityRevised

# Create screens directory
mkdir screens
cd screens

# Create screen modules
touch __init__.py
touch home_screen.py
touch new_experiment_screen.py
touch reference_sample_screen.py
touch bio_burden_sample_screen.py
touch result_page_screen.py
touch view_experiment_screen.py
touch config_screen.py

# Populate screen modules with basic content
echo "import tkinter as tk" >> home_screen.py
echo "from tkinter import messagebox" >> home_screen.py
echo "from screens.new_experiment_screen import NewExperiment" >> home_screen.py
# Repeat for other screen modules

# Return to project folder
cd ..

# Create main.py
touch main.py
echo "import tkinter as tk" >> main.py
echo "from screens.home_screen import HomeScreen" >> main.py
echo "from app import App" >> main.py
echo "" >> main.py
echo "if __name__ == \"__main__\":" >> main.py
echo "    app = App()" >> main.py
echo "    app.mainloop()" >> main.py

# Create app.py
touch app.py
echo "import tkinter as tk" >> app.py
echo "from screens.home_screen import HomeScreen" >> app.py
echo "" >> app.py
echo "class App(tk.Tk):" >> app.py
echo "    def __init__(self):" >> app.py
echo "        super().__init__()" >> app.py
echo "        self.title(\"Multi-Screen App\")" >> app.py
echo "        self.geometry(\"800x600\")" >> app.py
echo "        self.current_screen = None" >> app.py
echo "        self.switch_screen(HomeScreen)" >> app.py
echo "" >> app.py
echo "    def switch_screen(self, screen_class):" >> app.py
echo "        if self.current_screen:" >> app.py
echo "            self.current_screen.destroy()" >> app.py
echo "        self.current_screen = screen_class(self)" >> app.py
echo "        self.current_screen.pack(fill=\"both\", expand=True)" >> app.py
echo "" >> app.py
echo "if __name__ == \"__main__\":" >> app.py
echo "    app = App()" >> app.py
echo "    app.mainloop()" >> app.py

# Make main.py executable
chmod +x main.py

# Make the screens directory writable
chmod -R 777 screens
