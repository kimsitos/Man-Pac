from src import Surface, draw


class Render():
    cell_size = 50
    wall_color = (255,255,255)
    #wall_wi
    def maze_draw(self, maze: list[list[int]]) -> Surface:
        N, O, S, E = 8, 4, 2, 1

        surface_maze = Surface(
            (8 * 2 + len(maze) * self.cell_size, 8 * 2 + len(maze[0]) * self.cell_size)
            )
        surface_maze.fill("black")
        for y in range(0, len(maze)):
            for x in range(0, len(maze[y])):
                value = maze[x][y]

                if value & E:
                    draw.line(
                        surface_maze,
                        self.wall_color,
                        self._board_to_pixel(x, y),
                        self._board_to_pixel(x, y + 1))
                if value & N:
                    draw.line(
                        surface_maze,
                        self.wall_color,
                        self._board_to_pixel(x, y),
                        self._board_to_pixel(x+1, y)
                    )
                if value & S:
                    draw.line(
                        surface_maze,
                        self.wall_color,
                        self._board_to_pixel(x, y + 1),
                        self._board_to_pixel(x+1, y + 1)
                    )
                if value & O:
                    draw.line(
                        surface_maze,
                        self.wall_color,
                        self._board_to_pixel(x + 1, y),
                        self._board_to_pixel(x + 1, y + 1)
                    )

        return surface_maze
    
    def _board_to_pixel(self, x: int, y: int) -> tuple[int, int]:
        return (8 + x * self.cell_size, 8 + y * self.cell_size)
    

