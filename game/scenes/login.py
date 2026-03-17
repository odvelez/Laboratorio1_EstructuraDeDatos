import pygame

from crud import player

STATE_SELECT = "select"
STATE_INPUT = "input"

MODE_REGISTER = "register"
MODE_LOGIN = "login"

FIELD_USERNAME = 0
FIELD_PASSWORD = 1


class LoginScene:
    def __init__(self):
        self.next_scene = None
        self.should_quit = False

        self.state = STATE_SELECT
        self.mode = MODE_LOGIN
        self.menu_options = ["LOGIN", "REGISTER"]
        self.menu_index = 0

        self.username = ""
        self.password = ""
        self.active_field = FIELD_USERNAME
        self.max_chars = 20
        self.mensaje_error = ""
        self.mensaje_ok = ""

        self.cursor_visible = True
        self.cursor_timer = 0

        self.title_font = pygame.font.Font(None, 58)
        self.option_font = pygame.font.Font(None, 42)
        self.label_font = pygame.font.Font(None, 32)
        self.input_font = pygame.font.Font(None, 40)
        self.hint_font = pygame.font.Font(None, 26)
        self.msg_font = pygame.font.Font(None, 28)

        self.option_rects = []

    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()

        if self.state == STATE_SELECT:
            for i, rect in enumerate(self.option_rects):
                if rect.collidepoint(mouse_pos):
                    self.menu_index = i
                    break

        for event in events:
            if event.type == pygame.QUIT:
                self.should_quit = True
                return

            if self.state == STATE_SELECT:
                self._handle_select(event, mouse_pos)
            elif self.state == STATE_INPUT:
                self._handle_input(event)

    def _handle_select(self, event, mouse_pos):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.menu_index = (self.menu_index - 1) % len(self.menu_options)
            elif event.key == pygame.K_DOWN:
                self.menu_index = (self.menu_index + 1) % len(self.menu_options)
            elif event.key == pygame.K_RETURN:
                self._enter_input_mode()
            elif event.key == pygame.K_ESCAPE:
                self.should_quit = True

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, rect in enumerate(self.option_rects):
                if rect.collidepoint(mouse_pos):
                    self.menu_index = i
                    self._enter_input_mode()
                    break

    def _enter_input_mode(self):
        self.mode = MODE_LOGIN if self.menu_index == 0 else MODE_REGISTER
        self.state = STATE_INPUT
        self.username = ""
        self.password = ""
        self.active_field = FIELD_USERNAME
        self.mensaje_error = ""
        self.mensaje_ok = ""

    def _handle_input(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_ESCAPE:
            self.state = STATE_SELECT
            self.mensaje_error = ""
            self.mensaje_ok = ""
            return

        if event.key == pygame.K_TAB:
            self.active_field = FIELD_PASSWORD if self.active_field == FIELD_USERNAME else FIELD_USERNAME
            return

        if event.key == pygame.K_RETURN:
            self._submit()
            return

        if event.key == pygame.K_BACKSPACE:
            if self.active_field == FIELD_USERNAME:
                self.username = self.username[:-1]
            else:
                self.password = self.password[:-1]
            self.mensaje_error = ""
            return

        char = event.unicode
        if char.isprintable() and char != "":
            if self.active_field == FIELD_USERNAME and len(self.username) < self.max_chars:
                self.username += char
                self.mensaje_error = ""
            elif self.active_field == FIELD_PASSWORD and len(self.password) < self.max_chars:
                self.password += char
                self.mensaje_error = ""

    def _submit(self):
        username = self.username.strip()
        password = self.password

        if not username:
            self.mensaje_error = "Username cannot be empty"
            return
        if len(username) > self.max_chars:
            self.mensaje_error = f"Username max {self.max_chars} characters"
            return
        if not password:
            self.mensaje_error = "Password cannot be empty"
            return

        mgr = player.get_manager()

        if self.mode == MODE_REGISTER:
            jugador, error = mgr.register_user(username, password)
            if error:
                self.mensaje_error = error
                return
            mgr.set_jugador_actual(jugador)
            from scenes.menu import MenuScene
            self.next_scene = MenuScene()

        elif self.mode == MODE_LOGIN:
            jugador, error = mgr.login_user(username, password)
            if error:
                self.mensaje_error = error
                return
            mgr.set_jugador_actual(jugador)
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

        if self.state == STATE_SELECT:
            self._draw_select(screen, cx)
        elif self.state == STATE_INPUT:
            self._draw_input(screen, cx)

    def _draw_select(self, screen, cx):
        h = screen.get_height()
        cy = h // 2

        title = self.title_font.render("WELCOME", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(cx, cy - 100)))

        self.option_rects.clear()
        spacing = 60
        start_y = cy + 10
        for i, option in enumerate(self.menu_options):
            color = (255, 220, 0) if i == self.menu_index else (210, 210, 210)
            text = self.option_font.render(option, True, color)
            rect = text.get_rect(center=(cx, start_y + i * spacing))
            self.option_rects.append(rect)
            screen.blit(text, rect)

        hint = self.hint_font.render("ESC to quit", True, (120, 120, 120))
        screen.blit(hint, hint.get_rect(center=(cx, h - 35)))

    def _draw_input(self, screen, cx):
        h = screen.get_height()
        cy = h // 2

        mode_label = "REGISTER" if self.mode == MODE_REGISTER else "LOGIN"
        title = self.title_font.render(mode_label, True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(cx, cy - 180)))

        box_w, box_h = 340, 44
        user_y = cy - 90
        pass_y = cy + 10

        user_label = self.label_font.render("Username:", True, (180, 180, 180))
        screen.blit(user_label, user_label.get_rect(midleft=(cx - box_w // 2, user_y - 25)))

        user_box = pygame.Rect(cx - box_w // 2, user_y, box_w, box_h)
        border_color_u = (120, 180, 255) if self.active_field == FIELD_USERNAME else (80, 80, 110)
        pygame.draw.rect(screen, (35, 35, 55), user_box)
        pygame.draw.rect(screen, border_color_u, user_box, 2)

        user_display = self.username
        if self.active_field == FIELD_USERNAME and self.cursor_visible:
            user_display += "|"
        user_surf = self.input_font.render(user_display, True, (255, 255, 255))
        screen.blit(user_surf, user_surf.get_rect(midleft=(user_box.x + 12, user_box.centery)))

        pass_label = self.label_font.render("Password:", True, (180, 180, 180))
        screen.blit(pass_label, pass_label.get_rect(midleft=(cx - box_w // 2, pass_y - 25)))

        pass_box = pygame.Rect(cx - box_w // 2, pass_y, box_w, box_h)
        border_color_p = (120, 180, 255) if self.active_field == FIELD_PASSWORD else (80, 80, 110)
        pygame.draw.rect(screen, (35, 35, 55), pass_box)
        pygame.draw.rect(screen, border_color_p, pass_box, 2)

        pass_display = "●" * len(self.password)
        if self.active_field == FIELD_PASSWORD and self.cursor_visible:
            pass_display += "|"
        pass_surf = self.input_font.render(pass_display, True, (255, 255, 255))
        screen.blit(pass_surf, pass_surf.get_rect(midleft=(pass_box.x + 12, pass_box.centery)))

        msg_y = cy + 100
        if self.mensaje_error:
            err = self.msg_font.render(self.mensaje_error, True, (255, 80, 80))
            screen.blit(err, err.get_rect(center=(cx, msg_y)))

        if self.mensaje_ok:
            ok = self.msg_font.render(self.mensaje_ok, True, (80, 255, 120))
            screen.blit(ok, ok.get_rect(center=(cx, msg_y)))

        hints = [
            "TAB to switch field",
            "ENTER to submit",
            "ESC to go back",
        ]
        hint_start = cy + 150
        for i, hint in enumerate(hints):
            line = self.hint_font.render(hint, True, (120, 120, 120))
            screen.blit(line, line.get_rect(center=(cx, hint_start + i * 24)))
