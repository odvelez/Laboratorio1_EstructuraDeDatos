import pygame
import sys

from crud import player


class MenuScene:
    def __init__(self):
        self.options = ["START GAME", "LEADERBOARD", "HASH TABLE", "SETTINGS", "LOG OUT", "EXIT"]
        self.selected_index = 0
        self.next_scene = None
        self.should_quit = False
        self.title_font = pygame.font.Font(None, 64)
        self.option_font = pygame.font.Font(None, 40)
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
                    self._select_option()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for rect_index, rect in enumerate(self.option_rects):
                    if rect.collidepoint(mouse_pos):
                        self.selected_index = rect_index
                        self._select_option()
                        break

    def _select_option(self):
        option = self.options[self.selected_index]

        if option == "START GAME":
            from scenes.runner_scene import RunnerScene

            self.next_scene = RunnerScene()
        elif option == "LEADERBOARD":
            from scenes.leaderboard import LeaderboardScene

            self.next_scene = LeaderboardScene()
        elif option == "HASH TABLE":
            from scenes.hashtable_scene import HashTableScene

            self.next_scene = HashTableScene()
        elif option == "SETTINGS":
            from scenes.settings import SettingsScene

            self.next_scene = SettingsScene()
        elif option == "LOG OUT":
            from scenes.login import LoginScene

            player.jugador_actual = None
            self.next_scene = LoginScene()
        elif option == "EXIT":
            self.should_quit = True
            pygame.quit()
            sys.exit()

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((20, 20, 20))
        w, h = screen.get_size()
        cx = w // 2
        cy = h // 2

        title_text = self.title_font.render("MAIN MENU", True, (255, 255, 255))
        screen.blit(title_text, title_text.get_rect(center=(cx, cy - 170)))

        jugador = player.jugador_actual
        if jugador:
            info = self.info_font.render(
                f"Player: {jugador.get_nombre()}  |  Best: {jugador.get_max_score()}",
                True,
                (160, 220, 160),
            )
            screen.blit(info, info.get_rect(center=(cx, cy - 110)))

        self.option_rects.clear()
        spacing = 50
        block_height = (len(self.options) - 1) * spacing
        start_y = cy - block_height // 2
        for index, option in enumerate(self.options):
            color = (255, 220, 0) if index == self.selected_index else (210, 210, 210)
            option_text = self.option_font.render(option, True, color)
            option_rect = option_text.get_rect(center=(cx, start_y + index * spacing))
            self.option_rects.append(option_rect)
            screen.blit(option_text, option_rect)