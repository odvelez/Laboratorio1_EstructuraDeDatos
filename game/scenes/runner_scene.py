import random
import pygame


class RunnerScene:
    def __init__(self):
        self.next_scene = None
        self.should_quit = False

        self.width = 800
        self.height = 600
        self.player_width = 60
        self.player_height = 20
        self.player_x = (self.width - self.player_width) // 2
        self.player_y = self.height - 60
        self.player_speed = 7

        self.obstacles = []
        self.obstacle_width = 40
        self.obstacle_height = 40
        self.spawn_interval = 45
        self.spawn_counter = 0
        self.speed = 5
        self.score = 0

        self.game_over = False
        self.game_over_counter = 0
        self.game_over_wait_frames = 120

        self.title_font = pygame.font.Font(None, 64)
        self.info_font = pygame.font.Font(None, 36)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.should_quit = True
                return

    def update(self):
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
                break

    def draw(self, screen):
        screen.fill((18, 18, 25))

        player_rect = pygame.Rect(self.player_x, self.player_y, self.player_width, self.player_height)
        pygame.draw.rect(screen, (50, 120, 255), player_rect)

        for obstacle in self.obstacles:
            pygame.draw.rect(screen, (220, 60, 60), obstacle)

        score_text = self.info_font.render(f"SCORE: {self.score}", True, (230, 230, 230))
        screen.blit(score_text, (20, 20))

        if self.game_over:
            game_over_text = self.title_font.render("GAME OVER", True, (255, 255, 255))
            restart_text = self.info_font.render("Returning to menu...", True, (235, 235, 235))
            go_rect = game_over_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 20))
            rt_rect = restart_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 30))
            screen.blit(game_over_text, go_rect)
            screen.blit(restart_text, rt_rect)