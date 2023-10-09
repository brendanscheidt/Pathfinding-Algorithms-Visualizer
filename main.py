import pygame
import math
import random
from Button import Button
from Node import Node
from Dropdown import Dropdown
from Grid import Grid
from Algorithms import (
    reconstruct_path,
    h,
    dfs,
    bfs,
    bidirectional_search,
    reconstruct_bidirectional_path,
    dijkstra,
    aStar,
)

from queue import PriorityQueue
from collections import deque

pygame.init()
pygame.font.init()

WIDTH = 1000
HEIGHT = 860
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Path Finding Algorithm Visualizer")
BUTTON_AREA_HEIGHT = 80


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
DARK_GREY = (200, 200, 200)
LIGHT_GREEN = (0, 150, 0)
LIGHT_WHITE = (200, 200, 200)
LIGHT_RED = (255, 102, 102)

font = pygame.font.SysFont("calibri", 16)


# +60 to adjust for the buttons


def draw(
    win,
    grid,
    grid_obj,
    rows,
    width,
    start_button,
    end_button,
    barrier_button,
    start_algo_button,
    reset_button,
    maze_button,
    algorithm_dropdown,
    mouse_pos,
    mode,
):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    grid_obj.draw_grid(win)

    # Draw the buttons after filling the window and drawing the grid
    start_button.draw(win, (0, 0, 0))
    end_button.draw(win, (0, 0, 0))
    barrier_button.draw(win, (0, 0, 0))
    start_algo_button.draw(win, (0, 0, 0))
    reset_button.draw(win, (0, 0, 0))
    algorithm_dropdown.draw(win)
    maze_button.draw(win, (0, 0, 0))

    color = get_color_from_mode(mode)
    if color and mouse_pos[1] > BUTTON_AREA_HEIGHT:
        pygame.draw.rect(win, color, (mouse_pos[0] - 5, mouse_pos[1] - 5, 10, 10))

    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    x, y = pos

    col = x // gap
    row = (y - BUTTON_AREA_HEIGHT) // gap  # Adjust the y position here

    # Ensure row is within valid range
    row = min(max(row, 0), rows - 1)

    return row, col


def get_color_from_mode(mode):
    if mode == "start":
        return ORANGE
    elif mode == "end":
        return TURQUOISE
    elif mode == "barrier":
        return BLACK
    else:
        return None


def generate_random_maze(grid, barrier_probability=0.3):
    """
    Fills the grid with barriers based on the given probability.

    :param grid: The grid of nodes.
    :param barrier_probability: Probability of a node being a barrier.
    """
    # First, clear the grid except for start and end nodes
    for row in grid:
        for node in row:
            if (
                not node.is_start() and not node.is_end()
            ):  # Assuming you have methods like these in your node class
                node.reset()  # Assuming you have a reset method in your node class that sets the node back to its default state

    # Now, generate the random barriers
    for row in grid:
        for node in row:
            if (
                not node.is_start()
                and not node.is_end()
                and random.random() < barrier_probability
            ):
                node.make_barrier()


