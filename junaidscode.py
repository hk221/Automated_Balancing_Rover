maze = [[1,"S",1,1,1,1,1,1],
        [1,0,1,1,1,0,1,1],
        [1,0,0,0,0,1,1,1],
        [1,1,1,1,0,0,1,1],
        [1,1,1,1,1,0,0,1],
        [1,1,1,1,1,1,"E",1]]

# Find the start and end position
for r in range(len(maze)):
    for c in range(len(maze[r])):
        if maze[r][c] == "S":
            start_pos = [r,c]
        if maze[r][c] == "E":
            end_pos = [r,c]

width = len(maze[0]) # 8
height = len(maze) # 6
solvable = True
# When i find S and E, check they are on the edge, otherwise its unsolvable
if not (start_pos[0] == 0 or start_pos[0] == len(maze)-1 or start_pos[1] == 0 or start_pos[1] == len(maze[0])-1):
    solvable = False
if not (end_pos[0] == 0 or end_pos[0] == len(maze)-1 or end_pos[1] == 0 or end_pos[1] == len(maze[0])-1):
    solvable = False

# Create a function that given a starting row and column, finds all possible moves
possible_moves = [[start_pos]]
relationship = {}
i = 0
end_found = False
# Outputs a list of all possible moves
while end_found is False:
    try:
        for j in range(len(possible_moves[i])):
            row = possible_moves[i][j][0]
            col = possible_moves[i][j][1]
            tmp = []

            if (row > 0) and (maze[row - 1][col] != 1): # looking up
                # check if it already exists
                exists = any([row - 1,col] in sublist for sublist in possible_moves)
                if not exists:
                    tmp.append([row - 1,col])
            if (row < len(maze) - 1) and (maze[row+1][col] != 1): # looking down
                exists = any([row + 1,col] in sublist for sublist in possible_moves)
                if not exists:
                    tmp.append([row + 1,col])
            if (col > 0) and (maze[row][col - 1] != 1): # looking left
                exists = any([row,col - 1] in sublist for sublist in possible_moves)
                if not exists:    
                    tmp.append([row,col - 1])
            if (col < len(maze[0]) - 1) and (maze[row][col + 1] != 1): # looking right
                exists = any([row,col + 1] in sublist for sublist in possible_moves)
                if not exists:
                    tmp.append([row,col + 1])
            # If tmp is empty, dont add it
            if bool(tmp) is not False:
                possible_moves.append(tmp)
                relationship.update({str([row, col]):tmp})
            end_found = any(end_pos in sublist for sublist in possible_moves)
        i += 1
    except:
        solvable = False
        break

path = [end_pos]
if end_found is True:
    found = False
    # Find the first value containing the end square
    end_value = end_pos
    while not found:
        for key,value in relationship.items():
            if end_value in value:
                end_value = eval(key)
                path.insert(0, end_value)
                if end_value == start_pos:
                    found = True
print(path)
