import os
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import random
from PIL import Image, ImageTk

# Absolute paths for the icon images
script_dir = os.path.dirname(os.path.abspath(__file__))
play_icon_path = os.path.join(script_dir, 'play_icon.png')
pause_icon_path = os.path.join(script_dir, 'pause_icon.png')

class GraphPlotterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Plotter")
        self.root.geometry("1400x900")
        
        self.track_values = {
            "iterations": random.randint(50, 1000),
            "function": 0,
            "n": random.randint(100, 2000),
            "m": random.randint(100, 2000)
        }

        self.is_playing = False
        self.create_widgets()
        self.update_sliders()
        self.plot_graph()

    def create_widgets(self):
        # Menu
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Left frame for controls
        control_frame = ttk.Frame(self.root)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Combo Box for function selection
        self.combo_box = ttk.Combobox(control_frame, values=[0, 1, 2])
        self.combo_box.current(0)
        self.combo_box.bind("<<ComboboxSelected>>", self.on_combo_change)
        self.combo_box.pack(pady=5)

        # Sliders and Text Fields
        ttk.Label(control_frame, text="Iterations").pack(pady=5)
        self.iteration_slider = ttk.Scale(control_frame, from_=50, to_=1000, orient=tk.HORIZONTAL)
        self.iteration_slider.pack(pady=5)
        self.iteration_slider.bind("<Motion>", self.on_slider_change)
        self.text_iteration = ttk.Entry(control_frame)
        self.text_iteration.pack(pady=5)

        ttk.Label(control_frame, text="n").pack(pady=5)
        self.n_slider = ttk.Scale(control_frame, from_=100, to_=2000, orient=tk.HORIZONTAL)
        self.n_slider.pack(pady=5)
        self.n_slider.bind("<Motion>", self.on_slider_change)
        self.text_n = ttk.Entry(control_frame)
        self.text_n.pack(pady=5)

        ttk.Label(control_frame, text="m").pack(pady=5)
        self.m_slider = ttk.Scale(control_frame, from_=100, to_=2000, orient=tk.HORIZONTAL)
        self.m_slider.pack(pady=5)
        self.m_slider.bind("<Motion>", self.on_slider_change)
        self.text_m = ttk.Entry(control_frame)
        self.text_m.pack(pady=5)

        # Filler frame to push other widgets to the top
        filler_frame = ttk.Frame(control_frame)
        filler_frame.pack(expand=True, fill=tk.BOTH)

        # Speed Control
        ttk.Label(control_frame, text="Speed").pack(pady=5)
        self.speed_entry = ttk.Spinbox(control_frame, from_=1, to_=10, width=5)
        self.speed_entry.pack(pady=5)
        self.speed_entry.set(1)

        # Play and Pause Buttons with Icons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(side=tk.BOTTOM, pady=5)

        # Resize icons
        play_icon = Image.open(play_icon_path)
        play_icon = play_icon.resize((30, 30))
        play_icon = ImageTk.PhotoImage(play_icon)

        pause_icon = Image.open(pause_icon_path)
        pause_icon = pause_icon.resize((30, 30))
        pause_icon = ImageTk.PhotoImage(pause_icon)

        self.play_button = ttk.Button(button_frame, image=play_icon, command=self.play)
        self.play_button.image = play_icon  # Keep a reference to avoid garbage collection
        self.play_button.pack(side=tk.LEFT, padx=5)

        self.pause_button = ttk.Button(button_frame, image=pause_icon, command=self.pause)
        self.pause_button.image = pause_icon  # Keep a reference to avoid garbage collection
        self.pause_button.pack(side=tk.LEFT, padx=5)

        # Right frame for the plot
        plot_frame = ttk.Frame(self.root)
        plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Matplotlib Figure
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def update_sliders(self):
        self.iteration_slider.set(self.track_values["iterations"])
        self.n_slider.set(self.track_values["n"])
        self.m_slider.set(self.track_values["m"])

    def on_combo_change(self, event):
        self.track_values["function"] = int(self.combo_box.get())
        self.plot_graph()

    def on_slider_change(self, event):
        self.track_values["iterations"] = int(self.iteration_slider.get())
        self.track_values["n"] = int(self.n_slider.get())
        self.track_values["m"] = int(self.m_slider.get())
        self.plot_graph()

    def plot_graph(self):
        self.ax.clear()
        function = self.track_values["function"]
        n = self.track_values["n"]
        m = self.track_values["m"]
        iterations = self.track_values["iterations"]

        x_vals = []
        y_vals = []

        for i in range(iterations):
            if function == 0:
                x = np.cos(n * i) * np.cos(m * i)
                y = np.cos(n * i) * np.sin(m * i)
            elif function == 1:
                x = np.cos(n * n * i) * np.cos(m * i)
                y = np.cos(n * n * i) * np.sin(m * i)
            elif function == 2:
                x = np.cos(n * n * n * i) * np.cos(m * i)
                y = np.cos(n * n * n * i) * np.sin(m * i)
            
            x_vals.append(x)
            y_vals.append(y)
        
        self.ax.plot(x_vals, y_vals, color='blue', linestyle='-', linewidth=1.5)
        self.canvas.draw()

        # Update text fields
        self.text_iteration.delete(0, tk.END)
        self.text_iteration.insert(0, str(iterations))
        self.text_n.delete(0, tk.END)
        self.text_n.insert(0, str(n))
        self.text_m.delete(0, tk.END)
        self.text_m.insert(0, str(m))

    def play(self):
        self.is_playing = True
        self.increment_iterations()

    def pause(self):
        self.is_playing = False

    def increment_iterations(self):
        if self.is_playing:
            speed = int(self.speed_entry.get())
            self.track_values["iterations"] += speed
            if self.track_values["iterations"] > 1000:
                self.track_values["iterations"] = 50
            self.iteration_slider.set(self.track_values["iterations"])
            self.plot_graph()
            self.root.after(100, self.increment_iterations)  # Schedule the next update

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphPlotterApp(root)
    root.mainloop()
