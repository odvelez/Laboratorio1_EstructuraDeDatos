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

        self.title_font = pygame.font.Font(None, 64)
        self.info_font = pygame.font.Font(None, 36)
        self.pause_font = pygame.font.Font(None, 80)
        self.diff_label = config.dificultad_actual.upper()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.should_quit = True
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p and not self.game_over:
                    self.pausado = not self.pausado
                elif event.key == pygame.K_ESCAPE and not self.game_over:
                    self._guardar_y_salir()

    def update(self):
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
        screen.fill((18, 18, 25))

        player_rect = pygame.Rect(self.player_x, self.player_y, self.player_width, self.player_height)
        pygame.draw.rect(screen, (50, 120, 255), player_rect)

        for obstacle in self.obstacles:
            pygame.draw.rect(screen, (220, 60, 60), obstacle)

        score_text = self.info_font.render(f"SCORE: {self.score}", True, (230, 230, 230))
        screen.blit(score_text, (20, 20))

        diff_text = self.info_font.render(f"DIFF: {self.diff_label}", True, (180, 180, 180))
        screen.blit(diff_text, (screen.get_width() - diff_text.get_width() - 20, 20))

        jugador = player.jugador_actual
        if jugador:
            name_text = self.info_font.render(jugador.get_nombre(), True, (140, 200, 140))
            screen.blit(name_text, (20, 55))

        if self.pausado:
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 140))
            screen.blit(overlay, (0, 0))

            pause_text = self.pause_font.render("PAUSA", True, (255, 220, 0))
            hint_text = self.info_font.render("Press P to resume", True, (210, 210, 210))
            screen.blit(pause_text, pause_text.get_rect(center=(self.width // 2, self.height // 2 - 20)))
            screen.blit(hint_text, hint_text.get_rect(center=(self.width // 2, self.height // 2 + 30)))

        if self.game_over:
            game_over_text = self.title_font.render("GAME OVER", True, (255, 255, 255))
            score_final = self.info_font.render(f"Final Score: {self.score}", True, (235, 235, 235))
            restart_text = self.info_font.render("Returning to menu...", True, (200, 200, 200))
            go_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2 - 40))
            sf_rect = score_final.get_rect(center=(self.width // 2, self.height // 2 + 10))
            rt_rect = restart_text.get_rect(center=(self.width // 2, self.height // 2 + 50))
            screen.blit(game_over_text, go_rect)
            screen.blit(score_final, sf_rect)
            screen.blit(restart_text, rt_rect)

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
