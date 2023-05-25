    Maze drawing approach:
    
    Discretize the Maze: Divide the maze into a grid of cells. The size of the cells will depend on the smallest gap size in the maze and the precision of the rover's sensors. Each cell represents a small area of the maze.

    Initialize a Matrix: Create a 2D array (matrix) where each element corresponds to a cell in the maze. Initialize all elements to 0, representing open space.

    Detect Walls: As the rover moves through the maze, use its sensors to detect the walls. When a wall is detected, determine which cell the wall is in.

    Update the Matrix: When a wall is detected in a cell, change the corresponding element in the matrix to 1, representing a wall.

    Draw the Maze: Use the matrix to create a graphical representation of the maze. Each cell in the matrix corresponds to a cell in the graphical representation. Cells with a value of 0 are drawn as open space, and cells with a value of 1 are drawn as walls.

    Update the Maze: As the rover continues to explore the maze and detect new walls, update the matrix and the graphical representation accordingly.