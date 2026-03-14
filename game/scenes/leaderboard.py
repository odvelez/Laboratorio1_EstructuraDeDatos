import pygame


class LeaderboardScene:
    def __init__(self):
        self.next_scene = None
        self.should_quit = False
        self.title_font = pygame.font.Font(None, 64)
        self.item_font = pygame.font.Font(None, 40)
        self.info_font = pygame.font.Font(None, 30)
        self.scores = [("Player1", 500), ("Player2", 420), ("Player3", 300)]

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.should_quit = True
                return

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                from scenes.menu import MenuScene

                self.next_scene = MenuScene()

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((15, 22, 35))

        title = self.title_font.render("TOP SCORES", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(screen.get_width() // 2, 100)))

        start_y = 200
        spacing = 55
        for index, (name, points) in enumerate(self.scores, start=1):
            line = self.item_font.render(f"{index}. {name}  {points}", True, (220, 220, 220))
            screen.blit(line, line.get_rect(center=(screen.get_width() // 2, start_y + (index - 1) * spacing)))

        hint = self.info_font.render("ESC to return", True, (200, 200, 200))
        screen.blit(hint, hint.get_rect(center=(screen.get_width() // 2, screen.get_height() - 40)))
