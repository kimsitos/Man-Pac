from mazegenerator import MazeGenerator
from random import randint

labernto = MazeGenerator()

labernto.generate(seed=randint(-20, 95345892536))

for row in labernto.maze:
    print(row)