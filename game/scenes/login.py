import pygame

import player


class LoginScene:
    def __init__(self):
        self.next_scene = None
        self.should_quit = False

        self.nombre_input = ""
        self.max_chars = 16
        self.mensaje_error = ""
        self.cursor_visible = True
        self.cursor_timer = 0

        self.title_font = pygame.font.Font(None, 60)
        self.input_font = pygame.font.Font(None, 44)
        self.hint_font = pygame.font.Font(None, 30)
        self.error_font = pygame.font.Font(None, 28)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.should_quit = True
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self._intentar_login()
                elif event.key == pygame.K_BACKSPACE:
                    self.nombre_input = self.nombre_input[:-1]
                    self.mensaje_error = ""
                elif event.key == pygame.K_ESCAPE:
                    self.should_quit = True
                else:
                    char = event.unicode
                    if char.isprintable() and len(self.nombre_input) < self.max_chars:
                        self.nombre_input += char
                        self.mensaje_error = ""

    def _intentar_login(self):
        nombre = self.nombre_input.strip()

        if not nombre:
            self.mensaje_error = "Enter a name to continue"
            return

        mgr = player.get_manager()
        mgr.registrar_o_login(nombre)

        from scenes.menu import MenuScene

        self.next_scene = MenuScene()

    def update(self):
        self.cursor_timer += 1
        if self.cursor_timer >= 30:
            self.cursor_timer = 0
            self.cursor_visible = not self.cursor_visible

    def draw(self, screen):
        screen.fill((15, 15, 30))
        cx = screen.get_width() // 2

        title = self.title_font.render("PLAYER LOGIN", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(cx, 120)))

        hint = self.hint_font.render("Type your name and press ENTER", True, (180, 180, 180))
        screen.blit(hint, hint.get_rect(center=(cx, 200)))

        display_text = self.nombre_input
        if self.cursor_visible:
            display_text += "|"

        box_width, box_height = 360, 50
        box_rect = pygame.Rect(cx - box_width // 2, 260, box_width, box_height)
        pygame.draw.rect(screen, (40, 40, 60), box_rect)
        pygame.draw.rect(screen, (100, 100, 140), box_rect, 2)

        input_surface = self.input_font.render(display_text, True, (255, 255, 255))
        input_rect = input_surface.get_rect(midleft=(box_rect.x + 15, box_rect.centery))
        screen.blit(input_surface, input_rect)

        if self.mensaje_error:
            error = self.error_font.render(self.mensaje_error, True, (255, 80, 80))
            screen.blit(error, error.get_rect(center=(cx, 340)))

        esc_hint = self.hint_font.render("ESC to quit", True, (120, 120, 120))
        screen.blit(esc_hint, esc_hint.get_rect(center=(cx, screen.get_height() - 40)))
