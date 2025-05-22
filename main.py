import random

# Define suspects, traits, clues
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
    positions = [(x, y) for x in range(5) for y in range(5)]
    random.shuffle(positions)  # make randomise of positions

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


# Function to move the detective
def move(position, direction):
    x, y = position
    if direction == "UP" and x > 0:
        return (x - 1, y)
    if direction == "DOWN" and x < 4:
        return (x + 1, y)
    if direction == "LEFT" and y > 0:
        return (x, y - 1)
    if direction == "RIGHT" and y < 4:
        return (x, y + 1)
    return position



# Main game loop
def play_game():
    # Create the game grid and initialize the starting position
    grid = create_grid()
    position = (4, 0)  # Start at the Police Station
    collected_clues = []

    print("Welcome to the AI Detective Game!")
    print("Move your detective around the grid to collect clues and question suspects.")
    print("Once you collect enough clues, try to identify the guilty suspect!")

    while True:
        # Show the grid and current position
        display_grid(grid, position)
        print("Move (UP, DOWN, LEFT, RIGHT): ", end="")
        direction = input().strip().upper()

        # Handle invalid input
        if direction not in ["UP", "DOWN", "LEFT", "RIGHT"]:
            print("Invalid input! Please enter UP, DOWN, LEFT, or RIGHT.")
            continue

        # Move the detective
        position = move(position, direction)
        cell = grid[position[0]][position[1]]

        # Interact with the cell
        if "Clue" in cell:
            clue_index = int(cell.split()[-1]) - 1
            if clues[clue_index] not in collected_clues:
                collected_clues.append(clues[clue_index])
                print(f"You found a clue: {clues[clue_index]}!")
            else:
                print("You already collected this clue.")
            grid[position[0]][position[1]] = "Empty"  # Mark as visited
        elif "Suspect" in cell:
            name = cell.split()[-1]
            print(f"You found {name}. Traits: {suspects[name]}")
        elif cell == "Empty":
            print("This room is empty.")
        elif cell == "Police Station":
            print("You are back at the Police Station.")
            if len(collected_clues) >= 3:
                print("You have enough clues. Accuse a suspect!")
                print("Suspects: Alice, Bob, Charlie")
                print("Who is the culprit? ", end="")
                accusation = input().strip()

                # Check if the accusation is correct
                if accusation == "Charlie":  # Replace this for dynamic guilty logic
                    print("Correct! You solved the case!")
                    break
                else:
                    print("Wrong accusation. Keep investigating!")


# Run the game
if __name__ == "__main__":

    play_game()
