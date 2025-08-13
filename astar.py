import heapq

# Basic A* algorithm to plan from start to goal on a binary occupancy grid
def a_star(grid, start, goal, allowed_lanes):
    rows, cols = grid.shape
    open_set = []
    heapq.heappush(open_set, (0, start))  # (f_score, node)
    came_from = {}
    g_score = {start: 0}  # cost from start to this node

    def heuristic(a, b):
        # Manhattan distance (since we're on a grid)
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            # Reconstruct the path by backtracking from goal to start
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        # Explore 4-connected neighbors (N, W, E, S)
        for dy, dx in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
            neighbor = (current[0] + dy, current[1] + dx)
            ny, nx = neighbor

            if (0 <= ny < rows and 0 <= nx < cols and
                grid[ny, nx] == 0 and nx in allowed_lanes):

                tentative_g = g_score[current] + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    f = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f, neighbor))
                    came_from[neighbor] = current

    return []  # No path found
