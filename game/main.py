import os
import sys

_GAME_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_GAME_DIR)
sys.path.insert(0, _GAME_DIR)
sys.path.insert(0, _PROJECT_ROOT)

import pygame

from scenes.login import LoginScene

WINDOWED_SIZE = (800, 600)


def main():
    pygame.init()

    screen = pygame.display.set_mode(WINDOWED_SIZE)
    pygame.display.set_caption("Laboratorio 1 - Escenas")
    clock = pygame.time.Clock()

    current_scene = LoginScene()
    running = True

    while running:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                flags = screen.get_flags()
                if flags & pygame.FULLSCREEN:
                    screen = pygame.display.set_mode(WINDOWED_SIZE)
                else:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        current_scene.handle_events(events)
        current_scene.update()
        current_scene.draw(screen)
        pygame.display.flip()

        if current_scene.next_scene is not None:
            current_scene = current_scene.next_scene
        elif getattr(current_scene, "should_quit", False):
            running = False

        screen = pygame.display.get_surface()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