def main(win, width):
    ROWS = 50
    grid_obj = Grid(ROWS, width)
    grid = grid_obj.grid
    start = None
    end = None
    run = True
    started = False
    algorithm_ran = False

    # Create button instances
    start_button = Button(ORANGE, 10, 10, 100, 50, "Start Node", YELLOW)
    end_button = Button(TURQUOISE, 120, 10, 100, 50, "End Node", BLUE)
    barrier_button = Button(GREY, 230, 10, 100, 50, "Barrier", LIGHT_WHITE)
    start_algo_button = Button(GREEN, 340, 10, 150, 50, "Start Algorithm", LIGHT_GREEN)
    reset_button = Button(WHITE, 500, 10, 100, 50, "Reset", LIGHT_WHITE)
    maze_button = Button(LIGHT_RED, 830, 10, 150, 50, "Generate Maze", RED)

    # Create dropdown menu for algorithm selection
    algorithms = ["A* Search", "Dijkstra", "BFS", "DFS", "Bidirectional Search"]
    algorithm_dropdown = Dropdown(610, 10, 180, 50, algorithms)

    # Variable to track the current mode (start, end, barrier)
    mode = None

    while run:
        mouse_pos = pygame.mouse.get_pos()

        if not algorithm_ran:
            for button in [
                start_button,
                end_button,
                barrier_button,
                start_algo_button,
                reset_button,
                maze_button,
            ]:
                if button.is_over(mouse_pos) and not button.pressed:
                    button.color = button.hover_color
                    button.state_changed = True
                elif not button.is_over(mouse_pos) and not button.pressed:
                    button.color = button.default_color
                    button.state_changed = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            pos = pygame.mouse.get_pos()

            start_button.handle_event(event)
            end_button.handle_event(event)
            barrier_button.handle_event(event)
            start_algo_button.handle_event(event)
            reset_button.handle_event(event)
            algorithm_dropdown.handle_event(event)
            maze_button.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_over(pos):
                    start_button.pressed = True
                    mode = "start"
                elif end_button.is_over(pos):
                    end_button.pressed = True
                    mode = "end"
                elif barrier_button.is_over(pos):
                    barrier_button.pressed = True
                    mode = "barrier"
                elif maze_button.is_over(pos) and not algorithm_ran:
                    maze_button.pressed = True
                    mode = "maze"
                    generate_random_maze(grid)
                elif reset_button.is_over(pos):
                    reset_button.pressed = True
                    start = None
                    end = None
                    grid_obj = Grid(ROWS, width)
                    grid = grid_obj.grid
                    mode = None
                    algorithm_ran = False
                elif start_algo_button.is_over(pos):
                    start_algo_button.pressed = True
                    mode = "start_algo"
                if mode == "start_algo":
                    if start and end and not algorithm_ran:
                        # Start the algorithm
                        for row in grid:
                            for n in row:
                                n.update_neighbors(grid)

                        # Select the algorithm based on the dropdown selection
                        if algorithm_dropdown.selected_option == "A* Search":
                            algorithm = aStar
                        elif algorithm_dropdown.selected_option == "Dijkstra":
                            algorithm = dijkstra
                        elif algorithm_dropdown.selected_option == "BFS":
                            algorithm = bfs
                        elif algorithm_dropdown.selected_option == "DFS":
                            algorithm = dfs
                        elif (
                            algorithm_dropdown.selected_option == "Bidirectional Search"
                        ):
                            algorithm = bidirectional_search
                        else:
                            algorithm = (
                                aStar  # Default to A* if no valid option is selected
                            )

                        algorithm(
                            lambda: draw(
                                win,
                                grid,
                                grid_obj,
                                ROWS,
                                width,
                                start_button,
                                end_button,
                                barrier_button,
                                start_algo_button,
                                reset_button,
                                maze_button,
                                algorithm_dropdown,
                                mouse_pos,
                                mode,
                            ),
                            grid,
                            start,
                            end,
                        )
                        algorithm_ran = True

        # Check for grid interactions outside of the event loop
        if pygame.mouse.get_pressed()[0]:  # Left Mouse Button
            row, col = get_clicked_pos(pos, ROWS, width)
            if pos[1] > BUTTON_AREA_HEIGHT:
                node = grid[row][col]
                # Place nodes based on the mode
                if mode == "start" and not start and node != end:
                    start = node
                    start.make_start()
                elif mode == "end" and not end and node != start:
                    end = node
                    end.make_end()
                elif mode == "barrier" and node != end and node != start:
                    node.make_barrier()

        if any(
            [
                btn.state_changed
                for btn in [
                    start_button,
                    end_button,
                    barrier_button,
                    start_algo_button,
                    reset_button,
                    maze_button,
                ]
            ]
        ):
            draw(
                win,
                grid,
                grid_obj,
                ROWS,
                width,
                start_button,
                end_button,
                barrier_button,
                start_algo_button,
                reset_button,
                maze_button,
                algorithm_dropdown,
                mouse_pos,
                mode,
            )
            for btn in [
                start_button,
                end_button,
                barrier_button,
                start_algo_button,
                reset_button,
                maze_button,
            ]:
                btn.state_changed = False

    pygame.quit()


main(WIN, WIDTH)
