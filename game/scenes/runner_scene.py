import random

import pygame

import config
from crud import player


class RunnerScene:
    def __init__(self):
        self.next_scene = None
        self.should_quit = False

        cfg = config.config_dificultad[config.dificultad_actual]

        self.width = 800
        self.height = 600
        self.player_width = 60
        self.player_height = 20
        self.player_x = (self.width - self.player_width) // 2
        self.player_y = self.height - 60
        self.player_speed = cfg["velocidad_juego"]

        self.obstacles = []
        self.obstacle_width = 80
        self.obstacle_height = 80
        self.spawn_interval = cfg["spawn_obstaculos"]
        self.spawn_counter = 0
        self.speed = cfg["velocidad_obstaculos"]
        self.score = 0

        self.pausado = False
        self.game_over = False
        self.game_over_counter = 0
        self.game_over_wait_frames = 120
        self.score_saved = False
        self.restart_rect = pygame.Rect(0, 0, 0, 0)

        self.title_font = pygame.font.Font(None, 64)
        self.info_font = pygame.font.Font(None, 36)
        self.pause_font = pygame.font.Font(None, 80)
        self.diff_label = config.dificultad_actual.upper()

    def _sync_screen_size(self):
        display_surface = pygame.display.get_surface()
        if display_surface is None:
            return

        self.width, self.height = display_surface.get_size()
        self.player_y = self.height - 60
        self.player_x = max(0, min(self.player_x, self.width - self.player_width))

    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()

        for event in events:
            if event.type == pygame.QUIT:
                self.should_quit = True
                return

            if event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key in (pygame.K_RETURN, pygame.K_r, pygame.K_SPACE):
                        from scenes.runner_scene import RunnerScene

                        self.next_scene = RunnerScene()
                        return
                else:
                    if event.key == pygame.K_p:
                        self.pausado = not self.pausado
                    elif event.key == pygame.K_ESCAPE:
                        self._guardar_y_salir()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.game_over:
                if self.restart_rect.collidepoint(mouse_pos):
                    from scenes.runner_scene import RunnerScene

                    self.next_scene = RunnerScene()
                    return

    def update(self):
        self._sync_screen_size()

        if self.pausado:
            return

        if self.game_over:
            self.game_over_counter += 1
            if self.game_over_counter >= self.game_over_wait_frames:
                from scenes.menu import MenuScene

                self.next_scene = MenuScene()
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player_x -= self.player_speed
        if keys[pygame.K_RIGHT]:
            self.player_x += self.player_speed

        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:
            mouse_x = pygame.mouse.get_pos()[0]
            self.player_x = mouse_x - self.player_width // 2

        self.player_x = max(0, min(self.player_x, self.width - self.player_width))

        self.spawn_counter += 1
        if self.spawn_counter >= self.spawn_interval:
            self.spawn_counter = 0
            obstacle_x = random.randint(0, self.width - self.obstacle_width)
            self.obstacles.append(
                pygame.Rect(obstacle_x, -self.obstacle_height, self.obstacle_width, self.obstacle_height)
            )

        for obstacle in self.obstacles:
            obstacle.y += self.speed

        self.obstacles = [obs for obs in self.obstacles if obs.y < self.height + self.obstacle_height]
        self.score += 1

        player_rect = pygame.Rect(self.player_x, self.player_y, self.player_width, self.player_height)
        for obstacle in self.obstacles:
            if player_rect.colliderect(obstacle):
                self.game_over = True
                self._registrar_score()
                break

    def draw(self, screen):
        self._sync_screen_size()
        screen.fill((5, 5, 20))

        w, h = screen.get_size()
        tile = 40
        t = pygame.time.get_ticks() // 25
        for x in range(-tile, w + tile, tile):
            for y in range(-tile, h + tile, tile):
                phase = ((x // tile) + (y // tile) + (t // 4)) % 2
                col = (20, 18, 60) if phase == 0 else (12, 10, 40)
                rect = pygame.Rect(x + (t % tile), y, tile - 2, tile - 2)
                pygame.draw.rect(screen, col, rect, 0, border_radius=4)

        ground_y = self.height - 40
        pygame.draw.rect(screen, (15, 8, 35), (0, ground_y, w, 40))
        pygame.draw.rect(screen, (80, 255, 180), (0, ground_y, w, 4))

        player_rect = pygame.Rect(self.player_x, self.player_y, self.player_width, self.player_height)
        pygame.draw.rect(screen, (0, 240, 200), player_rect, border_radius=4)
        pygame.draw.rect(screen, (255, 255, 255), player_rect, 2, border_radius=4)

        for obstacle in self.obstacles:
            o_rect = pygame.Rect(obstacle.x, obstacle.y, obstacle.width, obstacle.height)
            pygame.draw.rect(screen, (255, 80, 80), o_rect, border_radius=6)
            pygame.draw.rect(screen, (255, 255, 255), o_rect, 2, border_radius=6)

        score_text = self.info_font.render(f"SCORE: {self.score}", True, (240, 240, 240))
        screen.blit(score_text, (20, 15))

        diff_text = self.info_font.render(f"DIFF: {self.diff_label}", True, (190, 190, 210))
        screen.blit(diff_text, (screen.get_width() - diff_text.get_width() - 20, 15))

        jugador = player.jugador_actual
        if jugador:
            name_text = self.info_font.render(jugador.get_nombre(), True, (180, 255, 210))
            screen.blit(name_text, (20, 50))

        if self.pausado:
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 140))
            screen.blit(overlay, (0, 0))

            pause_text = self.pause_font.render("PAUSE", True, (255, 255, 255))
            hint_text = self.info_font.render("Press P to resume", True, (220, 220, 240))
            screen.blit(pause_text, pause_text.get_rect(center=(self.width // 2, self.height // 2 - 20)))
            screen.blit(hint_text, hint_text.get_rect(center=(self.width // 2, self.height // 2 + 30)))

        if self.game_over:
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))

            game_over_text = self.title_font.render("GAME OVER", True, (255, 255, 255))
            score_final = self.info_font.render(f"Final Score: {self.score}", True, (235, 235, 235))
            restart_text = self.info_font.render("Press R / ENTER to restart", True, (200, 200, 200))
            menu_text = self.info_font.render("Returning to menu shortly...", True, (180, 180, 200))
            go_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2 - 70))
            sf_rect = score_final.get_rect(center=(self.width // 2, self.height // 2 - 20))
            rt_rect = restart_text.get_rect(center=(self.width // 2, self.height // 2 + 25))
            mt_rect = menu_text.get_rect(center=(self.width // 2, self.height // 2 + 60))
            screen.blit(game_over_text, go_rect)
            screen.blit(score_final, sf_rect)
            screen.blit(restart_text, rt_rect)
            screen.blit(menu_text, mt_rect)

            btn_w, btn_h = 220, 48
            btn_rect = pygame.Rect(0, 0, btn_w, btn_h)
            btn_rect.center = (self.width // 2, self.height // 2 + 110)
            pygame.draw.rect(screen, (40, 220, 140), btn_rect, border_radius=10)
            pygame.draw.rect(screen, (255, 255, 255), btn_rect, 2, border_radius=10)
            btn_label = self.info_font.render("RESTART", True, (10, 10, 10))
            screen.blit(btn_label, btn_label.get_rect(center=btn_rect.center))
            self.restart_rect = btn_rect

    def _registrar_score(self):
        if self.score_saved:
            return
        self.score_saved = True

        mgr = player.get_manager()
        mgr.registrar_intento(self.score, config.dificultad_actual)

    def _guardar_y_salir(self):
        self._registrar_score()
        from scenes.menu import MenuScene

        self.next_scene = MenuScene()
