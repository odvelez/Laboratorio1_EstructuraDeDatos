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
        screen.fill((15, 22, 35))
        cx = screen.get_width() // 2

        title = self.title_font.render("LEADERBOARD", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(cx, 60)))

        self.tab_rects.clear()
        tab_y = 115
        tab_spacing = 180
        tab_start_x = cx - tab_spacing
        for i, dif in enumerate(DIFICULTADES):
            is_active = i == self.tab_index
            color = (255, 220, 0) if is_active else (160, 160, 160)
            label = self.tab_font.render(dif.upper(), True, color)
            rect = label.get_rect(center=(tab_start_x + i * tab_spacing, tab_y))
            self.tab_rects.append(rect)
            screen.blit(label, rect)
            if is_active:
                pygame.draw.line(screen, color, (rect.left, rect.bottom + 2), (rect.right, rect.bottom + 2), 2)

        dificultad = DIFICULTADES[self.tab_index]
        scores = self.rankings_cache.get(dificultad, [])

        start_y = 170
        spacing = 38
        if scores:
            for pos, (nombre, puntos) in enumerate(scores, start=1):
                line = self.item_font.render(f"{pos}. {nombre}  {puntos}", True, (220, 220, 220))
                screen.blit(line, line.get_rect(center=(cx, start_y + (pos - 1) * spacing)))
        else:
            empty = self.item_font.render("No scores yet", True, (130, 130, 130))
            screen.blit(empty, empty.get_rect(center=(cx, start_y + 60)))

        nav_hint = self.info_font.render("< LEFT / RIGHT > to switch difficulty", True, (140, 140, 140))
        screen.blit(nav_hint, nav_hint.get_rect(center=(cx, screen.get_height() - 70)))

        back_color = (255, 220, 0) if self.back_hover else (200, 200, 200)
        back_text = self.info_font.render("BACK (ESC)", True, back_color)
        self.back_rect = back_text.get_rect(center=(cx, screen.get_height() - 35))
        screen.blit(back_text, self.back_rect)
