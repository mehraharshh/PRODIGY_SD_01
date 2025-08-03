import tkinter as tk
from tkinter import messagebox
import random

class GuessNumberGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Guess the Number")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        self.difficulty = None
        self.number_to_guess = None
        self.attempts = 0

        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self.root, text="🎯 Guess the Number", font=("Helvetica", 16, "bold"))
        self.title_label.pack(pady=10)

        self.diff_label = tk.Label(self.root, text="Select Difficulty:")
        self.diff_label.pack()

        self.diff_frame = tk.Frame(self.root)
        self.diff_frame.pack()

        self.easy_btn = tk.Button(self.diff_frame, text="Easy (1–10)", command=lambda: self.start_game("easy"))
        self.easy_btn.grid(row=0, column=0, padx=5)

        self.medium_btn = tk.Button(self.diff_frame, text="Medium (1–50)", command=lambda: self.start_game("medium"))
        self.medium_btn.grid(row=0, column=1, padx=5)

        self.hard_btn = tk.Button(self.diff_frame, text="Hard (1–100)", command=lambda: self.start_game("hard"))
        self.hard_btn.grid(row=0, column=2, padx=5)

        self.instruction_label = tk.Label(self.root, text="", font=("Helvetica", 10))
        self.instruction_label.pack(pady=10)

        self.entry = tk.Entry(self.root, font=("Helvetica", 12), state="disabled")
        self.entry.pack(pady=5)

        self.guess_btn = tk.Button(self.root, text="Submit Guess", command=self.check_guess, state="disabled")
        self.guess_btn.pack()

        self.feedback_label = tk.Label(self.root, text="", font=("Helvetica", 12))
        self.feedback_label.pack(pady=10)

    def start_game(self, difficulty):
        ranges = {"easy": 10, "medium": 50, "hard": 100}
        self.difficulty = difficulty
        self.number_to_guess = random.randint(1, ranges[difficulty])
        self.attempts = 0

        self.instruction_label.config(
            text=f"Enter your guess (1 to {ranges[difficulty]}):"
        )
        self.entry.config(state="normal")
        self.guess_btn.config(state="normal")
        self.feedback_label.config(text="")
        self.entry.delete(0, tk.END)

    def check_guess(self):
        try:
            guess = int(self.entry.get())
            self.attempts += 1

            if guess < self.number_to_guess:
                self.feedback_label.config(text="Too low! Try again.")
            elif guess > self.number_to_guess:
                self.feedback_label.config(text="Too high! Try again.")
            else:
                messagebox.showinfo("🎉 Correct!", f"You guessed it in {self.attempts} attempts!")
                self.reset_game()
        except ValueError:
            self.feedback_label.config(text="Please enter a valid number.")

    def reset_game(self):
        self.entry.delete(0, tk.END)
        self.entry.config(state="disabled")
        self.guess_btn.config(state="disabled")
        self.instruction_label.config(text="Select Difficulty:")
        self.feedback_label.config(text="")

# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    app = GuessNumberGame(root)
    root.mainloop()
