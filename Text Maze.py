import random

# Define the maze dimensions
MAZE_SIZE = 5

# Define player and heart symbols
PLAYER = 'P'
HEART = '❤'
EMPTY = ' '

# Define obstacles
OBSTACLE = '#'

# Define directions
UP = 'W'
DOWN = 'S'
LEFT = 'A'
RIGHT = 'D'

def create_maze(size):
    maze = [[EMPTY for _ in range(size)] for _ in range(size)]
    maze[random.randint(0, size-1)][random.randint(0, size-1)] = HEART  # Place heart randomly
    for _ in range(size):
        maze[random.randint(0, size-1)][random.randint(0, size-1)] = OBSTACLE  # Place obstacles randomly
    return maze

def print_maze(maze, player_position):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if (i, j) == player_position:
                print(PLAYER, end=' ')
            else:
                print(maze[i][j], end=' ')
        print()

def move_player(player_position, direction):
    x, y = player_position
    if direction == UP:
        return max(0, x - 1), y
    elif direction == DOWN:
        return min(MAZE_SIZE - 1, x + 1), y
    elif direction == LEFT:
        return x, max(0, y - 1)
    elif direction == RIGHT:
        return x, min(MAZE_SIZE - 1, y + 1)

def main():
    print("Welcome to the Maze of Love!")
    maze = create_maze(MAZE_SIZE)
    player_position = (0, 0)

    while True:
        print_maze(maze, player_position)

        if maze[player_position[0]][player_position[1]] == HEART:
            print("Congratulations! You found my heart ❤️")
            print("Our love knows no bounds!")
            print("Will you be my boyfriend?")
            break

        direction = input("Enter direction (W/A/S/D to move, Q to quit): ").upper()

        if direction == 'Q':
            print("You gave up... Don't give up on love!")
            break

        if direction in (UP, DOWN, LEFT, RIGHT):
            new_position = move_player(player_position, direction)
            if maze[new_position[0]][new_position[1]] != OBSTACLE:
                player_position = new_position
            else:
                print("Ouch! You bumped into an obstacle. Be careful!")
        else:
            print("Invalid direction! Use W/A/S/D to move or Q to quit.")

if __name__ == "__main__":
    main()