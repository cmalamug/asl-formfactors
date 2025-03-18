import tkinter as tk
import cv2
from PIL import Image, ImageTk


form_factors = ["Glasses", "Glasses & Bracelet", "Glasses & Ring", "Glasses & Glove"]
accuracies = ["68%", "92%", "100%"]


sentences = {
    "68%": [
        ("My family is small. It consists of my mother, father, younger sister, and me", "MY FAMILY SMALL MOTHER FATHER YOUNG SISTER I FINISH", "MY FAMILY SMALL MOTHER FATHER YOUNG WIFE I BLOWN-AWAY"),
        ("My family has a total of six grandchildren.", "MY FAMILY HAVE TOTAL SIX GRANDCHILDREN", "MY FAMILY HAVE TOTAL SIX GRANDCHILDREN"),
        ("My family recently moved to New York City because my father was transferred for work at IBM", "FAMILY MOVE RECENT WHERE NYC WHY FATHER THERE WORK TRANSFER ns-IBM", "MY SISTER WANT HER BIRTHDAY WHAT"),
        ("What does my sister want for her birthday?", "MY SISTER WANT HER BIRTHDAY WHAT", "MY SISTER WANT HER BIRTHDAY WHAT"),
        ("What does my sister want for her birthday?", "MY SISTER WANT HER BIRTHDAY WHAT", "MY SISTER WANT HER BIRTHDAY WHAT"),
        ("What does my sister want for her birthday?", "MY SISTER WANT HER BIRTHDAY WHAT", "MY SISTER WANT HER BIRTHDAY WHAT"),
        ("What does my sister want for her birthday?", "MY SISTER WANT HER BIRTHDAY WHAT", "MY SISTER WANT HER BIRTHDAY WHAT"),
        ("What does my sister want for her birthday?", "MY SISTER WANT HER BIRTHDAY WHAT", "MY SISTER WANT HER BIRTHDAY WHAT"),
        ("What does my sister want for her birthday?", "MY SISTER WANT HER BIRTHDAY WHAT", "MY SISTER WANT HER BIRTHDAY WHAT"),
        ("What does my sister want for her birthday?", "MY SISTER WANT HER BIRTHDAY WHAT", "MY SISTER WANT HER BIRTHDAY WHAT"),
        ("What does my sister want for her birthday?", "MY SISTER WANT HER BIRTHDAY WHAT", "MY SISTER WANT HER BIRTHDAY WHAT"),
        ("What does my sister want for her birthday?", "MY SISTER WANT HER BIRTHDAY WHAT", "MY SISTER WANT HER BIRTHDAY WHAT"),
        ("What does my sister want for her birthday?", "MY SISTER WANT HER BIRTHDAY WHAT", "MY SISTER WANT HER BIRTHDAY WHAT"),
        ("What does my sister want for her birthday?", "MY SISTER WANT HER BIRTHDAY WHAT", "MY SISTER WANT HER BIRTHDAY WHAT"),
        ("What does my sister want for her birthday?", "MY SISTER WANT HER BIRTHDAY WHAT", "MY SISTER WANT HER BIRTHDAY WHAT"),
        ("What does my sister want for her birthday?", "MY SISTER WANT HER BIRTHDAY WHAT", "MY SISTER WANT HER BIRTHDAY WHAT"),
        ("What does my sister want for her birthday?", "MY SISTER WANT HER BIRTHDAY WHAT", "MY SISTER WANT HER BIRTHDAY WHAT"),
        ("What does my sister want for her birthday?", "MY SISTER WANT HER BIRTHDAY WHAT", "MY SISTER WANT HER BIRTHDAY WHAT"),
        ("What does my sister want for her birthday?", "MY SISTER WANT HER BIRTHDAY WHAT", "MY SISTER WANT HER BIRTHDAY WHAT"),
        ("What does my sister want for her birthday?", "MY SISTER WANT HER BIRTHDAY WHAT", "MY SISTER WANT HER BIRTHDAY WHAT"),
        ("What does my sister want for her birthday?", "MY SISTER WANT HER BIRTHDAY WHAT", "MY SISTER WANT HER BIRTHDAY WHAT"),
        ("What does my sister want for her birthday?", "MY SISTER WANT HER BIRTHDAY WHAT", "MY SISTER WANT HER BIRTHDAY WHAT"),
        ("What does my sister want for her birthday?", "MY SISTER WANT HER BIRTHDAY WHAT", "MY SISTER WANT HER BIRTHDAY WHAT"),
        ("What does my sister want for her birthday?", "MY SISTER WANT HER BIRTHDAY WHAT", "MY SISTER WANT HER BIRTHDAY WHAT"),
        ("What does my sister want for her birthday?", "MY SISTER WANT HER BIRTHDAY WHAT", "MY SISTER WANT HER BIRTHDAY WHAT")
    ],
    "92%": [
        ("Where is the nearest grocery store?", "GROCERY STORE WHERE", "GROCERY STORE WHERE"),
        
    ],
    "100%": [
        ("Can you help me with my homework?", "YOU HELP ME HOMEWORK CAN", "YOU HELP ME HOMEWORK CAN"),
        
    ]
}

class ResearchInterviewApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Research Interview")

        self.current_condition = None
        self.current_index = 0
        self.camera_on = False
        self.cap = None

        self.label = tk.Label(root, text="Select a Condition", font=("Arial", 18))
        self.label.pack(pady=20)

        self.button_frame = tk.Frame(root)
        self.button_frame.pack()

        # Create buttons for all conditions
        for form_factor in form_factors:
            for accuracy in accuracies:
                condition_name = f"{form_factor} - {accuracy}"
                btn = tk.Button(self.button_frame, text=condition_name, command=lambda f=form_factor, a=accuracy: self.start_condition(f, a))
                btn.pack(side=tk.LEFT, padx=5)

        self.sentence_label = tk.Label(root, text="", font=("Arial", 16))
        self.sentence_label.pack(pady=20)

        self.output_label = tk.Label(root, text="", font=("Arial", 14), fg="blue")
        self.output_label.pack(pady=20)

        self.root.bind("<space>", self.handle_space)

    def start_condition(self, form_factor, accuracy):
    # Store selected condition
        self.current_condition = (form_factor, accuracy)
        self.current_index = 0

    # Hide all buttons by destroying them
        for widget in self.button_frame.winfo_children():
         widget.destroy()

    # Hide the title label
        self.label.pack_forget()

    # Show the sentence area
        self.sentence_label.pack(pady=20)
        self.output_label.pack(pady=20)

    # Start showing sentences
        self.show_sentence()

    def show_sentence(self):
        accuracy = self.current_condition[1]

        if self.current_index < len(sentences[accuracy]):  # If more sentences remain
            intended_meaning, asl_gloss, system_recognized = sentences[accuracy][self.current_index]
        
        # Show the next sentence
            self.sentence_label.config(text=f"You are signing for the intended meaning:\n\"{intended_meaning}\"\nASL Gloss: {asl_gloss}")
            self.output_label.config(text="Press SPACE to continue")
        else:
        # All sentences completed, show completion message
            self.sentence_label.config(text="Condition Complete. Select another condition.")
            self.output_label.config(text="")

        # Wait 2 seconds before showing condition buttons again
            self.root.after(2000, self.show_condition_buttons)

    def handle_space(self, event):
        accuracy = self.current_condition[1]

        if self.current_index < len(sentences[accuracy]):  # Ensure valid index
            intended_meaning, asl_gloss, system_recognized = sentences[accuracy][self.current_index]

            if not self.camera_on:
            # Start the camera on first space press
                self.start_camera()
            else:
            # Stop the camera and show system-recognized output
                self.stop_camera()
                self.output_label.config(text=f"System Recognized:\n{system_recognized}")
                self.current_index += 1

            # Show next sentence or finish condition
                self.show_sentence()

    def start_camera(self):
        self.cap = cv2.VideoCapture(0)
        self.camera_on = True
        self.update_camera()

    def stop_camera(self):
        if self.cap:
            self.cap.release()
            cv2.destroyAllWindows()
            self.camera_on = False

    def update_camera(self):
        ret, frame = self.cap.read()
        if ret:
            cv2.imshow('Sign Here', frame)
        if self.camera_on:
            self.root.after(10, self.update_camera)

    def show_condition_buttons(self):
    # Clear the sentence display
        self.sentence_label.config(text="")
        self.output_label.config(text="")

    # Show condition selection screen again
        self.label.config(text="Select a Condition")
        self.label.pack(pady=20)

    # Recreate the buttons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack()

        for form_factor in form_factors:
            for accuracy in accuracies:
                condition_name = f"{form_factor} - {accuracy}"
                btn = tk.Button(self.button_frame, text=condition_name, 
                            command=lambda f=form_factor, a=accuracy: self.start_condition(f, a))
                btn.pack(side=tk.LEFT, padx=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = ResearchInterviewApp(root)
    root.mainloop()
