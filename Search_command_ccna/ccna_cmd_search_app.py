import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

# Function to load and parse the configuration file
def load_config():
    sections = {}
    current_section = None

    try:
        with open("cmd_config", "r") as fo:
            lines = fo.readlines()

        for line in lines:
            if line.startswith("CONFIG "):
                current_section = line.strip()[7:]  # Remove "CONFIG " prefix
                sections[current_section] = []
            elif line.startswith("END_"):
                current_section = None
            elif current_section:
                sections[current_section].append(line)

        return sections
    except FileNotFoundError:
        messagebox.showerror("Error", "File 'cmd_config' not found.")
        return None

# Function to handle user input and display section content
def show_section(event=None):
    user_input = entry.get().strip()
    
    if user_input == 'q':
        root.destroy()
        return
    
    found_section = None

    for section, content in sections.items():
        if user_input in section:
            found_section = section
            break

    if found_section:
        text_area.config(state=tk.NORMAL)
        text_area.delete('1.0', tk.END)
        for line in sections[found_section]:
            text_area.insert(tk.END, line)
        text_area.config(state=tk.DISABLED)
    else:
        messagebox.showwarning("Section Not Found", f"Section '{user_input}' not found in cmd_config. Please try again.")

# Create the main application window
root = tk.Tk()
root.title("Find config CCNA")

# Load configuration data
sections = load_config()

if not sections:
    root.destroy()
else:
    # Create GUI components
    label = tk.Label(root, text="Enter section name (e.g., static nat):")
    label.pack(pady=10)

    entry = tk.Entry(root, width=50)
    entry.pack()
    entry.focus_set()  # Set default focus to the entry widget
    
    # Bind Enter key to show_section function
    entry.bind("<Return>", show_section)

    show_button = tk.Button(root, text="Show Section", command=show_section)
    show_button.pack(pady=10)

    text_area = scrolledtext.ScrolledText(root, width=80, height=20, wrap=tk.WORD)
    text_area.pack(padx=10, pady=10)
    text_area.config(state=tk.DISABLED)

    # Start the main GUI loop
    root.mainloop()
