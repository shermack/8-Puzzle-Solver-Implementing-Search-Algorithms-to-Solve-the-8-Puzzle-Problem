import numpy as np
import time
import heapq
from queue import Queue, LifoQueue
from collections import deque
from search import *
import pygame

# Set up Pygame
pygame.init()
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("8 Puzzle")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up font
font = pygame.font.SysFont("arial", 20)

# Define board size and goal state
BOARD_SIZE = 3
GOAL_STATE = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])


def generate_random_state():
    state = np.array(range(9))
    np.random.shuffle(state)
    state = np.reshape(state, (3, 3))
    return state


def bfs_search(initial_state, goal_state):
    visited = set()
    queue = Queue()
    queue.put(initial_state)
    nodes_expanded = 0

    while not queue.empty():
        current_state = queue.get()
        visited.add(tuple(current_state.flatten()))
        nodes_expanded += 1

        if np.array_equal(current_state, goal_state):
            return (current_state, nodes_expanded)

        for next_state in get_next_states(current_state):
            if tuple(next_state.flatten()) not in visited:
                queue.put(next_state)

    return (None, nodes_expanded)


def dfs_search(initial_state, goal_state):
    visited = set()
    stack = LifoQueue()
    stack.put(initial_state)
    nodes_expanded = 0

    while not stack.empty():
        current_state = stack.get()
        visited.add(tuple(current_state.flatten()))
        nodes_expanded += 1

        if np.array_equal(current_state, goal_state):
            return (current_state, nodes_expanded)

        for next_state in reversed(get_next_states(current_state)):
            if tuple(next_state.flatten()) not in visited:
                stack.put(next_state)

    return (None, nodes_expanded)


def astar_search(initial_state, goal_state, heuristic_fn):
    nodes_expanded = 0
    frontier = PriorityQueue()
    frontier.append((initial_state, 0))
    came_from = {}
    cost_so_far = {}
    came_from[tuple(initial_state.flatten())] = None
    cost_so_far[tuple(initial_state.flatten())] = 0

    while frontier:
        current_state, current_cost = frontier.pop()
        nodes_expanded += 1

        if np.array_equal(current_state, goal_state):
            return (current_state, nodes_expanded)

        for next_state in get_next_states(current_state):
            new_cost = cost_so_far[tuple(current_state.flatten())] + 1

            if (tuple(next_state.flatten()) not in cost_so_far) or (
                    new_cost < cost_so_far[tuple(next_state.flatten())]):
                cost_so_far[tuple(next_state.flatten())] = new_cost
                priority = new_cost + heuristic_fn(next_state, goal_state)
                frontier.append((next_state, priority))
                came_from[tuple(next_state.flatten())] = current_state

    return (None, nodes_expanded)


def idastar_search(initial_state, goal_state, heuristic_fn):
    nodes_expanded = 0
    threshold = heuristic_fn(initial_state, goal_state)
pygame.time.delay(5000)
