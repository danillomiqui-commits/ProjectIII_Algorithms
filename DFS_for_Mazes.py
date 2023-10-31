import pygame
import random
import time

# Maze parameters
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 20

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Generation and DFS")

# Define maze dimensions
maze_width = WIDTH // GRID_SIZE
maze_height = HEIGHT // GRID_SIZE

# Create a grid to represent the maze
maze = [[0] * maze_width for _ in range(maze_height)]


def draw_maze():
    for y in range(maze_height):
        for x in range(maze_width):
            if maze[y][x] == 1:
                pygame.draw.rect(
                    screen, BLACK, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                )


def generate_maze():
    for y in range(maze_height):
        for x in range(maze_width):
            if x % 2 == 0 or y % 2 == 0:
                maze[y][x] = 1

    stack = [(0, 0)]
    while stack:
        current = stack[-1]
        x, y = current
        maze[y][x] = 0
        neighbors = [(x + 2, y), (x - 2, y), (x, y + 2), (x, y - 2)]
        unvisited_neighbors = [
            n
            for n in neighbors
            if 0 <= n[0] < maze_width
            and 0 <= n[1] < maze_height
            and maze[n[1]][n[0]] == 1
        ]
        if unvisited_neighbors:
            next_cell = random.choice(unvisited_neighbors)
            nx, ny = next_cell
            maze[(ny + y) // 2][(nx + x) // 2] = 0
            stack.append(next_cell)
        else:
            stack.pop()


def dfs(maze, start, end):
    stack = [start]
    visited = set()
    came_from = {}
    exit_found = False

    while stack:
        x, y = stack.pop()
        if (x, y) == end:
            path = []
            while (x, y) in came_from:
                path.append((x, y))
                x, y = came_from[(x, y)]
            exit_found = True
            break

        visited.add((x, y))
        neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        random.shuffle(neighbors)

        for nx, ny in neighbors:
            if (
                0 <= nx < maze_width
                and 0 <= ny < maze_height
                and maze[ny][nx] == 0
                and (nx, ny) not in visited
            ):
                stack.append((nx, ny))
                came_from[(nx, ny)] = (x, y)

    return exit_found, path


def main():
    generate_maze()
    start = (1, 1)
    end = (maze_width - 2, maze_height - 2)

    start_time = time.time()
    exit_found, path = dfs(maze, start, end)
    end_time = time.time()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.fill(WHITE)
        draw_maze()

        if path:
            for x, y in path:
                pygame.draw.rect(
                    screen, GREEN, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                )

        if exit_found:
            print("Exit found!")
            print(f"Time to find the exit: {end_time - start_time:.5f} seconds")
            exit_found = False

        pygame.display.update()


if __name__ == "__main__":
    main()
