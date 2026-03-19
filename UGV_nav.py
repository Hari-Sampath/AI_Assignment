import heapq
import math
import random


def octile_heuristic(current, goal):
    dx = abs(current[0] - goal[0])
    dy = abs(current[1] - goal[1])
    # Cost is 1 for cardinal moves, sqrt(2) for diagonal moves
    return max(dx, dy) + (math.sqrt(2) - 1) * min(dx, dy)


def generate_battlefield(width, height, obstacle_density, start, goal):
    grid = []
    for y in range(height):
        row = []
        for x in range(width):
            # Randomly place obstacles based on the density threshold
            if random.random() < obstacle_density:
                row.append(1)
            else:
                row.append(0)
        grid.append(row)

    # Ensure start and goal are always traversable
    grid[start[1]][start[0]] = 0
    grid[goal[1]][goal[0]] = 0

    return grid


def reconstruct_path(came_from, current):
    """Traces backwards from the goal to the start to build the final path."""
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    total_path.reverse()  # Reverse to get Start -> Goal
    return total_path


# --- The Core A* Algorithm ---


def a_star_search(grid, start, goal):
    """
    Executes A* search on a 2D grid.
    Returns the optimal path, the total cost, and the number of nodes expanded (MoE).
    """
    width = len(grid[0])
    height = len(grid)

    # 8-way movement vectors and their exact costs
    directions = [
        (0, -1, 1),
        (0, 1, 1),
        (-1, 0, 1),
        (1, 0, 1),  # N, S, W, E (Cost: 1)
        (-1, -1, math.sqrt(2)),
        (1, -1, math.sqrt(2)),  # NW, NE (Cost: ~1.414)
        (-1, 1, math.sqrt(2)),
        (1, 1, math.sqrt(2)),  # SW, SE (Cost: ~1.414)
    ]

    # Priority Queue: stores tuples of (f_score, (x, y))
    frontier = []
    heapq.heappush(frontier, (0, start))

    came_from = {}

    # g_score tracks the exact cost from the start node to the current node
    g_score = {start: 0}
    nodes_expanded = 0  # MoE metric

    while frontier:
        # Pop the node with the absolute lowest f_score
        current_f, current_node = heapq.heappop(frontier)
        nodes_expanded += 1

        if current_node == goal:
            optimal_path = reconstruct_path(came_from, current_node)
            return optimal_path, g_score[current_node], nodes_expanded

        # Evaluate all 8 valid neighbors
        for dx, dy, move_cost in directions:
            neighbor = (current_node[0] + dx, current_node[1] + dy)

            # Boundary and obstacle check
            if 0 <= neighbor[0] < width and 0 <= neighbor[1] < height:
                if grid[neighbor[1]][neighbor[0]] == 1:
                    continue  # It's an obstacle, skip

                # Calculate tentative g_score for this neighbor
                tentative_g = g_score[current_node] + move_cost

                # If this is a new node, or we found a cheaper path to an existing node
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current_node
                    g_score[neighbor] = tentative_g

                    # f(n) = g(n) + h(n)
                    f_score = tentative_g + octile_heuristic(neighbor, goal)
                    heapq.heappush(frontier, (f_score, neighbor))

    return None, float("inf"), nodes_expanded  # Path not found


# --- Visualization and Execution ---


def print_grid(grid, path, start, goal):
    """Prints the battlefield to the console with the optimal path."""
    for y in range(len(grid)):
        row_str = ""
        for x in range(len(grid[0])):
            if (x, y) == start:
                row_str += "S "  # Start
            elif (x, y) == goal:
                row_str += "G "  # Goal
            elif path and (x, y) in path:
                row_str += "* "  # UGV Path
            elif grid[y][x] == 1:
                row_str += "# "  # Obstacle
            else:
                row_str += ". "  # Empty space
        print(row_str)


# Simulation Parameters
GRID_WIDTH = 30
GRID_HEIGHT = 15
START_NODE = (0, 0)
GOAL_NODE = (GRID_WIDTH - 1, GRID_HEIGHT - 1)

# Test 1: Medium Density (25%)
print("\n--- UGV Battlefield Navigation: Medium Density (25%) ---")
battlefield = generate_battlefield(GRID_WIDTH, GRID_HEIGHT, 0.25, START_NODE, GOAL_NODE)

# Run the Algorithm
optimal_path, total_cost, nodes_expanded = a_star_search(
    battlefield, START_NODE, GOAL_NODE
)

# Output Results
print_grid(battlefield, optimal_path, START_NODE, GOAL_NODE)

print("\n--- Measures of Effectiveness (MoE) ---")
if optimal_path:
    print("Path Found: YES")
    print(f"Total Optimal Cost: {total_cost:.2f} units")
    print(f"Search Efficiency (Nodes Expanded): {nodes_expanded} nodes evaluated")
else:
    print("Path Found: NO (Goal is completely walled off by obstacles)")
    print(f"Nodes Evaluated Before Giving Up: {nodes_expanded}")
