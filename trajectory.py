import numpy as np
import matplotlib.pyplot as plt
import heapq

# Define waypoints and target coordinates (for example)
waypoints = [(0, 0), (100, 50), (200, 100)]  # Example waypoints
target_coordinates = (200, 150)  # Example target coordinates


# Calculates Euclidean distance
def euclideanDistance(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


# A* algorithm to compute waypoints
def aStar(start, goal, _waypoints):
    frontier = [(0, start)]
    came_from = {}
    cost_so_far = {start: 0}

    while frontier:
        current_cost, current = heapq.heappop(frontier)

        if current == goal:
            break

        for nxt in _waypoints:
            new_cost = cost_so_far[current] + euclideanDistance(current, nxt)
            if nxt not in cost_so_far or new_cost < cost_so_far[nxt]:
                cost_so_far[nxt] = new_cost
                priority = new_cost + euclideanDistance(nxt, goal)
                heapq.heappush(frontier, (priority, nxt))
                came_from[nxt] = current

    # Reconstruct path
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()

    return path


# Calculates optimal path using A*
def calculateOptimalPath(start, end, waypoint):
    return aStar(start, end, waypoint)


optimal_path = calculateOptimalPath(waypoints[0], target_coordinates, waypoints)

# Plotting the trajectory
x_path, y_path = zip(*optimal_path)
plt.figure()
plt.plot(x_path, y_path, marker='o', linestyle='-', color='b')
plt.scatter(*zip(*waypoints), color='g', label='Waypoints')
plt.scatter(*target_coordinates, color='r', label='Target')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Optimal Path Planning')
plt.legend()
plt.grid(True)
plt.show()
