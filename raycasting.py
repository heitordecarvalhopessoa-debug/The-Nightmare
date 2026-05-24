import pygame as pg
import math
import settings as st

class Raycasting:
    def __init__(self, game):
        self.game = game
        self.depth_buffer = [st.MAX_DEPTH] * st.NUM_RAYS

    def draw(self):
        for ray, values in enumerate(self.ray_casting_result):
            depth, proj_height, side, wall_type = values

            # Sombreamento básico baseado na distância
            intensity = 255 / (1 + depth * depth * 0.0001)
            
            if wall_type == 2: # Safe Zone Wall (Green)
                color = (0, intensity, 0)
            else: # Standard Wall (Gray)
                color = [intensity] * 3
            
            # Sombras direcionais: paredes verticais são um pouco mais escuras
            if side: color = [c * 0.7 for c in color]
            
            pg.draw.rect(self.game.screen, color, 
                         (ray * st.SCALE, st.HEIGHT // 2 - proj_height // 2 + self.game.player.z, st.SCALE, proj_height))

    def draw_items(self):
        px, py = self.game.player.pos
        items = []
        for pos in self.game.map.files_map:
            ix, iy = pos[0] + 0.5, pos[1] + 0.5
            dist = math.sqrt((px - ix)**2 + (py - iy)**2)
            items.append((dist, ix, iy))
        
        # Ordenar por distância (pintar os mais longe primeiro)
        items.sort(key=lambda x: x[0], reverse=True)

        for dist, ix, iy in items:
            dx, dy = ix - px, iy - py
            theta = math.atan2(dy, dx)
            gamma = theta - self.game.player.angle
            
            if gamma > math.pi: gamma -= math.tau
            if gamma < -math.pi: gamma += math.tau
            
            if -st.HALF_FOV - 0.2 < gamma < st.HALF_FOV + 0.2:
                corrected_dist = dist * math.cos(gamma)
                if corrected_dist < 0.1: continue
                
                proj_height = st.SCREEN_DIST / (corrected_dist + 0.0001)
                screen_x = (gamma / st.FOV + 0.5) * st.WIDTH
                
                ray_idx = int(screen_x // st.SCALE)
                if 0 <= ray_idx < st.NUM_RAYS:
                    if corrected_dist < self.depth_buffer[ray_idx]:
                        w, h = proj_height * 0.15, proj_height * 0.3
                        # Efeito flutuante
                        y_off = math.sin(pg.time.get_ticks() * 0.005) * 10
                        pg.draw.rect(self.game.screen, 'yellow', 
                                     (screen_x - w // 2, st.HEIGHT // 2 - h // 2 + self.game.player.z + y_off, w, h))

    def ray_cast(self):
        self.ray_casting_result = []
        self.depth_buffer = []
        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        ray_angle = self.game.player.angle - st.HALF_FOV + 0.0001
        for ray in range(st.NUM_RAYS):
            sin_a, cos_a = math.sin(ray_angle), math.cos(ray_angle)

            # Horizontais
            y_hor, dy = (y_map + 1, 1) if sin_a >= 0 else (y_map - 1e-6, -1)
            depth_hor = (y_hor - oy) / sin_a
            x_hor = ox + depth_hor * cos_a
            delta_depth = dy / sin_a
            dx = delta_depth * cos_a
            wall_type_hor = 0

            for i in range(st.MAX_DEPTH):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.game.map.world_map:
                    wall_type_hor = self.game.map.world_map[tile_hor]
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            # Verticais
            x_vert, dx = (x_map + 1, 1) if cos_a >= 0 else (x_map - 1e-6, -1)
            depth_vert = (x_vert - ox) / cos_a
            y_vert = oy + depth_vert * sin_a
            delta_depth = dx / cos_a
            dy = delta_depth * sin_a
            wall_type_vert = 0

            for i in range(st.MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.game.map.world_map:
                    wall_type_vert = self.game.map.world_map[tile_vert]
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            # Profundidade
            if depth_vert < depth_hor:
                depth, side, wall_type = depth_vert, 0, wall_type_vert
            else:
                depth, side, wall_type = depth_hor, 1, wall_type_hor
            
            # Remover efeito olho de peixe
            depth *= math.cos(self.game.player.angle - ray_angle)
            
            # Projeção 3D
            proj_height = st.SCREEN_DIST / (depth + 0.0001)

            self.ray_casting_result.append((depth, proj_height, side, wall_type))
            self.depth_buffer.append(depth)
            
            ray_angle += st.DELTA_ANGLE

    def update(self):
        self.ray_cast()