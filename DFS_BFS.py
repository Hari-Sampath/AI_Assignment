import time
from collections import deque


class EightQueens:
    def __init__(self, n=8):
        self.n = n

    def is_safe(self, state, new_col):
        """
        Checks if placing a new queen at (new_row, new_col) is safe.
        'state' contains the columns of queens placed in previous rows.
        """
        new_row = len(state)
        for row, col in enumerate(state):
            # Check column conflict or diagonal conflict
            if col == new_col or abs(col - new_col) == abs(row - new_row):
                return False
        return True

    def get_successors(self, state):
        """Generates valid next states (placing a queen in the next row)."""
        successors = []
        # If we already have N queens, no more successors
        if len(state) == self.n:
            return successors

        for col in range(self.n):
            if self.is_safe(state, col):
                # Append the new column to the current state
                successors.append(state + [col])
        return successors

    def dfs_backtracking(self):
        """Depth-First Search (Stack) - Highly efficient for this problem."""
        # State is an empty list (no queens placed yet)
        stack = [[]]
        states_explored = 0

        while stack:
            current_state = stack.pop()
            states_explored += 1

            # Goal check: Did we successfully place N queens?
            if len(current_state) == self.n:
                return current_state, states_explored

            # Add valid next moves to the stack
            for next_state in self.get_successors(current_state):
                stack.append(next_state)

        return None, states_explored

    def bfs(self):
        """Breadth-First Search (Queue) - Highly inefficient for this problem."""
        queue = deque([[]])
        states_explored = 0

        while queue:
            current_state = queue.popleft()
            states_explored += 1

            if len(current_state) == self.n:
                return current_state, states_explored

            for next_state in self.get_successors(current_state):
                queue.append(next_state)

        return None, states_explored

    def print_board(self, state):
        """Visualizes the solution array as a chessboard."""
        for row in range(self.n):
            line = ""
            for col in range(self.n):
                if state[row] == col:
                    line += " Q "
                else:
                    line += " . "
            print(line)


# --- Execution and Comparison ---
problem = EightQueens(n=8)

print("--- Depth-First Search (Backtracking) ---")
start_time = time.time()
dfs_solution, dfs_explored = problem.dfs_backtracking()
dfs_time = time.time() - start_time

print(f"Nodes Explored: {dfs_explored}")
print(f"Time Taken: {dfs_time:.5f} seconds")
print("Solution Board:")
problem.print_board(dfs_solution)


print("\n--- Breadth-First Search (BFS) ---")
start_time = time.time()
bfs_solution, bfs_explored = problem.bfs()
bfs_time = time.time() - start_time

print(f"Nodes Explored: {bfs_explored}")
print(f"Time Taken: {bfs_time:.5f} seconds")
