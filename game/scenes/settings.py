import pygame

import config

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

        if option == "DIFFICULTY":
            self.indice_dificultad = (self.indice_dificultad + 1) % len(config.dificultades)
            config.dificultad_actual = config.dificultades[self.indice_dificultad]
        elif option == "VOLUME":
            self.volume = (self.volume + 1) % 11
        elif option == "FULLSCREEN":
            if _is_fullscreen():
                pygame.display.set_mode(WINDOWED_SIZE)
            else:
                pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        elif option == "BACK":
            from scenes.menu import MenuScene

            self.next_scene = MenuScene()

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((25, 15, 35))
        w, h = screen.get_size()
        cx = w // 2
        cy = h // 2

        title = self.title_font.render("SETTINGS", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(cx, cy - 180)))

        fs_label = "ON" if _is_fullscreen() else "OFF"
        rendered_options = [
            f"DIFFICULTY: {config.dificultad_actual.upper()}",
            f"VOLUME: {self.volume}",
            f"FULLSCREEN: {fs_label}",
            "BACK",
        ]

        self.option_rects.clear()
        spacing = 55
        block_start = cy - 50
        for index, text in enumerate(rendered_options):
            color = (255, 220, 0) if index == self.selected_index else (225, 225, 225)
            line = self.option_font.render(text, True, color)
            line_rect = line.get_rect(center=(cx, block_start + index * spacing))
            self.option_rects.append(line_rect)
            screen.blit(line, line_rect)

        hint = self.info_font.render("ENTER/CLICK to modify  |  ESC to return  |  F11 fullscreen", True, (210, 210, 210))
        screen.blit(hint, hint.get_rect(center=(cx, h - 35)))
