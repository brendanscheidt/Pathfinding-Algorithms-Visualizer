import pygame
from queue import PriorityQueue
from collections import deque


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def dfs(draw, grid, start, end):
    stack = [start]
    came_from = {}
    visited = set([start])

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = stack.pop()

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited:
                stack.append(neighbor)
                visited.add(neighbor)
                came_from[neighbor] = current
                neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False


def bfs(draw, grid, start, end):
    queue = deque([start])
    came_from = {}
    visited = set([start])

    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = queue.popleft()

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited:
                queue.append(neighbor)
                visited.add(neighbor)
                came_from[neighbor] = current
                neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False


def bidirectional_search(draw, grid, start, end):
    # Initialize two open sets (as deques) for the forward and backward searches
    open_set_forward = deque([start])
    open_set_backward = deque([end])

    # Dictionaries to store where each node came from for both searches
    came_from_forward = {}
    came_from_backward = {}

    visited_forward = {start}
    visited_backward = {end}

    while open_set_forward and open_set_backward:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Expand the forward search
        current_forward = open_set_forward.popleft()
        if current_forward in visited_backward:  # Intersection found
            reconstruct_bidirectional_path(
                came_from_forward, came_from_backward, current_forward, draw
            )
            return True
        for neighbor in current_forward.neighbors:
            if neighbor not in visited_forward:
                came_from_forward[neighbor] = current_forward
                open_set_forward.append(neighbor)
                visited_forward.add(neighbor)
                neighbor.make_open()
        draw()

        # Expand the backward search
        current_backward = open_set_backward.popleft()
        if current_backward in visited_forward:  # Intersection found
            reconstruct_bidirectional_path(
                came_from_forward, came_from_backward, current_backward, draw
            )
            return True
        for neighbor in current_backward.neighbors:
            if neighbor not in visited_backward:
                came_from_backward[neighbor] = current_backward
                open_set_backward.append(neighbor)
                visited_backward.add(neighbor)
                neighbor.make_open()
        draw()

        # Update colors
        if current_forward != start:
            current_forward.make_closed()
        if current_backward != end:
            current_backward.make_closed()

    return False


def reconstruct_bidirectional_path(
    came_from_forward, came_from_backward, intersection, draw
):
    # Color the intersection node first
    intersection.make_path()
    draw()

    # Reconstruct the path from the start to the intersection
    current = intersection
    while current in came_from_forward:
        current = came_from_forward[current]
        current.make_path()
        draw()

    # Reconstruct the path from the end to the intersection
    current = intersection
    while current in came_from_backward:
        current = came_from_backward[current]
        current.make_path()
        draw()


def dijkstra(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((g_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False


def aStar(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False
