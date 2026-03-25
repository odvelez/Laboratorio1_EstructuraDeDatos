import pygame

import config
from crud import player
from scenes.settings import WINDOWED_SIZE

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
        elif self.mode == MODE_LOGIN:
            jugador, error = mgr.login_user(username, password)
            if error:
                self.mensaje_error = error
                return
            mgr.set_jugador_actual(jugador)

        # Aplicar configuraciones guardadas del jugador (dificultad, fullscreen)
        if jugador is not None:
            settings = getattr(jugador, "settings", {})
            dif = settings.get("difficulty")
            if dif in config.dificultades:
                config.dificultad_actual = dif

            fullscreen_pref = settings.get("fullscreen", False)
            if fullscreen_pref:
                pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            else:
                pygame.display.set_mode(WINDOWED_SIZE)

        from scenes.menu import MenuScene
        self.next_scene = MenuScene()

    def update(self):
        self.cursor_timer += 1
        if self.cursor_timer >= 30:
            self.cursor_timer = 0
            self.cursor_visible = not self.cursor_visible

    def draw(self, screen):
        w, h = screen.get_size()
        cx = w // 2

        screen.fill((6, 4, 18))
        tile = 32
        t = pygame.time.get_ticks() // 25
        for x in range(-tile, w + tile, tile):
            for y in range(-tile, h + tile, tile):
                phase = ((x + y + t) // tile) % 2
                color = (25, 18, 60) if phase == 0 else (18, 10, 40)
                rect = pygame.Rect(int(x), int(y), int(tile - 2), int(tile - 2))
                pygame.draw.rect(screen, color, rect, 0, border_radius=4)

        if self.state == STATE_SELECT:
            self._draw_select(screen, cx)
        elif self.state == STATE_INPUT:
            self._draw_input(screen, cx)

    def _draw_select(self, screen, cx):
        h = screen.get_height()
        cy = h // 2

        card = pygame.Rect(0, 0, 420, 220)
        card.center = (cx, cy - 10)
        pygame.draw.rect(screen, (20, 14, 60), card, border_radius=18)
        pygame.draw.rect(screen, (120, 90, 255), card, 3, border_radius=18)

        title = self.title_font.render("WELCOME", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(cx, card.top + 55)))

        self.option_rects.clear()
        spacing = 70
        start_y = card.top + 110
        for i, option in enumerate(self.menu_options):
            is_selected = i == self.menu_index
            btn_rect = pygame.Rect(0, 0, card.width - 80, 44)
            btn_rect.center = (cx, start_y + i * spacing)
            bg = (40, 220, 140) if is_selected else (35, 24, 80)
            border = (255, 255, 255) if is_selected else (160, 140, 255)
            pygame.draw.rect(screen, bg, btn_rect, border_radius=12)
            pygame.draw.rect(screen, border, btn_rect, 2, border_radius=12)

            label_color = (10, 10, 10) if is_selected else (230, 230, 230)
            text = self.option_font.render(option, True, label_color)
            screen.blit(text, text.get_rect(center=btn_rect.center))
            self.option_rects.append(btn_rect)

        hint = self.hint_font.render("ESC to quit", True, (160, 160, 190))
        screen.blit(hint, hint.get_rect(center=(cx, h - 35)))

    def _draw_input(self, screen, cx):
        h = screen.get_height()
        cy = h // 2

        card = pygame.Rect(0, 0, 520, 360)
        card.center = (cx, cy)
        pygame.draw.rect(screen, (18, 10, 45), card, border_radius=20)
        pygame.draw.rect(screen, (90, 255, 200), card, 3, border_radius=20)

        mode_label = "REGISTER" if self.mode == MODE_REGISTER else "LOGIN"
        title = self.title_font.render(mode_label, True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(cx, card.top + 45)))

        box_w, box_h = 360, 44
        user_y = card.top + 110
        pass_y = card.top + 195

        user_label = self.label_font.render("Username", True, (170, 210, 255))
        screen.blit(user_label, user_label.get_rect(midleft=(cx - box_w // 2, user_y - 26)))

        user_box = pygame.Rect(cx - box_w // 2, user_y, box_w, box_h)
        border_color_u = (120, 220, 255) if self.active_field == FIELD_USERNAME else (70, 80, 120)
        pygame.draw.rect(screen, (28, 20, 70), user_box, border_radius=10)
        pygame.draw.rect(screen, border_color_u, user_box, 2, border_radius=10)

        user_display = self.username
        if self.active_field == FIELD_USERNAME and self.cursor_visible:
            user_display += "|"
        user_surf = self.input_font.render(user_display, True, (255, 255, 255))
        screen.blit(user_surf, user_surf.get_rect(midleft=(user_box.x + 12, user_box.centery)))

        pass_label = self.label_font.render("Password", True, (170, 210, 255))
        screen.blit(pass_label, pass_label.get_rect(midleft=(cx - box_w // 2, pass_y - 26)))

        pass_box = pygame.Rect(cx - box_w // 2, pass_y, box_w, box_h)
        border_color_p = (120, 220, 255) if self.active_field == FIELD_PASSWORD else (70, 80, 120)
        pygame.draw.rect(screen, (28, 20, 70), pass_box, border_radius=10)
        pygame.draw.rect(screen, border_color_p, pass_box, 2, border_radius=10)

        pass_display = "●" * len(self.password)
        if self.active_field == FIELD_PASSWORD and self.cursor_visible:
            pass_display += "|"
        pass_surf = self.input_font.render(pass_display, True, (255, 255, 255))
        screen.blit(pass_surf, pass_surf.get_rect(midleft=(pass_box.x + 12, pass_box.centery)))

        msg_y = card.bottom - 90
        if self.mensaje_error:
            err = self.msg_font.render(self.mensaje_error, True, (255, 80, 80))
            screen.blit(err, err.get_rect(center=(cx, msg_y)))

        if self.mensaje_ok:
            ok = self.msg_font.render(self.mensaje_ok, True, (80, 255, 120))
            screen.blit(ok, ok.get_rect(center=(cx, msg_y)))

        hints = [
            "TAB  switch field",
            "ENTER  submit",
            "ESC  back",
        ]
        hint_start = card.bottom - 40
        for i, hint in enumerate(hints):
            line = self.hint_font.render(hint, True, (150, 150, 190))
            screen.blit(line, line.get_rect(center=(cx, hint_start + i * 20)))
