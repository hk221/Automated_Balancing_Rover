import heapq

def shortest_path(matrix, start, end):
    height = len(matrix)
    width = len(matrix[0])
    distances = [[float('inf')] * width for _ in range(height)]
    distances[start[0]][start[1]] = 0
    visited = [[False] * width for _ in range(height)]
    queue = [(0, start, [])]

    while queue:
        current_dist, current, path = heapq.heappop(queue)

        if current == end:
            return path + [current]

        if visited[current[0]][current[1]]:
            continue

        visited[current[0]][current[1]] = True

        for neighbor in get_neighbors(matrix, current):
            new_dist = current_dist + 1

            if new_dist < distances[neighbor[0]][neighbor[1]]:
                distances[neighbor[0]][neighbor[1]] = new_dist
                heapq.heappush(queue, (new_dist, neighbor, path + [current]))

    return None

def is_valid_position(matrix, position):
    row, col = position
    height = len(matrix)
    width = len(matrix[0])

    if 0 <= row < height and 0 <= col < width and matrix[row][col] == 0:
        return True

    return False

def get_neighbors(matrix, position):
    row, col = position
    neighbors = []

    if row > 0 and is_valid_position(matrix, (row - 1, col)):
        neighbors.append((row - 1, col))
    if row < len(matrix) - 1 and is_valid_position(matrix, (row + 1, col)):
        neighbors.append((row + 1, col))
    if col > 0 and is_valid_position(matrix, (row, col - 1)):
        neighbors.append((row, col - 1))
    if col < len(matrix[0]) - 1 and is_valid_position(matrix, (row, col + 1)):
        neighbors.append((row, col + 1))

    return neighbors

# Example usage:
matrix = [
    [0, 0, 0, 0, 1],
    [1, 1, 0, 0, 1],
    [0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0]
]

start = (0, 0)
end = (5, 5)

path = shortest_path(matrix, start, end)

if path:
    print("Shortest path found:")
    for position in path:
        print(position)
else:
    print("No path found.")
