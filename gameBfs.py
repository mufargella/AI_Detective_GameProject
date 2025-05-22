import random
from collections import deque

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


# Function to create a randomized grid
def create_grid():
    grid = [["Empty"] * 5 for _ in range(5)]
    positions = [(x, y) for x in range(5) for y in range(5)]  # feha kol el e7dasyat el momkna el hya mn (0,0) to (4,4)
    random.shuffle(positions)  # Randomize positions

    # Place police station
    grid[4][0] = "Police Station"
    positions.remove((4, 0))  # b7gz mkan ll PS
    #وبنشيل الإحداثية دي من لستة positions عشان ما نستخدمهاش لأي حاجة تانية.



    # Place clues and suspects
    for i in range(3):     # 3 clues and 3 suspects
        x, y = positions.pop()          ## kol wa7ed hyb2a leh mkan mn 8er ma etnen yt7ato fo2 b3d
        grid[x][y] = f"Clue {i + 1}"


    for name in suspects.keys():
        x, y = positions.pop()
        grid[x][y] = f"Suspect {name}"  # place suspect name in cell mn 8er ma etnen suspects yt7ato fo2 b3d

    return grid


# Function to display the grid
def display_grid(grid, position):
    for i, row in enumerate(grid):   ### loop 3la el row ma 3 rkm el row (i)
        for j, cell in enumerate(row):  ## loop 3la el col m3 rkm el col (j)
            if (i, j) == position:   #لو الخانة هي نفسها مكان الضابط (position)، بنطبع حرف "D".
                print("D", end=" ")  # Detective position
            elif cell == "Police Station":
                print("PS", end=" ")
            elif "Clue" in cell:
                print("C", end=" ")
            elif "Suspect" in cell:
                print("S", end=" ")
            else:
                print(".", end=" ") # empty cells
        print()


# BFS pathfinding algorithm to find shortest path
def bfs(grid, start, target):
    queue = deque([(start, [])])  # Queue with (current_position, path_so_far)
    visited = set()

    while queue:
        current, path = queue.popleft()  #  make sure that  if i visited continue  else visited.add(current)
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
            if clue == "Thief wears glasses" and not traits.get("Glasses"):
                is_possible = False
            if clue == "Thief has no alibi" and traits.get("Alibi"):
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
    dynamic_target = None  # Next target position

    print("Welcome to the AI Detective Game!")
    print("Move your detective around the grid to collect clues and question suspects.")
    print("Solve the case by gathering clues and accusing the correct suspect!")

    while True:
        # Show the grid and current position
        display_grid(grid, position)

        # Step 1: Decide where to go (clues, suspects, or police station)
        if len(collected_clues) < 3:
            # Still collecting clues
            for clue_index in range(1, 4):
                target = f"Clue {clue_index}"
                dynamic_target = find_position(grid, target)
                if dynamic_target is not None:
                    print(f"Targeting {target} at {dynamic_target}")
                    break
        elif dynamic_target is None:
            # Collect suspects or prepare to accuse
            for suspect_name in suspects.keys():
                dynamic_target = find_position(grid, f"Suspect {suspect_name}")
                if dynamic_target is not None:
                    print(f"Targeting Suspect {suspect_name} at {dynamic_target}")
                    break

        # Step 2: Calculate path to the dynamic target
        path_to_target = bfs(grid, position, dynamic_target)
        if path_to_target is None:
            print("No path to the target found!")
            break

        next_step = path_to_target[0]  # Get the next step on the path
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
            dynamic_target = None  # Reset target to search for the next one

        elif "Suspect" in cell:
            name = cell.split()[-1]
            print(f"You found {name}. Traits: {suspects[name]}")

            # Eliminate suspects based on collected clues
            suspects_left = eliminate_suspects(collected_clues)
            print("Suspects remaining after analysis:", suspects_left)

            if len(suspects_left) == 1:
                print(f"The culprit must be {suspects_left[0]}! Returning to the Police Station to accuse.")
                dynamic_target = (4, 0)  # Go back to Police Station
            else:
                dynamic_target = None  # Keep analyzing other cells

        elif "Police Station" in cell:
            if len(collected_clues) >= 3:
                print("You have enough clues. Determining the culprit now!")
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
