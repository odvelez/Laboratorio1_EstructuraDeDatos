import pygame
import sys

from crud import player


class MenuScene:
    def __init__(self):
        self.options = ["START GAME", "LEADERBOARD", "HASH TABLE", "SETTINGS", "LOG OUT", "EXIT"]
        self.selected_index = 0
        self.next_scene = None
        self.should_quit = False
        self.title_font = pygame.font.Font(None, 64)
        self.option_font = pygame.font.Font(None, 40)
        self.info_font = pygame.font.Font(None, 28)
        self.option_rects = []

    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()

        for rect_index, rect in enumerate(self.option_rects):
            if rect.collidepoint(mouse_pos):
                self.selected_index = rect_index
                break

        for event in events:
            if event.type == pygame.QUIT:
                self.should_quit = True
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    self._select_option()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for rect_index, rect in enumerate(self.option_rects):
                    if rect.collidepoint(mouse_pos):
                        self.selected_index = rect_index
                        self._select_option()
                        break

    def _select_option(self):
        option = self.options[self.selected_index]

        if option == "START GAME":
            from scenes.runner_scene import RunnerScene

            self.next_scene = RunnerScene()
        elif option == "LEADERBOARD":
            from scenes.leaderboard import LeaderboardScene

            self.next_scene = LeaderboardScene()
        elif option == "HASH TABLE":
            from scenes.hashtable_scene import HashTableScene

            self.next_scene = HashTableScene()
        elif option == "SETTINGS":
            from scenes.settings import SettingsScene

            self.next_scene = SettingsScene()
        elif option == "LOG OUT":
            from scenes.login import LoginScene

            player.jugador_actual = None
            self.next_scene = LoginScene()
        elif option == "EXIT":
            self.should_quit = True
            pygame.quit()
            sys.exit()

    def update(self):
        pass

    def draw(self, screen):
        w, h = screen.get_size()
        cx = w // 2
        cy = h // 2

        screen.fill((8, 6, 20))
        grid_color = (40, 30, 80)
        tile = 40
        offset = (pygame.time.get_ticks() // 20) % tile
        for x in range(-tile, w + tile, tile):
            for y in range(-tile, h + tile, tile):
                rect = pygame.Rect(x + offset, y + offset, tile - 2, tile - 2)
                pygame.draw.rect(screen, grid_color, rect, 1, border_radius=3)

        header_rect = pygame.Rect(0, 0, w, 140)
        pygame.draw.rect(screen, (30, 10, 70), header_rect)
        pygame.draw.rect(screen, (255, 220, 0), header_rect, 2)

        title_text = self.title_font.render("GEOMETRY RUN", True, (255, 255, 255))
        screen.blit(title_text, title_text.get_rect(center=(cx, 60)))

        jugador = player.jugador_actual
        if jugador:
            info = self.info_font.render(
                f"Player: {jugador.get_nombre()}  |  Best: {jugador.get_max_score()}",
                True,
                (120, 255, 200),
            )
            info_bg = info.get_rect(center=(cx, 110))
            info_bg.inflate_ip(20, 10)
            pygame.draw.rect(screen, (15, 40, 80), info_bg, border_radius=8)
            pygame.draw.rect(screen, (0, 220, 160), info_bg, 2, border_radius=8)
            screen.blit(info, info.get_rect(center=info_bg.center))

        panel_w = 420
        panel_h = 60 * len(self.options) + 40
        panel_rect = pygame.Rect(0, 0, panel_w, panel_h)
        panel_rect.center = (cx, cy + 20)
        pygame.draw.rect(screen, (18, 12, 40), panel_rect, border_radius=12)
        pygame.draw.rect(screen, (90, 60, 200), panel_rect, 3, border_radius=12)

        self.option_rects.clear()
        spacing = 60
        start_y = panel_rect.top + 40
        for index, option in enumerate(self.options):
            is_selected = index == self.selected_index
            base_y = start_y + index * spacing
            btn_rect = pygame.Rect(0, 0, panel_w - 60, 44)
            btn_rect.center = (cx, base_y)
            bg_color = (40, 220, 120) if is_selected else (40, 30, 90)
            border_color = (255, 255, 255) if is_selected else (140, 120, 255)
            pygame.draw.rect(screen, bg_color, btn_rect, border_radius=10)
            pygame.draw.rect(screen, border_color, btn_rect, 2, border_radius=10)

            glow = btn_rect.inflate(8, 6)
            alpha = 70 if is_selected else 20
            glow_surf = pygame.Surface(glow.size, pygame.SRCALPHA)
            glow_surf.fill((0, 0, 0, 0))
            pygame.draw.rect(glow_surf, (255, 255, 255, alpha), glow_surf.get_rect(), border_radius=12)
            screen.blit(glow_surf, glow.topleft)

            color = (10, 10, 10) if is_selected else (230, 230, 230)
            option_text = self.option_font.render(option, True, color)
            option_rect = option_text.get_rect(center=btn_rect.center)
            self.option_rects.append(btn_rect)
            screen.blit(option_text, option_rect)