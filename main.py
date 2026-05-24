import pygame as pg
import sys

import settings as st
from map import *
from player import *
from raycasting import *
from menu import *

class Game: 
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(st.RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.paused = False
        self.in_menu = True
        self.current_level = 0
        self.files_collected = 0
        self.total_files = 0
        self.level_transition = False
        self.transition_timer = 0
        pg.mouse.set_visible(True)
        pg.event.set_grab(False)
        self.font = pg.font.SysFont('arial', 100, bold=True)
        self.ui_font = pg.font.SysFont('arial', 25, bold=True)
        self.menu = Menu(self)
        self.new_game()

    def new_game(self):
        self.files_collected = 0
        self.map = Map(self)
        self.player = Player(self)
        self.raycasting = Raycasting(self)

    def next_level(self):
        self.current_level += 1
        if self.current_level >= len(MAP_DATA):
            self.current_level = 0
            self.in_menu = True
            pg.mouse.set_visible(True)
            pg.event.set_grab(False)
        self.new_game()

    def update_resolution(self):
        # Atualiza a janela e reinicia os componentes para aplicar a nova escala
        self.screen = pg.display.set_mode(st.RES)
        self.new_game()
        
    def update(self):
        if self.in_menu:
            # Efeito de rotação suave da câmera para o fundo do menu
            self.player.angle += 0.3 * self.delta_time
            self.raycasting.update()
            self.menu.update()
        elif self.level_transition:
            pass
        elif not self.paused:
            self.player.update()
            self.raycasting.update()
            # Trigger transition only if items exist and all are collected
            if self.total_files > 0 and self.files_collected >= self.total_files:
                self.level_transition = True
        self.delta_time = self.clock.tick(st.FPS) / 1000
        pg.display.set_caption(f'{self.clock.get_fps():.1f}')

    def draw_ui(self):
        # Stats in top right
        ui_bg = pg.Surface((200, 110))
        ui_bg.set_alpha(150)
        ui_bg.fill('black')
        self.screen.blit(ui_bg, (st.WIDTH - 210, 10))
        
        life_txt = self.ui_font.render(f"LIFE: {self.player.life}", True, 'red')
        def_txt = self.ui_font.render(f"DEF: {self.player.defense}", True, 'blue')
        files_txt = self.ui_font.render(f"FILES: {self.files_collected}/{self.total_files}", True, 'cyan')
        lvl_txt = self.ui_font.render(f"LEVEL: {self.current_level + 1}", True, 'white')

        self.screen.blit(life_txt, (st.WIDTH - 200, 20))
        self.screen.blit(def_txt, (st.WIDTH - 200, 40))
        self.screen.blit(files_txt, (st.WIDTH - 200, 60))
        self.screen.blit(lvl_txt, (st.WIDTH - 200, 80))

    def draw(self):
        if self.in_menu:
            # Desenha o mundo como fundo "injogável"
            self.screen.fill('black')
            pg.draw.rect(self.screen, (30, 30, 30), (0, 0, st.WIDTH, st.HEIGHT // 2))
            pg.draw.rect(self.screen, (15, 15, 15), (0, st.HEIGHT // 2, st.WIDTH, st.HEIGHT))
            self.raycasting.draw()
            self.raycasting.draw_items()
            
            # Overlay escuro para destacar o texto do menu
            overlay = pg.Surface((st.WIDTH, st.HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            
            self.menu.draw()
        elif self.paused:
            self.screen.fill('black')
            render = self.font.render('PAUSED', True, 'white')
            rect = render.get_rect(center=(st.WIDTH // 2, st.HEIGHT // 2))
            self.screen.blit(render, rect)
        elif self.level_transition:
            self.screen.fill((5, 5, 25))
            glow = math.sin(pg.time.get_ticks() * 0.005) * 55 + 200
            render = self.font.render('LEVEL COMPLETED', True, (glow, glow, 0))
            rect = render.get_rect(center=(st.WIDTH // 2, st.HEIGHT // 2 - 60))
            self.screen.blit(render, rect)
            
            msg = self.ui_font.render(f"FILES DECRYPTED: {self.files_collected} / {self.total_files}", True, 'white')
            self.screen.blit(msg, (st.WIDTH // 2 - msg.get_width() // 2, st.HEIGHT // 2 + 20))
            
            if (pg.time.get_ticks() // 500) % 2:
                prompt = self.ui_font.render('PRESS [ENTER] TO UPLOAD DATA AND CONTINUE', True, 'cyan')
                self.screen.blit(prompt, (st.WIDTH // 2 - prompt.get_width() // 2, st.HEIGHT // 2 + 100))
        else:
            self.screen.fill('black')
            # Desenha Teto e Chão
            pg.draw.rect(self.screen, (40, 40, 40), (0, 0, st.WIDTH, st.HEIGHT // 2))
            pg.draw.rect(self.screen, (20, 20, 20), (0, st.HEIGHT // 2, st.WIDTH, st.HEIGHT))
            
            self.raycasting.draw()
            self.raycasting.draw_items()
            # self.map.draw() 
            # self.player.draw()
            self.draw_ui()

        pg.display.flip()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            
            if self.in_menu:
                self.menu.handle_input(event)
                continue

            if self.level_transition:
                if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    self.level_transition = False
                    self.next_level()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.paused = not self.paused
                    pg.mouse.set_visible(self.paused)
                    pg.event.set_grab(not self.paused)
                    if not self.paused:
                        pg.mouse.get_rel()

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()

if __name__ == '__main__':
    game = Game()
    game.run()