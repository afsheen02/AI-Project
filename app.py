import pygame
import random

# Define colors using RGB values
WHITE = (255, 255, 255)
GREY = (220, 220, 220)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)  # Added for visual highlights

# Define the time interval for updating the screen (in milliseconds)
UPDATE_TIME_MS = 10

# Initialize Pygame
pygame.init()

# Set up the window size and title
window_size = (500, 500)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Maze Solver")

# Define the size of the maze and size of each cell
maze_size = 20
cell_size = window_size[0] // maze_size


class Cell:
    """Represent a single cell in the maze."""
    def __init__(self) -> None:
        self.neighbor = []
        self.generated = False
        self.visited = False

    def set_neighbor(self, neighbor: str) -> None:
        self.neighbor.append(neighbor)

    def set_generated(self) -> None:
        self.generated = True

    def set_visited(self) -> None:
        self.visited = True

    def get_neighbor(self) -> list:
        return self.neighbor

    def get_generated(self) -> bool:
        return self.generated

    def get_visited(self) -> bool:
        return self.visited


class Maze:
    """Represent a maze grid and provides methods to generate and solve the maze."""
    def __init__(self, maze_size, cell_size) -> None:
        self.maze_size = maze_size
        self.cell_size = cell_size
        self.maze = [Cell() for _ in range(self.maze_size * self.maze_size)]
        self.path = []

    def at(self, x: int, y: int) -> Cell:
        return self.maze[y * self.maze_size + x]

    def generate(self) -> None:
        visited = 0
        stack = []

        # Start generating from a random cell
        x = random.randint(0, self.maze_size - 1)
        y = random.randint(0, self.maze_size - 1)
        stack.append((x, y))
        self.at(x, y).set_generated()
        visited += 1

        while visited < self.maze_size * self.maze_size:
            x, y = stack[-1]
            neighbor = []

            # Check ungenerated neighboring cells
            if x > 0 and not self.at(x - 1, y).get_generated():
                neighbor.append('left')
            if x < self.maze_size - 1 and not self.at(x + 1, y).get_generated():
                neighbor.append('right')
            if y > 0 and not self.at(x, y - 1).get_generated():
                neighbor.append('up')
            if y < self.maze_size - 1 and not self.at(x, y + 1).get_generated():
                neighbor.append('down')

            if neighbor:
                random_next = random.choice(neighbor)

                if random_next == 'left':
                    self.at(x, y).set_neighbor('left')
                    self.at(x - 1, y).set_neighbor('right')
                    self.at(x - 1, y).set_generated()
                    stack.append((x - 1, y))
                elif random_next == 'right':
                    self.at(x, y).set_neighbor('right')
                    self.at(x + 1, y).set_neighbor('left')
                    self.at(x + 1, y).set_generated()
                    stack.append((x + 1, y))
                elif random_next == 'up':
                    self.at(x, y).set_neighbor('up')
                    self.at(x, y - 1).set_neighbor('down')
                    self.at(x, y - 1).set_generated()
                    stack.append((x, y - 1))
                elif random_next == 'down':
                    self.at(x, y).set_neighbor('down')
                    self.at(x, y + 1).set_neighbor('up')
                    self.at(x, y + 1).set_generated()
                    stack.append((x, y + 1))
                visited += 1
            else:
                stack.pop()

    def solve(self, show=True, update_time_ms=10, show_visited=True) -> list[tuple[int, int]]:
        stack = []
        x, y = 0, 0
        stack.append((x, y))
        self.at(x, y).set_visited()

        while x != self.maze_size - 1 or y != self.maze_size - 1:
            x, y = stack[-1]
            self.at(x, y).set_visited()

            backtrack = True
            neighbor = self.at(x, y).get_neighbor()

            for go_to in neighbor:
                if go_to == 'left' and not self.at(x - 1, y).get_visited():
                    stack.append((x - 1, y))
                    backtrack = False
                elif go_to == 'right' and not self.at(x + 1, y).get_visited():
                    stack.append((x + 1, y))
                    backtrack = False
                elif go_to == 'up' and not self.at(x, y - 1).get_visited():
                    stack.append((x, y - 1))
                    backtrack = False
                elif go_to == 'down' and not self.at(x, y + 1).get_visited():
                    stack.append((x, y + 1))
                    backtrack = False

            if backtrack:
                stack.pop()

            if show:
                self.show(show_visited)
                pygame.draw.rect(screen, GREEN, (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
                pygame.display.flip()
                pygame.time.delay(update_time_ms)

        self.path = stack
        if (self.maze_size - 1, self.maze_size - 1) not in self.path:
            self.path.append((self.maze_size - 1, self.maze_size - 1))
        return self.path

    def show(self, show_visited=False) -> None:
        screen.fill(WHITE)
        for y in range(self.maze_size):
            for x in range(self.maze_size):
                cell = self.at(x, y)
                if show_visited and cell.get_visited():
                    pygame.draw.rect(screen, GREY, (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
                if 'left' not in cell.neighbor:
                    pygame.draw.line(screen, BLACK, (x * self.cell_size, y * self.cell_size), (x * self.cell_size, (y + 1) * self.cell_size))
                if 'right' not in cell.neighbor:
                    pygame.draw.line(screen, BLACK, ((x + 1) * self.cell_size, y * self.cell_size), ((x + 1) * self.cell_size, (y + 1) * self.cell_size))
                if 'up' not in cell.neighbor:
                    pygame.draw.line(screen, BLACK, (x * self.cell_size, y * self.cell_size), ((x + 1) * self.cell_size, y * self.cell_size))
                if 'down' not in cell.neighbor:
                    pygame.draw.line(screen, BLACK, (x * self.cell_size, (y + 1) * self.cell_size), ((x + 1) * self.cell_size, (y + 1) * self.cell_size))
        for x, y in self.path:
            pygame.draw.circle(screen, BLUE, (x * self.cell_size + self.cell_size // 2, y * self.cell_size + self.cell_size // 2), self.cell_size // 5)
        pygame.draw.rect(screen, YELLOW, ((self.maze_size - 1) * self.cell_size, (self.maze_size - 1) * self.cell_size, self.cell_size, self.cell_size))
        pygame.display.flip()


def main() -> None:
    maze = Maze(maze_size, cell_size)
    maze.generate()
    solution_path = maze.solve(True, UPDATE_TIME_MS, True)
    print(" ")
    print("Program Built by 210690, 210680 and 210697")
    print(" ")

    print('Solution path:', solution_path)
    maze.show(True)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


if __name__ == '__main__':
    main()
