import tkinter as tk
from tkinter import messagebox
from collections import deque
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
        self.targets = []  # Initialize targets before calling create_grid
        self.grid = self.create_grid()
        self.position = (4, 0)  # Initial position at Police Station
        self.collected_clues = []
        self.correct_culprit = random.choice(list(suspects.keys()))  # Randomly choose the culprit

        self.buttons = {}
        self.remaining_suspects = list(suspects.keys())  # Start with all suspects
        self.init_gui()

        self.auto_move()  # Start the automatic movement

    def create_grid(self):
        """ Create a randomized 5x5 game grid. """
        grid = [["Empty"] * 5 for _ in range(5)]
        positions = [(x, y) for x in range(5) for y in range(5)]
        random.shuffle(positions)

        # Place the police station
        grid[4][0] = "Police Station"
        positions.remove((4, 0))

        # Place clues and suspects
        for i in range(3):
            x, y = positions.pop()
            grid[x][y] = f"Clue {i + 1}"
            self.targets.append((x, y))  # Add to target list
        for name in suspects.keys():
            x, y = positions.pop()
            grid[x][y] = f"Suspect {name}"
            self.targets.append((x, y))  # Add to target list

        return grid

    def init_gui(self):
        """ Initialize the GUI. """
        self.master.title("AI Detective Game")
        self.master.geometry("600x650")

        self.info_label = tk.Label(self.master, text="Welcome to the AI Detective Game!", font=("Arial", 14),
                                   wraplength=500)
        self.info_label.pack(pady=10)

        # Create the playable grid
        self.grid_frame = tk.Frame(self.master)
        self.grid_frame.pack(pady=10)
        for i in range(5):
            for j in range(5):
                btn = tk.Button(self.grid_frame, text=".", width=8, height=4, font=("Arial", 12))
                btn.grid(row=i, column=j)
                self.buttons[(i, j)] = btn

        self.update_grid()

    def update_grid(self):
        """ Update the grid and visuals based on game state. """
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

    def bfs(self, target):
        """ BFS pathfinding algorithm to find the shortest path to a target. """
        queue = deque([(self.position, [])])  # (current_position, path_so_far)
        visited = set()

        while queue:
            current, path = queue.popleft()
            if current in visited:
                continue
            visited.add(current)

            if current == target:
                return path  # Return the full path to the target

            # Generate neighbors
            x, y = current
            neighbors = [
                (x - 1, y),  # Up
                (x + 1, y),  # Down
                (x, y - 1),  # Left
                (x, y + 1)  # Right
            ]
            for nx, ny in neighbors:
                if 0 <= nx < 5 and 0 <= ny < 5 and (nx, ny) not in visited:
                    queue.append(((nx, ny), path + [(nx, ny)]))

        return []  # Return empty list if no path is found

    def handle_cell(self):
        """ Handle interactions when reaching a specific cell. """
        x, y = self.position
        cell = self.grid[x][y]

        if "Clue" in cell:
            clue_index = int(cell.split()[-1]) - 1
            if clues[clue_index] not in self.collected_clues:
                self.collected_clues.append(clues[clue_index])
                self.info_label.config(text=f"Found clue: {clues[clue_index]}")
                self.grid[x][y] = "Empty"  # Mark clue as collected
        elif "Suspect" in cell:
            suspect_name = cell.split()[-1]
            self.info_label.config(text=f"Interrogating {suspect_name}.")
            self.remaining_suspects = self.filter_suspects()
        elif cell == "Police Station":
            if len(self.remaining_suspects) == 1:
                self.info_label.config(text=f"The culprit is {self.remaining_suspects[0]}!")
                messagebox.showinfo("Case Solved!", f"The culprit was {self.remaining_suspects[0]}. Well done!")
                self.master.quit()

    def filter_suspects(self):
        """ Filter suspects based on collected clues. """
        remaining = []
        for name, traits in suspects.items():
            is_possible = True
            for clue in self.collected_clues:
                if clue == "Thief wears glasses" and not traits.get("Glasses"):
                    is_possible = False
                if clue == "Thief has no alibi" and traits.get("Alibi"):
                    is_possible = False
            if is_possible:
                remaining.append(name)
        return remaining

    def auto_move(self):
        """ Automatically move the detective to the next target (clue or suspect). """
        if self.targets:
            # Find path to the next target
            target = self.targets[0]
            path = self.bfs(target)
            if path:
                # Move step-by-step along the path
                next_step = path.pop(0)
                self.position = next_step
                self.update_grid()
                self.master.after(500, self.auto_move)  # Delay for smooth movement
            else:
                # If we reach the target, handle the cell and remove it from targets
                self.handle_cell()
                self.targets.remove(target)
                self.auto_move()  # Move to the next target
        else:
            # No more targets, automatically accuse!
            self.info_label.config(text="Returning to Police Station to accuse!")
            path = self.bfs((4, 0))
            if path:
                next_step = path.pop(0)
                self.position = next_step
                self.update_grid()
                self.master.after(500, self.auto_move)
            else:
                self.handle_cell()


# Start the game
if __name__ == "__main__":
    root = tk.Tk()
    DetectiveGame(root)
    root.mainloop()
