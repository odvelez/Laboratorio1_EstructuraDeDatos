import pygame

import config
from crud import ranking


DIFICULTADES = ["facil", "medio", "dificil"]


class LeaderboardScene:
    def __init__(self):
        self.next_scene = None
        self.should_quit = False

        self.tab_index = DIFICULTADES.index(config.dificultad_actual)
        self.rankings_cache = ranking.obtener_todos_los_rankings()

        self.title_font = pygame.font.Font(None, 58)
        self.tab_font = pygame.font.Font(None, 36)
        self.item_font = pygame.font.Font(None, 34)
        self.info_font = pygame.font.Font(None, 28)

        self.tab_rects = []
        self.back_rect = pygame.Rect(0, 0, 0, 0)
        self.back_hover = False

    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        self.back_hover = self.back_rect.collidepoint(mouse_pos)

        for event in events:
            if event.type == pygame.QUIT:
                self.should_quit = True
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._go_back()
                elif event.key == pygame.K_LEFT:
                    self.tab_index = (self.tab_index - 1) % len(DIFICULTADES)
                elif event.key == pygame.K_RIGHT:
                    self.tab_index = (self.tab_index + 1) % len(DIFICULTADES)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.back_rect.collidepoint(mouse_pos):
                    self._go_back()
                for i, rect in enumerate(self.tab_rects):
                    if rect.collidepoint(mouse_pos):
                        self.tab_index = i

    def _go_back(self):
        from scenes.menu import MenuScene

        self.next_scene = MenuScene()

    def update(self):
        pass

    def draw(self, screen):
        w, h = screen.get_size()
        cx = w // 2
        cy = h // 2

        screen.fill((8, 8, 26))
        tile = 34
        t = pygame.time.get_ticks() // 30
        for x in range(-tile, w + tile, tile):
            for y in range(-tile, h + tile, tile):
                color = (22, 20, 60) if ((x + y + t) // tile) % 2 == 0 else (14, 14, 42)
                rect = pygame.Rect(x, y, tile - 1, tile - 1)
                pygame.draw.rect(screen, color, rect, 0, border_radius=4)

        header = pygame.Rect(0, 0, w, 120)
        pygame.draw.rect(screen, (30, 16, 70), header)
        pygame.draw.rect(screen, (255, 220, 0), header, 2)

        title = self.title_font.render("LEADERBOARD", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(cx, 55)))

        self.tab_rects.clear()
        tab_y = header.bottom + 35
        tab_spacing = 170
        tab_start_x = cx - tab_spacing
        for i, dif in enumerate(DIFICULTADES):
            is_active = i == self.tab_index
            chip_rect = pygame.Rect(0, 0, 130, 40)
            chip_rect.center = (tab_start_x + i * tab_spacing, tab_y)
            chip_bg = (40, 220, 140) if is_active else (26, 20, 80)
            chip_border = (255, 255, 255) if is_active else (180, 160, 255)
            pygame.draw.rect(screen, chip_bg, chip_rect, border_radius=16)
            pygame.draw.rect(screen, chip_border, chip_rect, 2, border_radius=16)

            color = (10, 10, 10) if is_active else (220, 220, 220)
            label = self.tab_font.render(dif.upper(), True, color)
            rect = label.get_rect(center=chip_rect.center)
            self.tab_rects.append(chip_rect)
            screen.blit(label, rect)

        dificultad = DIFICULTADES[self.tab_index]
        scores = self.rankings_cache.get(dificultad, [])

        panel = pygame.Rect(0, 0, 540, 320)
        panel.center = (cx, cy + 40)
        pygame.draw.rect(screen, (16, 12, 46), panel, border_radius=18)
        pygame.draw.rect(screen, (120, 90, 255), panel, 3, border_radius=18)

        start_y = panel.top + 50
        spacing = 38
        if scores:
            for pos, (nombre, puntos) in enumerate(scores, start=1):
                rank_color = (255, 230, 120) if pos == 1 else (200, 220, 255)
                line = self.item_font.render(f"{pos}. {nombre}  {puntos}", True, rank_color)
                screen.blit(line, line.get_rect(center=(cx, start_y + (pos - 1) * spacing)))
        else:
            empty = self.item_font.render("No scores yet", True, (140, 140, 170))
            screen.blit(empty, empty.get_rect(center=(cx, start_y + 60)))

        nav_hint = self.info_font.render("< LEFT / RIGHT >  switch difficulty", True, (170, 170, 210))
        screen.blit(nav_hint, nav_hint.get_rect(center=(cx, h - 70)))

        back_color = (255, 220, 0) if self.back_hover else (210, 210, 230)
        back_text = self.info_font.render("BACK (ESC)", True, back_color)
        self.back_rect = back_text.get_rect(center=(cx, h - 35))
        screen.blit(back_text, self.back_rect)
