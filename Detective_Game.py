import random
from collections import deque

# Define suspects with traits hidden initially
suspects = {
    "Alice": {"Glasses": "Unknown", "Alibi": "Unknown"},
    "Bob": {"Glasses": "Unknown", "Alibi": "Unknown"},
    "Charlie": {"Glasses": "Unknown", "Alibi": "Unknown"}
}

# Clues that the detective needs to collect
clues = [
    "Thief wears glasses",
    "Thief was here at 8PM",
    "Thief has no alibi"
]


# Function to create a randomized grid
def create_grid():
    grid = [["Empty"] * 5 for _ in range(5)]
    positions = [(x, y) for x in range(5) for y in range(5)]   # to define grid
    random.shuffle(positions)     ## change suspects and clues every time

    # Place police station
    grid[4][0] = "Police Station"
    positions.remove((4, 0))  # m7dsh ya5od mkano

    # Place clues and suspects
    for i in range(3):  # Place 3 clues
        x, y = positions.pop()   # ytl3ha 3shan  mhyt7sh haga tani
        grid[x][y] = f"Clue {i + 1}"

    for name in suspects.keys():  # Place suspects
        x, y = positions.pop()
        grid[x][y] = f"Suspect {name}"

    return grid


# Function to display the grid
def display_grid(grid, position):
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if (i, j) == position:
                print("D", end=" ")  # Detective position
            elif cell == "Police Station":
                print("PS", end=" ")
            elif "Clue" in cell:
                print("C", end=" ")
            elif "Suspect" in cell:
                print("S", end=" ")
            else:
                print(".", end=" ")
        print()


# BFS pathfinding algorithm to find shortest path
def bfs(grid, start, target):
    queue = deque([(start, [])])  # Queue with (current_position, path_so_far)
    visited = set()

    while queue:
        current, path = queue.popleft()
        if current in visited:
            continue
        visited.add(current)

        if current == target:
            return path  # Return the path to the target

        # Explore neighbors
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

    return None  # Return None if no path is found


# Function to find the position of an object (e.g., clue or suspect) in the grid
def find_position(grid, target):
    for i in range(5):
        for j in range(5):
            if target in grid[i][j]:
                return (i, j)
    return None


# Function to eliminate suspects based on clues
def eliminate_suspects(collected_clues):
    remaining_suspects = []
    for name, traits in suspects.items():
        is_possible = True
        for clue in collected_clues:
            if clue == "Thief wears glasses":
                if traits.get("Glasses") == "Unknown":  # Don't eliminate if still unknown
                    continue
                if not traits.get("Glasses"):
                    is_possible = False
            if clue == "Thief has no alibi":
                if traits.get("Alibi") == "Unknown":  # Don't eliminate if still unknown
                    continue
                if traits.get("Alibi"):
                    is_possible = False
        if is_possible:
            remaining_suspects.append(name)
    return remaining_suspects


# Main game loop
def play_game():
    # Create the game grid and initialize the starting position
    grid = create_grid()
    position = (4, 0)  # Start at the Police Station
    collected_clues = []
    suspects_visited = set()
    dynamic_target = None  # Next target position

    print("Welcome to the AI Detective Game!")
    print("Move your detective around the grid to collect clues and question suspects.")
    print("Solve the case by gathering clues and interacting with suspects!")

    while True:
        # Show the grid and current position
        display_grid(grid, position)

        # Step 1: Decide where to go (clues or suspects)
        if len(collected_clues) < 3:
            # Target clues first
            for clue_index in range(1, 4):
                target = f"Clue {clue_index}"
                dynamic_target = find_position(grid, target)
                if dynamic_target is not None:
                    print(f"Targeting {target} at {dynamic_target}")
                    break
        elif len(suspects_visited) < 3:
            # Then target unvisited suspects
            for suspect_name in suspects.keys():
                if suspect_name not in suspects_visited:
                    dynamic_target = find_position(grid, f"Suspect {suspect_name}")
                    if dynamic_target is not None:
                        print(f"Targeting Suspect {suspect_name} at {dynamic_target}")
                        break
        else:
            # Decide to accuse the thief
            dynamic_target = (4, 0)  # Police Station

        # Step 2: Calculate path to the dynamic target
        path_to_target = bfs(grid, position, dynamic_target)
        if path_to_target is None:
            print("No path to the target found!")
            break

        next_step = path_to_target[0]
        print(f"Moving from {position} to {next_step}")
        position = next_step  # Move to the next step

        # Step 3: Interact with the cell when reaching the target
        cell = grid[position[0]][position[1]]
        if "Clue" in cell:
            clue_index = int(cell.split()[-1]) - 1
            if clues[clue_index] not in collected_clues:
                collected_clues.append(clues[clue_index])
                print(f"You found a clue: {clues[clue_index]}!")
                grid[position[0]][position[1]] = "Empty"  # Mark as visited
            else:
                print("You already collected this clue.")
            dynamic_target = None  # Reset target

        elif "Suspect" in cell:
            name = cell.split()[-1]
            suspects_visited.add(name)  # Mark suspect as visited
            if suspects[name]["Glasses"] == "Unknown":
                suspects[name]["Glasses"] = True if name in ["Alice", "Charlie"] else False
            if suspects[name]["Alibi"] == "Unknown":
                suspects[name]["Alibi"] = False if name in ["Bob", "Charlie"] else True
            print(f"You questioned {name}. Traits revealed: {suspects[name]}")

            # Eliminate suspects based on collected clues
            suspects_left = eliminate_suspects(collected_clues)
            print("Suspects remaining after analysis:", suspects_left)

            dynamic_target = None  # Reset target

        elif "Police Station" in cell:
            if len(collected_clues) >= 3 and len(suspects_visited) >= 3:
                print("You have enough clues and have questioned all suspects. Solving the case now!")
                suspects_left = eliminate_suspects(collected_clues)

                if len(suspects_left) == 1:
                    print(f"The only possible culprit is {suspects_left[0]}!")
                    print(f"The culprit is {suspects_left[0]}. Congratulations! Case closed!")
                else:
                    print("Unable to determine a specific culprit. Keep investigating!")

                break  # End the game


# Run the game
if __name__ == "__main__":
    play_game()
