import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pygame

from scenes.login import LoginScene


def main():
    pygame.init()

    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Laboratorio 1 - Escenas")
    clock = pygame.time.Clock()

    current_scene = LoginScene()
    running = True

    while running:
        events = pygame.event.get()

        current_scene.handle_events(events)
        current_scene.update()
        current_scene.draw(screen)
        pygame.display.flip()

        if current_scene.next_scene is not None:
            current_scene = current_scene.next_scene
        elif getattr(current_scene, "should_quit", False):
            running = False

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
