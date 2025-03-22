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
        self.root.geometry("1200x600")

        self.current_condition = None
        self.current_factor = None
        self.incomplete_conditions = [(c, f) for c in conditions_used for f in form_factors]
        self.num_same_factor = 0
        self.current_index = 0
        self.camera_on = False
        self.cap = None

        self.data = pd.read_csv("performance_survey_cleaned.csv")

        self.label = tk.Label(root, text="Select a Condition", font=("Arial", 24))
        self.label.pack(pady=10)

        self.condition_label = tk.Label(root, text="", font=("Arial", 18), fg="gray")
        self.condition_label.pack()

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)

        factor = random.choice(form_factors)
        i = random.choice(conditions_used)
        condition_name = f"condition {i} {factor}"
        btn = tk.Button(self.button_frame, text=condition_name, command=lambda c=i, f=factor: self.start_condition(c, f))
        btn.pack(side=tk.LEFT, padx=5)

        self.sentence_label = tk.Label(root, text="", font=("Arial", 24))
        self.sentence_label.pack(pady=20)

        self.system_output_text = tk.Text(root, height=2, font=("Arial", 24), bd=0, bg="black", fg="white")
        self.system_output_text.pack(pady=10)
        self.system_output_text.config(state=tk.DISABLED)

        self.instruction_label = tk.Label(root, text="", font=("Arial", 20), fg="blue", justify="center")
        self.instruction_label.pack(pady=5, anchor="center")

        self.root.bind("<space>", self.handle_space)

    def start_condition(self, condition, factor):
        self.current_condition = condition
        self.current_factor = factor
        self.incomplete_conditions.remove((condition, factor))
        self.num_same_factor += 1
        self.current_index = 0

        self.condition_label.config(text=f"Current Condition: {condition} | Form Factor: {factor}")

        for widget in self.button_frame.winfo_children():
            widget.destroy()

        self.label.pack_forget()
        self.sentence_label.pack(pady=20)
        self.system_output_text.pack(pady=10)
        self.instruction_label.pack(pady=5)

        sentences = self.find_sentences(condition)
        self.show_sentence(sentences)

    def find_sentences(self, condition):
        return self.data[self.data["condition"] == condition]

    def show_sentence(self, sentences):
        if self.current_index < len(sentences):
            current_sentence = sentences.iloc[self.current_index]
            intended_meaning = current_sentence["intended_meaning"]
            asl_gloss = current_sentence["asl_gloss"]

            self.sentence_label.config(text=f"{intended_meaning}\n\n{asl_gloss}")

            self.system_output_text.config(state=tk.NORMAL)
            self.system_output_text.delete("1.0", tk.END)
            self.system_output_text.config(state=tk.DISABLED)

            self.instruction_label.config(text="Press SPACE to continue")
        else:
            self.sentence_label.config(text="Condition Complete. Select another condition.")
            self.system_output_text.config(state=tk.NORMAL)
            self.system_output_text.delete("1.0", tk.END)
            self.system_output_text.config(state=tk.DISABLED)
            self.instruction_label.config(text="")
            self.condition_label.config(text="")
            self.root.after(2000, self.show_condition_buttons)

    def handle_space(self, event):
        condition = self.current_condition
        sentences = self.find_sentences(condition)
        if self.current_index < len(sentences):
            current_sentence = sentences.iloc[self.current_index]
            intended_meaning = current_sentence["intended_meaning"]
            asl_gloss = current_sentence["asl_gloss"]
            system_recognized = current_sentence["error_asl_gloss"]

            if not hasattr(self, "state"):
                self.state = 0

            if self.state == 0:
                self.sentence_label.config(text=f"{intended_meaning}\n\n{asl_gloss}")
                self.instruction_label.config(text="Press SPACE when finished signing")
                self.system_output_text.config(state=tk.NORMAL)
                self.system_output_text.delete("1.0", tk.END)
                self.system_output_text.config(state=tk.DISABLED)
                self.state = 1

            elif self.state == 1:
                self.sentence_label.config(text=f"{intended_meaning}\n\n{asl_gloss}")

                gloss_words = asl_gloss.strip().upper().split()
                recognized_words = system_recognized.strip().upper().split()

                self.system_output_text.config(state=tk.NORMAL)
                self.system_output_text.delete("1.0", tk.END)

                if gloss_words == recognized_words:
                    # Entire sentence correct
                    self.system_output_text.insert(tk.END, system_recognized, "correct")
                else:
                    # Word-by-word comparison
                    for i, word in enumerate(recognized_words):
                        if i < len(gloss_words) and word == gloss_words[i]:
                            self.system_output_text.insert(tk.END, word + " ")
                        else:
                            self.system_output_text.insert(tk.END, word + " ", "wrong")

                self.system_output_text.tag_config("wrong", foreground="red")
                self.system_output_text.tag_config("correct", foreground="green")
                self.system_output_text.config(state=tk.DISABLED)

                self.instruction_label.config(text="Press SPACE for the next sentence.")
                self.state = 2

            elif self.state == 2:
                self.current_index += 1
                self.show_sentence(sentences)
                self.state = 0

    def show_condition_buttons(self):
        self.sentence_label.config(text="")
        self.instruction_label.config(text="")
        self.condition_label.config(text="")

        self.system_output_text.config(state=tk.NORMAL)
        self.system_output_text.delete("1.0", tk.END)
        self.system_output_text.config(state=tk.DISABLED)

        self.label = tk.Label(root, text="Select a Condition", font=("Arial", 24))
        self.label.pack(pady=10)

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)

        if len(self.incomplete_conditions) == 0:
            self.sentence_label.config(text="All Conditions Complete.")
        else:
            i, factor = random.choice(self.incomplete_conditions)
            condition_name = f"condition {i} {factor}"
            btn = tk.Button(self.button_frame, text=condition_name, command=lambda c=i, f=factor: self.start_condition(c, f))
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
