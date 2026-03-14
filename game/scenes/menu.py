import pygame
import sys


class MenuScene:
    def __init__(self):
        self.options = ["START GAME", "LEADERBOARD", "SETTINGS", "EXIT"]
        self.selected_index = 0
        self.next_scene = None
        self.should_quit = False
        self.title_font = pygame.font.Font(None, 64)
        self.option_font = pygame.font.Font(None, 40)

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
                    self._select_option()

    def _select_option(self):
        option = self.options[self.selected_index]

        if option == "START GAME":
            from scenes.runner_scene import RunnerScene

            self.next_scene = RunnerScene()
        elif option == "LEADERBOARD":
            from scenes.leaderboard import LeaderboardScene

            self.next_scene = LeaderboardScene()
        elif option == "SETTINGS":
            from scenes.settings import SettingsScene

            self.next_scene = SettingsScene()
        elif option == "EXIT":
            self.should_quit = True
            pygame.quit()
            sys.exit()

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((20, 20, 20))

        title_text = self.title_font.render("MAIN MENU", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(screen.get_width() // 2, 110))
        screen.blit(title_text, title_rect)

        start_y = 220
        spacing = 55
        for index, option in enumerate(self.options):
            color = (255, 220, 0) if index == self.selected_index else (210, 210, 210)
            option_text = self.option_font.render(option, True, color)
            option_rect = option_text.get_rect(center=(screen.get_width() // 2, start_y + index * spacing))
            screen.blit(option_text, option_rect)
