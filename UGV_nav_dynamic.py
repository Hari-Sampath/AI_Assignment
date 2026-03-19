import heapq
import random

GRID_SIZE = 10


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star(grid, start, goal):
    pq = [(0, start)]
    came_from = {}
    cost_so_far = {start: 0}

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while pq:
        _, current = heapq.heappop(pq)

        if current == goal:
            break

        for d in directions:
            next_node = (current[0] + d[0], current[1] + d[1])

            if 0 <= next_node[0] < GRID_SIZE and 0 <= next_node[1] < GRID_SIZE:
                if grid[next_node[0]][next_node[1]] == 1:
                    continue

                new_cost = cost_so_far[current] + 1

                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + heuristic(goal, next_node)
                    heapq.heappush(pq, (priority, next_node))
                    came_from[next_node] = current

    path = []
    node = goal
    while node != start:
        path.append(node)
        node = came_from.get(node, start)
    path.append(start)
    path.reverse()

    return path


grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

start = (0, 0)
goal = (9, 9)

current = start

while current != goal:
    path = a_star(grid, current, goal)

    if len(path) < 2:
        print("No path possible")
        break

    next_step = path[1]

    if random.random() < 0.3:
        x, y = random.randint(0, 9), random.randint(0, 9)
        grid[x][y] = 1
        print("New obstacle at:", (x, y))

    current = next_step
    print("Moving to:", current)

print("Reached Goal!")
