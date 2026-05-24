import pygame as pg
import sys
import math
import settings as st

class Menu:
    def __init__(self, game):
        self.game = game
        self.font = pg.font.SysFont('arial', 40, bold=True)
        self.title_font = pg.font.SysFont('arial', 80, bold=True)
        self.menu_state = 'main' # 'main', 'settings', 'credits'
        
        # Opções base para os menus
        self.main_options_base = ['PLAY', 'SETTINGS', 'CREDITS', 'EXIT']
        self.settings_options = ['RESOLUTION', 'SENSITIVITY', 'BACK']
        self.credits_options = ['BACK']
        
        self.credits_info = [
            "     THE NIGHTMARE           ",
            "---------------------------",
            "    DEV: Heitor Pessoa    ",
            "      Engine: VSCode       ",
            "     Language: Python      "
        ]

        self.selected_index = 0
        
        # Tracking current choices
        self.res_idx = st.RES_OPTIONS.index(st.RES) if st.RES in st.RES_OPTIONS else 0
        self.sens_idx = st.SENS_OPTIONS.index(st.MOUSE_SENSITIVITY) if st.MOUSE_SENSITIVITY in st.SENS_OPTIONS else 1

    def draw(self):
        # O fundo agora é desenhado no main.py para efeito dinâmico
        right_pos = st.WIDTH - 60

        # Desenhar moldura tecnológica
        pg.draw.rect(self.game.screen, 'red', (st.WIDTH - 440, 40, 420, st.HEIGHT - 80), 3)
        pg.draw.rect(self.game.screen, 'red', (st.WIDTH - 430, 50, 400, st.HEIGHT - 100), 1)

        # Efeito de Scanlines
        for i in range(40, st.HEIGHT - 40, 4):
            pg.draw.line(self.game.screen, (25, 0, 0), (st.WIDTH - 440, i), (st.WIDTH - 20, i))
        
        if self.menu_state == 'main':
            current_main_options = list(self.main_options_base) # Create a mutable copy
            if self.game.paused:
                current_main_options[0] = 'RESUME' # Change 'PLAY' to 'RESUME' if paused

            self.draw_text('THE OX', self.title_font, (50, 0, 0), right_pos + 6, st.HEIGHT // 4 + 6, align='right')
            self.draw_text('THE OX', self.title_font, 'red', right_pos, st.HEIGHT // 4, align='right')
            for i, option in enumerate(current_main_options):
                text = f"> {option}" if i == self.selected_index else option
                color = 'yellow' if i == self.selected_index else 'white'
                self.draw_text(text, self.font, color, right_pos, st.HEIGHT // 2 + i * 60, align='right')
        
        elif self.menu_state == 'settings':
            self.draw_text('SETTINGS', self.title_font, 'blue', right_pos, st.HEIGHT // 4, align='right')
            for i, option in enumerate(self.settings_options):
                if option == 'RESOLUTION':
                    res = st.RES_OPTIONS[self.res_idx]
                    text = f"RES: {res[0]}x{res[1]}"
                elif option == 'SENSITIVITY':
                    sens = st.SENS_OPTIONS[self.sens_idx]
                    text = f"SENS: {sens}"
                else:
                    text = option
                    
                color = 'yellow' if i == self.selected_index else 'white'
                self.draw_text(text, self.font, color, right_pos, st.HEIGHT // 2 + i * 60, align='right')

        elif self.menu_state == 'credits':
            self.draw_text('CREDITS', self.title_font, 'green', right_pos, st.HEIGHT // 5, align='right')
            for i, line in enumerate(self.credits_info):
                self.draw_text(line, self.font, 'white', right_pos, st.HEIGHT // 2 - 50 + i * 45, align='right')
            
            # Botão BACK nos créditos
            color = 'yellow'
            self.draw_text('BACK', self.font, color, right_pos, st.HEIGHT - 100, align='right')

    def draw_text(self, text, font, color, x, y, align='center'):
        render = font.render(text, True, color)
        rect = render.get_rect()
        if align == 'right':
            rect.midright = (x, y)
        else:
            rect.center = (x, y)
        self.game.screen.blit(render, rect)

    def update(self):
        pass

    def handle_input(self, event):
        if event.type == pg.KEYDOWN:
            current_options_list = []
            if self.menu_state == 'main':
                current_options_list = list(self.main_options_base)
                if self.game.paused:
                    current_options_list[0] = 'RESUME'
            elif self.menu_state == 'settings':
                current_options_list = self.settings_options
            elif self.menu_state == 'credits':
                current_options_list = self.credits_options

            if not current_options_list: # Should not happen if states are managed correctly
                return

            if event.key == pg.K_UP:
                self.selected_index = (self.selected_index - 1) % len(current_options_list)
            elif event.key == pg.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(current_options_list)
            elif event.key == pg.K_RETURN:
                self.select_option()

    def select_option(self):
        if self.menu_state == 'main':
            current_main_options = list(self.main_options_base)
            if self.game.paused:
                current_main_options[0] = 'RESUME'
            
            selected_option_text = current_main_options[self.selected_index]

            if selected_option_text == 'PLAY':
                self.game.in_menu = False
                pg.mouse.set_visible(False)
                pg.event.set_grab(True)
            elif selected_option_text == 'RESUME':
                self.game.paused = False
                pg.mouse.set_visible(False)
                pg.event.set_grab(True)
            elif selected_option_text == 'SETTINGS':
                self.menu_state = 'settings'
                self.selected_index = 0
            elif selected_option_text == 'CREDITS':
                self.menu_state = 'credits'
                self.selected_index = 0
            elif selected_option_text == 'EXIT':
                pg.quit()
                sys.exit()
        
        elif self.menu_state == 'settings':
            choice = self.settings_options[self.selected_index]
            if choice == 'BACK':
                self.menu_state = 'main'
                self.selected_index = 0
            else:
                self.change_resolution(choice)
        
        elif self.menu_state == 'credits':
            self.menu_state = 'main'
            self.selected_index = 2 # Retorna para a posição de Créditos

    def change_resolution(self, res):
        import settings
        settings.WIDTH, settings.HEIGHT = res
        settings.RES = res
        # Recalcula variáveis que dependem de WIDTH
        settings.NUM_RAYS = settings.WIDTH // 2
        settings.HALF_NUM_RAYS = settings.NUM_RAYS // 2
        settings.DELTA_ANGLE = settings.FOV / settings.NUM_RAYS
        settings.SCREEN_DIST = settings.HALF_NUM_RAYS / math.tan(settings.HALF_FOV)
        settings.SCALE = settings.WIDTH // settings.NUM_RAYS
        self.game.update_resolution()