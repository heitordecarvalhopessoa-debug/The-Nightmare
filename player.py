import settings as st
import pygame as pg
import math

class Player:
    def __init__ (self, game):
        self.game = game
        self.x, self.y = self.game.map.player_start
        self.angle = st.PLAYER_ANGLE
        self.z = 0 # Posição vertical para o pulo
        self.vel_z = 0
        self.is_jumping = False
        
        # Stats
        self.life = 100
        self.defense = 50

    def mouse_control(self):
        mx, my = pg.mouse.get_pos()
        if mx < 100 or mx > st.WIDTH - 100:
            pg.mouse.set_pos([st.WIDTH // 2, st.HEIGHT // 2])
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-st.MOUSE_MAX_REL, min(st.MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * st.MOUSE_SENSITIVITY

    def movement(self):
        sin_a, cos_a = math.sin(self.angle), math.cos(self.angle)
        dx, dy = 0, 0
        speed = st.PLAYER_SPEED * self.game.delta_time
        
        # Pulo
        if not self.is_jumping and pg.key.get_pressed()[pg.K_SPACE]:
            self.is_jumping = True
            self.vel_z = st.JUMP_SPEED

        speed_sin = speed * sin_a
        speed_cos = speed * cos_a
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            dx += -speed_cos
            dy += -speed_sin
        if keys[pg.K_a]:
            dx += speed_sin
            dy += -speed_cos
        if keys[pg.K_d]:
            dx += -speed_sin
            dy += speed_cos

        if keys[pg.K_LEFT]:
            self.angle -= st.PLAYER_ROT_SPEED * self.game.delta_time
        if keys[pg.K_RIGHT]:
            self.angle += st.PLAYER_ROT_SPEED * self.game.delta_time

        self.check_wall_collision(dx, dy)
        self.angle %= math.tau
        
    def check_file_collection(self):
        # File collection logic
        if self.map_pos in self.game.map.files_map:
            self.game.map.files_map.pop(self.map_pos)
            self.game.files_collected += 1
            self.z += 5 # Feedback visual na coleta

    def jump_logic(self):
        if self.is_jumping:
            self.z += self.vel_z * self.game.delta_time
            self.vel_z -= st.GRAVITY * self.game.delta_time
            if self.z < 0:
                self.z = 0
                self.is_jumping = False
                self.vel_z = 0

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map
    
    def check_wall_collision(self, dx, dy):
        if self.check_wall(int(self.x + dx), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy)):
            self.y += dy

    def draw(self):
        pg.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)

    def update(self):
        self.mouse_control()
        self.movement()
        self.check_file_collection()
        self.jump_logic()

    @property
    def pos(self):
        return (self.x, self.y)

    @property
    def map_pos(self):
        return int(self.x), int(self.y)