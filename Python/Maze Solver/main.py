from collections import deque

with open("Map/map01.txt", "r") as f:
    labyrinth = [list(line.strip()) for line in f if line.strip()]

# Find start (A) and end (B) positions
for i, row in enumerate(labyrinth):
    for j, cell in enumerate(row):
        if cell == 'A':
            start = (i, j)
        if cell == 'B':
            end = (i, j)

def is_solvable(labyrinth, start, end):
    rows, cols = len(labyrinth), len(labyrinth[0])
    visited = [[False]*cols for _ in range(rows)]
    queue = deque([start])
    visited[start[0]][start[1]] = True

    while queue:
        x, y = queue.popleft()
        if (x, y) == end:
            return True
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < rows and 0 <= ny < cols:
                if not visited[nx][ny] and labyrinth[nx][ny] in ('0', 'B'):
                    visited[nx][ny] = True
                    queue.append((nx, ny))
    return False

if is_solvable(labyrinth, start, end):
    print("Solvable")
else:
    print("Not solvable")
