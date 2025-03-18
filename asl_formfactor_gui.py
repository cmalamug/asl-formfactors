import tkinter as tk

# List of texts to cycle through
texts = ["Hello, World!", "Press Space to Change", "Tkinter is fun!", "Python GUI"]
current_index = 0  # Track the current text index

def change_text(event=None):
    print(f"Key pressed: {event.keysym}") 
    global current_index
    current_index = (current_index + 1) % len(texts)  # Cycle through texts
    label.config(text=texts[current_index])

# Create main window
root = tk.Tk()
root.title("Text Changer")
root.geometry("400x200")

# Create label to display text
label = tk.Label(root, text=texts[current_index], font=("Arial", 20))
label.pack(expand=True)

# Bind spacebar to change text
root.bind("<space>", change_text)
root.focus_set()

# Run the Tkinter event loop
root.mainloop()