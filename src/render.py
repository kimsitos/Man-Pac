from src import Surface


class Render():
    cell_size = 50

    def _maze_draw(self, maze: list[list[int]]) -> Surface:
        E, S, O, N = 8, 4, 2, 1

        surface_maze = Surface((len(maze) * self.cell_size, len(maze[0]) * self.cell_size))
        surface_maze.fill("black")
    
        return surface_maze

