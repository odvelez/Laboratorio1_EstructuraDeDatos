"""
Punto de entrada del juego. Compatible con escritorio y con pygbag (WebAssembly).

Para web: instala pygame-ce y pygbag, luego desde esta carpeta `game`:
pygbag .
"""
import asyncio
import os
import sys

_GAME_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_GAME_DIR)
sys.path.insert(0, _GAME_DIR)
sys.path.insert(0, _PROJECT_ROOT)

import pygame

import audio_manager
import backend
from crud import player
from scenes.login import LoginScene

WINDOWED_SIZE = (800, 600)


async def main():
    pygame.init()

    backend.get_persistence()

    screen = pygame.display.set_mode(WINDOWED_SIZE)
    pygame.display.set_caption("Laboratorio 1 - Escenas")
    clock = pygame.time.Clock()
    audio_manager.load_and_play_music()
    applied_volume = None

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

        current_player = player.jugador_actual
        target_volume = 5
        if current_player is not None:
            target_volume = current_player.settings.get("volume", 5)
        if target_volume != applied_volume:
            audio_manager.set_volume_from_level(target_volume)
            applied_volume = target_volume

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
        # Necesario para pygbag: cede el control al runtime WASM cada frame
        await asyncio.sleep(0)

    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
