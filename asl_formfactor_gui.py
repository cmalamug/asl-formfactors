import tkinter as tk
import pandas as pd
import cv2
import random

conditions_used = [3, 5, 9]
form_factors = ["glasses", "glasses + glove", "glasses + ring", "glasses + wristband"]

class ResearchInterviewApp: 
    def __init__(self, root):
        self.root = root
        self.root.title("Research Interview")
        self.root.geometry("1200x400")

        self.current_condition = None
        self.incomplete_conditions = [(c, f) for c in conditions_used for f in form_factors]
        self.num_same_factor = 0
        self.current_index = 0
        self.camera_on = False
        self.cap = None

        self.data = pd.read_csv("performance_survey_cleaned.csv")

        self.label = tk.Label(root, text="Select a Condition", font=("Arial", 24))
        self.label.pack(pady=20)

        self.button_frame = tk.Frame(root)
        self.button_frame.pack()

        # Create buttons for a random condition
        factor = random.choice(form_factors)
        i = random.choice(conditions_used)

        condition_name = f"condition {i} {factor}"
        btn = tk.Button(self.button_frame, text=condition_name, command=lambda c = i, f = factor: self.start_condition(c, f))
        btn.pack(side=tk.LEFT, padx=5)

        self.sentence_label = tk.Label(root, text="", font=("Arial", 24))
        self.sentence_label.pack(pady=20)

        self.output_label = tk.Label(root, text="", font=("Arial", 24), fg="blue")
        self.output_label.pack(pady=20)

        self.root.bind("<space>", self.handle_space)

    def start_condition(self, condition, factor):
        # Store selected condition
        self.current_condition = condition
        self.incomplete_conditions.remove((condition, factor))
        self.num_same_factor += 1
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
        sentences = self.find_sentences(condition)
        self.show_sentence(sentences)

    def find_sentences(self, condition):
        return self.data[self.data["condition"] == condition]

    def show_sentence(self, sentences):
        if self.current_index < len(sentences):  # If more sentences remain
            current_sentence = sentences.iloc[self.current_index]
            intended_meaning = current_sentence["intended_meaning"]
            asl_gloss = current_sentence["asl_gloss"]
            
            # Show the next sentence
            self.sentence_label.config(text=f"{intended_meaning}\n\n{asl_gloss}")
            self.output_label.config(text="Press SPACE to continue")
        else:
            # All sentences completed, show completion message
            self.sentence_label.config(text="Condition Complete. Select another condition.")
            self.output_label.config(text="")

            # Wait 2 seconds before showing condition buttons again
            self.root.after(2000, self.show_condition_buttons)

    def handle_space(self, event):
        condition = self.current_condition
        sentences = self.find_sentences(condition)
        if self.current_index < len(sentences):  # Ensure valid index
            current_sentence = sentences.iloc[self.current_index]
            intended_meaning = current_sentence["intended_meaning"]
            asl_gloss = current_sentence["asl_gloss"]
            system_recognized = current_sentence["error_asl_gloss"]

            if not hasattr(self, "state"):
                self.state = 0

            if self.state == 0:
                self.sentence_label.config(text=f"{intended_meaning}\n\n{asl_gloss}")
                self.output_label.config(text="Press SPACE when finished signing")
                self.state = 1

            elif self.state == 1:
                self.sentence_label.config(text=f"{intended_meaning}\n\n{asl_gloss}")
                self.output_label.config(text=f"{system_recognized}\n\nPress SPACE for the next sentence.")
                self.output_label.update_idletasks()
                self.state = 2

            elif self.state == 2:
                self.current_index += 1
                self.show_sentence(sentences)
                self.state = 0

    def show_condition_buttons(self):
        # Clear the sentence display
        self.sentence_label.config(text="")
        self.output_label.config(text="")

        self.label = tk.Label(root, text="Select a Condition", font=("Arial", 24))
        self.label.pack(pady=20)

        self.button_frame = tk.Frame(root)
        self.button_frame.pack()

        # Create button
        if len(self.incomplete_conditions) == 0:
            self.sentence_label.config(text="All Condition Complete.")
        else:
            i, factor = random.choice(incomplete_conditions)
            
            condition_name = f"condition {i} {factor}"

            btn = tk.Button(self.button_frame, text=condition_name, command=lambda c = i, f = factor: self.start_condition(c, f))
            btn.pack(side=tk.LEFT, padx=5)

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
                
if __name__ == "__main__":
    root = tk.Tk()
    app = ResearchInterviewApp(root)
    app.start_camera()
    root.mainloop()
    app.stop_camera()