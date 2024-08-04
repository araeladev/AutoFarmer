import tkinter as tk
from tkinter import PhotoImage
import random
import time
import threading
import pynput.keyboard as keyboard
import os
from PIL import Image, ImageTk

class AutoFarmerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoFarmer by Araela.")
        self.root.configure(bg="black")
        self.set_window_icon()
        self.is_running = False
        self.last_click_times = []
        self.max_click_history = 5
        self.main_frame = tk.Frame(self.root, bg="black")
        self.main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        self.start_button = self.create_rounded_button("Start", self.start_auto_clicker, "#d6a1d7", "#b57edc")
        self.start_button.pack(pady=10)
        self.stop_button = self.create_rounded_button("Stop", self.stop_auto_clicker, "#d6a1d7", "#b57edc")
        self.stop_button.pack(pady=10)
        self.footer_label = tk.Label(self.root, text="Made by Araela.", bg="black", fg="#4b0082", font=("Arial", 12))
        self.footer_label.place(x=10, y=self.root.winfo_height() - 30, anchor=tk.W)
        self.root.bind("<Configure>", self.update_footer_position)
        self.keyboard_controller = keyboard.Controller()
    
    def set_window_icon(self):
        """Set the window icon with a png. (It can be anything)"""
        try:
            icon_path = "Placeholder_Icon.png"  # Path to your preferred picture!
            if os.path.exists(icon_path):
                image = Image.open(icon_path)
                photo = ImageTk.PhotoImage(image)
                self.root.tk.call('wm', 'iconphoto', self.root._w, photo)
            else:
                print("There's no Icon: 'Placeholder_Icon.png' Add yours to this directory!")
        except Exception as e:
            print(f"Error setting the icon: {e}")

    def create_rounded_button(self, text, command, color_normal, color_hover):
        """Create a button with rounded corners and hover effects."""
        frame = tk.Frame(self.main_frame, bg="black", width=150, height=50)
        frame.pack_propagate(False)  # Prevent frame from resizing to fit content
        # Create a canvas to draw the rounded button and text
        canvas = tk.Canvas(frame, width=150, height=50, bg="black", highlightthickness=0)
        self.button_color = color_normal
        self.button_color_hover = color_hover
        self.button = canvas.create_oval(0, 0, 150, 50, fill=self.button_color, outline=self.button_color)
        self.text = canvas.create_text(75, 25, text=text, fill="white", font=("Arial", 14))
        canvas.pack()
        # Bind hover and press events
        canvas.bind("<Enter>", lambda event: self.on_hover(event, canvas))
        canvas.bind("<Leave>", lambda event: self.on_leave(event, canvas))
        canvas.bind("<Button-1>", lambda event: self.on_press(event, canvas, command))
        
        return frame

    def on_hover(self, event, canvas):
        """Change color on hover. (This is so cool tbh)"""
        canvas.itemconfig(self.button, fill=self.button_color_hover)
        canvas.itemconfig(self.text, fill="white")

    def on_leave(self, event, canvas):
        """Revert color on leave."""
        canvas.itemconfig(self.button, fill=self.button_color)
        canvas.itemconfig(self.text, fill="white")

    def on_press(self, event, canvas, command):
        """Animate button press and execute command."""
        original_color = self.button_color
        animation_color = "#a2a2a2"
        self.button_color = animation_color
        canvas.itemconfig(self.button, fill=self.button_color)
        canvas.itemconfig(self.text, fill="white")
        self.root.after(100, lambda: self.reset_button_color(canvas, original_color, command))

    def reset_button_color(self, canvas, original_color, command):
        """Reset button color after animation and execute command."""
        self.button_color = original_color
        canvas.itemconfig(self.button, fill=self.button_color)
        canvas.itemconfig(self.text, fill="white")
        command()

    def start_auto_clicker(self):
        if not self.is_running:
            self.is_running = True
            self.auto_clicker_thread = threading.Thread(target=self.auto_click)
            self.auto_clicker_thread.start()
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
    
    def stop_auto_clicker(self):
        if self.is_running:
            self.is_running = False
            self.auto_clicker_thread.join()
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
    
    def auto_click(self):
        while self.is_running:
            now = time.time()
            delay = random.randint(60, 90) # We make sure to not make it press the key at the same time to avoid certain penalties...
            
            while delay in self.last_click_times:
                delay = random.randint(60, 90) 
            
            self.last_click_times.append(delay)
            if len(self.last_click_times) > self.max_click_history:
                self.last_click_times.pop(0)
            
            time.sleep(delay)
            self.press_key('1') # Change this to any key in case you want to use it for any other game!

    def press_key(self, key):
        """Simulates a key press."""
        key = keyboard.KeyCode.from_char(key)
        self.keyboard_controller.press(key)
        time.sleep(0.05)  # Duration of key press
        self.keyboard_controller.release(key)

    def update_footer_position(self, event):
        """Makes sure that the footer text stays on even if the window is resized."""
        self.footer_label.place(x=10, y=self.root.winfo_height() - 30, anchor=tk.W)

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoFarmerApp(root)
    root.geometry("300x200")
    root.mainloop()
