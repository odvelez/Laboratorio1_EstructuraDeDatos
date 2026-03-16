import pygame

import config


class SettingsScene:
    def __init__(self):
        self.next_scene = None
        self.should_quit = False

        self.options = ["DIFFICULTY", "VOLUME", "FULLSCREEN", "BACK"]
        self.selected_index = 0

        self.volume = 5
        self.indice_dificultad = config.dificultades.index(config.dificultad_actual)
        self.fullscreen = False

        self.title_font = pygame.font.Font(None, 60)
        self.option_font = pygame.font.Font(None, 38)
        self.info_font = pygame.font.Font(None, 28)

    def handle_events(self, events):
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

    def _apply_option_action(self):
        option = self.options[self.selected_index]

        if option == "DIFFICULTY":
            self.indice_dificultad = (self.indice_dificultad + 1) % len(config.dificultades)
            config.dificultad_actual = config.dificultades[self.indice_dificultad]
        elif option == "VOLUME":
            self.volume = (self.volume + 1) % 11
        elif option == "FULLSCREEN":
            self.fullscreen = not self.fullscreen
        elif option == "BACK":
            from scenes.menu import MenuScene

            self.next_scene = MenuScene()

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((25, 15, 35))

        title = self.title_font.render("SETTINGS", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(screen.get_width() // 2, 90)))

        rendered_options = [
            f"DIFFICULTY: {config.dificultad_actual.upper()}",
            f"VOLUME: {self.volume}",
            f"FULLSCREEN: {'ON' if self.fullscreen else 'OFF'}",
            "BACK",
        ]

        start_y = 200
        spacing = 55
        for index, text in enumerate(rendered_options):
            color = (255, 220, 0) if index == self.selected_index else (225, 225, 225)
            line = self.option_font.render(text, True, color)
            line_rect = line.get_rect(center=(screen.get_width() // 2, start_y + index * spacing))
            screen.blit(line, line_rect)

        hint = self.info_font.render("ENTER to modify, ESC to return", True, (210, 210, 210))
        screen.blit(hint, hint.get_rect(center=(screen.get_width() // 2, screen.get_height() - 35)))
