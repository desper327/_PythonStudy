import tkinter as tk
from tkinter import filedialog


root = tk.Tk()
root.withdraw()
keys_file = filedialog.asksaveasfile(initialfile= 
                                     '_body_anim' + '.json',
                                      defaultextension=".json", filetypes=[("All Files", "*.*"), ("JSON file", "*.json")])