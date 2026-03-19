import pygame

import config
from crud import player

WINDOWED_SIZE = (800, 600)


def _is_fullscreen():
    surface = pygame.display.get_surface()
    if surface is None:
        return False
    return bool(surface.get_flags() & pygame.FULLSCREEN)


class SettingsScene:
    def __init__(self):
        self.next_scene = None
        self.should_quit = False

        self.options = ["DIFFICULTY", "VOLUME", "FULLSCREEN", "BACK"]
        self.selected_index = 0

        self.volume = 5
        self.indice_dificultad = config.dificultades.index(config.dificultad_actual)

        jugador = player.jugador_actual
        if jugador is not None:
            settings = getattr(jugador, "settings", {})
            self.volume = int(settings.get("volume", self.volume))
            dif = settings.get("difficulty")
            if dif in config.dificultades:
                self.indice_dificultad = config.dificultades.index(dif)
                config.dificultad_actual = dif

        self.title_font = pygame.font.Font(None, 60)
        self.option_font = pygame.font.Font(None, 38)
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
                    self._apply_option_action()
                elif event.key == pygame.K_ESCAPE:
                    from scenes.menu import MenuScene

                    self.next_scene = MenuScene()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for rect_index, rect in enumerate(self.option_rects):
                    if rect.collidepoint(mouse_pos):
                        self.selected_index = rect_index
                        self._apply_option_action()
                        break

    def _apply_option_action(self):
        option = self.options[self.selected_index]

        jugador = player.jugador_actual
        mgr = player.get_manager() if hasattr(player, "get_manager") else None

        if option == "DIFFICULTY":
            self.indice_dificultad = (self.indice_dificultad + 1) % len(config.dificultades)
            config.dificultad_actual = config.dificultades[self.indice_dificultad]
            if jugador is not None:
                jugador.settings["difficulty"] = config.dificultad_actual
        elif option == "VOLUME":
            self.volume = (self.volume + 1) % 11
            if jugador is not None:
                jugador.settings["volume"] = self.volume
        elif option == "FULLSCREEN":
            if _is_fullscreen():
                pygame.display.set_mode(WINDOWED_SIZE)
                if jugador is not None:
                    jugador.settings["fullscreen"] = False
            else:
                pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                if jugador is not None:
                    jugador.settings["fullscreen"] = True
        elif option == "BACK":
            from scenes.menu import MenuScene

            self.next_scene = MenuScene()

        if mgr is not None and jugador is not None:
            mgr._guardar()

    def update(self):
        pass

    def draw(self, screen):
        w, h = screen.get_size()
        cx = w // 2
        cy = h // 2

        screen.fill((10, 6, 24))
        tile = 36
        t = pygame.time.get_ticks() // 30
        for x in range(-tile, w + tile, tile):
            for y in range(-tile, h + tile, tile):
                if (x // tile + y // tile + t // 4) % 2 == 0:
                    color = (26, 18, 70)
                else:
                    color = (18, 12, 46)
                rect = pygame.Rect(x, y, tile - 1, tile - 1)
                pygame.draw.rect(screen, color, rect, 0, border_radius=5)

        header = pygame.Rect(0, 0, w, 130)
        pygame.draw.rect(screen, (30, 12, 70), header, border_radius=0)
        pygame.draw.rect(screen, (255, 220, 0), header, 2)

        title = self.title_font.render("SETTINGS", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(cx, 60)))

        fs_label = "ON" if _is_fullscreen() else "OFF"
        rendered_options = [
            f"DIFFICULTY: {config.dificultad_actual.upper()}",
            f"VOLUME: {self.volume}",
            f"FULLSCREEN: {fs_label}",
            "BACK",
        ]

        panel = pygame.Rect(0, 0, 520, 260)
        panel.center = (cx, cy + 20)
        pygame.draw.rect(screen, (16, 10, 40), panel, border_radius=18)
        pygame.draw.rect(screen, (120, 90, 255), panel, 3, border_radius=18)

        self.option_rects.clear()
        spacing = 55
        block_start = panel.top + 50
        for index, text in enumerate(rendered_options):
            is_selected = index == self.selected_index
            btn_rect = pygame.Rect(0, 0, panel.width - 80, 40)
            btn_rect.center = (cx, block_start + index * spacing)
            bg = (40, 220, 140) if is_selected else (26, 20, 80)
            border = (255, 255, 255) if is_selected else (170, 150, 255)
            pygame.draw.rect(screen, bg, btn_rect, border_radius=12)
            pygame.draw.rect(screen, border, btn_rect, 2, border_radius=12)

            color = (10, 10, 10) if is_selected else (225, 225, 225)
            line = self.option_font.render(text, True, color)
            line_rect = line.get_rect(center=btn_rect.center)
            self.option_rects.append(btn_rect)
            screen.blit(line, line_rect)

        hint = self.info_font.render(
            "ENTER/CLICK modify   ESC return   F11 fullscreen", True, (210, 210, 230)
        )
        screen.blit(hint, hint.get_rect(center=(cx, h - 35)))
