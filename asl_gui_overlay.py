import tkinter as tk
import pandas as pd
import cv2
import random
import sys

conditions_used = [5, 9]
form_factors = ["glasses", "glasses + glove", "glasses + ring", "glasses + wristband"]

class ResearchInterviewApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Research Interview")
        self.root.geometry("400x200")

        self.current_condition = None
        self.current_factor = None
        self.incomplete_conditions = [(c, f) for c in conditions_used for f in form_factors]
        self.num_same_factor = 0
        self.current_index = 0
        self.camera_on = False
        self.cap = None

        self.data = pd.read_csv("performance_survey_cleaned.csv")

        self.label = tk.Label(root, text="Select a Condition", font=("Arial", 16))
        self.label.pack(pady=10)

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)

        self.show_condition_buttons()
        self.root.bind("<space>", self.handle_space)

    def start_condition(self, condition, factor):
        self.current_condition = condition
        self.current_factor = factor
        if (condition, factor) in self.incomplete_conditions:
            self.incomplete_conditions.remove((condition, factor))
        self.num_same_factor += 1
        self.current_index = 0
        self.state = 0

        self.label.pack_forget()
        for widget in self.button_frame.winfo_children():
            widget.destroy()

    def find_sentences(self, condition):
        return self.data[self.data["condition"] == condition]

    def handle_space(self, event):
        if self.current_condition is None:
            return
        sentences = self.find_sentences(self.current_condition)
        if self.current_index >= len(sentences):
            return

        if self.state == 0:
            self.state = 1
        elif self.state == 1:
            self.state = 2
        elif self.state == 2:
            self.current_index += 1
            self.state = 0

        if self.current_index >= len(sentences):
            self.show_condition_buttons()
            self.current_condition = None

    def show_condition_buttons(self):
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        self.label = tk.Label(root, text="Select a Condition", font=("Arial", 16))

        if len(self.incomplete_conditions) == 0:
            finish_label = tk.Label(root, text="All Conditions Complete.", font=("Arial", 14))
            finish_label.pack()
            sys.exit()
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

    def draw_centered_text(self, frame, text, y, color, font_scale=1.0, thickness=2, max_width=None):
        font = cv2.FONT_HERSHEY_DUPLEX
        if max_width is None:
            max_width = frame.shape[1] - 40  # Add 20px padding on each side

        # Try reducing scale if text is too wide
        while True:
            text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
            if text_size[0] <= max_width or font_scale < 0.5:
                break
            font_scale -= 0.05

        x = (frame.shape[1] - text_size[0]) // 2
        cv2.putText(frame, text, (x, y), font, font_scale, color, thickness, lineType=cv2.LINE_AA)


    def draw_centered_comparison(self, frame, ref_text, pred_text, y):
        ref_words = ref_text.strip().upper().split()
        pred_words = pred_text.strip().upper().split()

        font = cv2.FONT_HERSHEY_DUPLEX
        font_scale = 1.0
        thickness = 2
        space = 15

        # Calculate total width
        word_sizes = []
        total_width = 0
        for i, word in enumerate(pred_words):
            size = cv2.getTextSize(word, font, font_scale, thickness)[0]
            word_sizes.append(size)
            total_width += size[0] + space
        total_width -= space  # no space after last word

        x = (frame.shape[1] - total_width) // 2

        for i, word in enumerate(pred_words):
            size = word_sizes[i]
            color = (0, 255, 0) if i < len(ref_words) and word == ref_words[i] else (0, 0, 255)
            cv2.putText(frame, word, (x, y), font, font_scale, color, thickness, lineType=cv2.LINE_AA)
            x += size[0] + space

        return y + size[1] + 30  # advance y

    def update_camera(self):
        ret, frame = self.cap.read()
        if ret:
            y = 40

            if self.current_condition is not None:
                sentences = self.find_sentences(self.current_condition)
                total_sentences = len(sentences)
                if self.current_index < total_sentences:
                    current_sentence = sentences.iloc[self.current_index]
                    intended_meaning = current_sentence["intended_meaning"]
                    asl_gloss = current_sentence["asl_gloss"]
                    system_recognized = current_sentence["error_asl_gloss"]

                    # Top info bar
                    top_info = f"Condition {self.current_condition} | {self.current_factor} | Sentence {self.current_index + 1} of {total_sentences}"
                    self.draw_centered_text(frame, top_info, y, (255, 255, 255), 1.2)
                    y += 50

                    self.draw_centered_text(frame, f"{intended_meaning}", y, (255, 255, 255), 1.2)
                    y += 50
                    self.draw_centered_text(frame, f"{asl_gloss}", y, (0, 255, 0), 1.2)
                    y += 50

                    if self.state >= 1:
                        y = self.draw_centered_comparison(frame, asl_gloss, system_recognized, y)

                    instruction = ""
                    if self.state == 0:
                        instruction = "Press SPACE when ready to sign"
                    elif self.state == 1:
                        instruction = "Press SPACE to show recognition"
                    elif self.state == 2:
                        instruction = "Press SPACE for next sentence"

                    self.draw_centered_text(frame, instruction, y, (255, 255, 0), 1.0)

            cv2.imshow('Sign Here', frame)

        if self.camera_on:
            self.root.after(10, self.update_camera)

if __name__ == "__main__":
    root = tk.Tk()
    app = ResearchInterviewApp(root)
    app.start_camera()
    root.mainloop()
    app.stop_camera()
