import pygame as pg

_ = False

# 1 = Wall, 2 = Safe Zone (Green Wall), 3 = File, 4 = Player Start
MAP_DATA = [
    [ # Level 1: Outpost (15x11)
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 2, 2, 2, 2, 2, 1, _, _, _, 3, _, _, _, 1],
        [1, 2, 4, _, _, 2, 1, _, 1, 1, 1, 1, 1, _, 1],
        [1, 2, _, _, _, 2, 1, _, _, _, _, _, 1, _, 1],
        [1, 2, 2, 2, _, 2, 1, 1, 1, _, 1, _, 1, _, 1],
        [1, _, _, _, _, _, _, _, _, _, 1, _, _, _, 1],
        [1, _, 1, 1, 1, 1, 1, _, 1, 1, 1, 1, 1, 1, 1],
        [1, 3, 1, _, _, _, 1, _, _, _, _, _, _, 3, 1],
        [1, _, 1, _, 3, _, 1, 1, 1, 1, 1, 1, 1, _, 1],
        [1, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ],
    [ # Level 2: The Grid (18x11)
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 2, 2, 2, 1, 3, _, _, _, 1, 3, _, _, _, _, _, 3, 1],
        [1, 2, 4, _, 1, _, 1, 1, _, 1, _, 1, 1, 1, 1, 1, _, 1],
        [1, 2, _, _, _, _, _, 1, _, 1, _, _, _, _, _, 1, _, 1],
        [1, 1, 1, 1, 1, 1, _, 1, _, 1, 1, 1, 1, 1, _, 1, _, 1],
        [1, _, _, _, _, _, _, 1, _, _, _, _, _, _, _, 1, _, 1],
        [1, _, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, _, 1, 1, 1, _, 1],
        [1, 3, _, _, _, _, _, _, _, _, _, _, _, 1, 3, _, _, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, _, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]
]

class Map:
    def __init__(self, game):
        self.game = game
        self.mini_map = MAP_DATA[self.game.current_level]
        self.world_map = {}
        self.files_map = {}
        self.player_start = (2, 2)
        self.get_map()

    def get_map(self):
        for j, row in enumerate(self.mini_map):
            for i, vaule in enumerate(row):
                if vaule == 1 or vaule == 2:
                    self.world_map[(i, j)] = vaule
                elif vaule == 3:
                    self.files_map[(i, j)] = vaule
                elif vaule == 4:
                    self.player_start = (i + 0.5, j + 0.5)
                self.game.total_files = len(self.files_map)

    def draw(self):
        [pg.draw.rect(self.game.screen, 'darkgray', (pos[0] * 100, pos[1] * 100, 100, 100), 2)
        for pos in self.world_map]
