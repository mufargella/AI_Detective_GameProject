import tkinter as tk
from tkinter import messagebox
import random

# Define suspects, traits, and clues
suspects = {
    "Alice": {"Glasses": True, "Alibi": True},
    "Bob": {"Red Hat": True, "Alibi": False},
    "Charlie": {"Glasses": True, "Alibi": False}
}

clues = [
    "Thief wears glasses",
    "Thief was here at 8PM",
    "Thief has no alibi"
]


class DetectiveGame:
    def __init__(self, master):
        self.master = master
        self.grid = self.create_grid()
        self.position = (4, 0)  # Start position (Police Station)
        self.collected_clues = []
        self.correct_culprit = "Charlie"  # Set culprit to Charlie
        self.init_gui()

    def create_grid(self):
        # Create a randomized 5x5 grid
        grid = [["Empty"] * 5 for _ in range(5)]
        positions = [(x, y) for x in range(5) for y in range(5)]
        random.shuffle(positions)

        # Place police station
        grid[4][0] = "Police Station"
        positions.remove((4, 0))

        # Place clues and suspects
        for i in range(3):
            x, y = positions.pop()
            grid[x][y] = f"Clue {i + 1}"
        for name in suspects.keys():
            x, y = positions.pop()
            grid[x][y] = f"Suspect {name}"

        return grid

    def init_gui(self):
        # Create a GUI with Tkinter
        self.master.title("AI Detective Game")
        self.master.geometry("600x600")
        self.buttons = {}
        self.info_area = tk.Label(self.master, text="Welcome to the AI Detective Game!", font=("Arial", 14),
                                  wraplength=500)
        self.info_area.pack(pady=10)

        # Create a grid layout
        self.grid_frame = tk.Frame(self.master)
        self.grid_frame.pack(pady=10)
        for i in range(5):
            for j in range(5):
                btn = tk.Button(self.grid_frame, text=".", width=6, height=3, font=("Arial", 12))
                btn.grid(row=i, column=j)
                self.buttons[(i, j)] = btn
        self.update_grid()

        # Create movement buttons
        self.controls_frame = tk.Frame(self.master)
        self.controls_frame.pack(pady=10)
        tk.Button(self.controls_frame, text="UP", command=lambda: self.move("UP"), width=10).grid(row=0, column=1)
        tk.Button(self.controls_frame, text="LEFT", command=lambda: self.move("LEFT"), width=10).grid(row=1, column=0)
        tk.Button(self.controls_frame, text="RIGHT", command=lambda: self.move("RIGHT"), width=10).grid(row=1, column=2)
        tk.Button(self.controls_frame, text="DOWN", command=lambda: self.move("DOWN"), width=10).grid(row=2, column=1)

    def update_grid(self):
        # Update the grid display
        for i in range(5):
            for j in range(5):
                btn = self.buttons[(i, j)]
                if (i, j) == self.position:
                    btn.config(text="D", bg="yellow")  # Detective position
                elif self.grid[i][j] == "Police Station":
                    btn.config(text="PS", bg="lightblue")
                elif "Clue" in self.grid[i][j]:
                    btn.config(text="C", bg="lightgreen")
                elif "Suspect" in self.grid[i][j]:
                    btn.config(text="S", bg="lightcoral")
                else:
                    btn.config(text=".", bg="white")

    def move(self, direction):
        x, y = self.position
        if direction == "UP" and x > 0:
            self.position = (x - 1, y)
        elif direction == "DOWN" and x < 4:
            self.position = (x + 1, y)
        elif direction == "LEFT" and y > 0:
            self.position = (x, y - 1)
        elif direction == "RIGHT" and y < 4:
            self.position = (x, y + 1)

        self.interact_with_cell()
        self.update_grid()

    def interact_with_cell(self):
        x, y = self.position
        cell = self.grid[x][y]

        if "Clue" in cell:
            clue_index = int(cell.split()[-1]) - 1
            if clues[clue_index] not in self.collected_clues:
                self.collected_clues.append(clues[clue_index])
                self.info_area.config(text=f"You found a clue: {clues[clue_index]}!")
                self.grid[x][y] = "Empty"  # Mark as visited
            else:
                self.info_area.config(text="You already collected this clue.")
        elif "Suspect" in cell:
            name = cell.split()[-1]
            self.info_area.config(text=f"You found {name}. Traits: {suspects[name]}")
        elif cell == "Police Station":
            if len(self.collected_clues) >= 3:
                self.info_area.config(text="You have enough clues. Make an accusation!")
                self.make_accusation()
            else:
                self.info_area.config(text="You are back at the Police Station. Keep investigating!")
        elif cell == "Empty":
            self.info_area.config(text="This room is empty.")

    def make_accusation(self):
        def accuse():
            guess = culprit_guess.get()
            if guess == self.correct_culprit:
                messagebox.showinfo("Victory!",
                                    f"Correct! The culprit was {self.correct_culprit}. You solved the case!")
                self.master.quit()
            else:
                messagebox.showerror("Wrong!", f"Wrong accusation! The culprit is still out there. Keep investigating!")

        # Create a new window for accusation
        accusation_window = tk.Toplevel(self.master)
        accusation_window.title("Make an Accusation")
        accusation_window.geometry("400x200")

        tk.Label(accusation_window, text="Who do you think is the culprit?", font=("Arial", 12)).pack(pady=10)
        culprit_guess = tk.StringVar()
        tk.Entry(accusation_window, textvariable=culprit_guess, font=("Arial", 12)).pack(pady=5)
        tk.Button(accusation_window, text="Accuse", command=accuse, font=("Arial", 12)).pack(pady=10)


# Start the game
if __name__ == "__main__":
    root = tk.Tk()
    game = DetectiveGame(root)
    root.mainloop()
