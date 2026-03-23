import os

import pygame


AUDIO_DIR = os.path.join(os.path.dirname(__file__), "audio")
SUPPORTED_AUDIO_EXTENSIONS = (
    ".ogg",
    ".mp3",
    ".wav",
    ".flac",
    ".mid",
    ".midi",
    ".mp4",
)

_initialized = False
_current_track = None


def init_audio():
    global _initialized
    if _initialized:
        return True

    try:
        if pygame.mixer.get_init() is None:
            pygame.mixer.init()
        _initialized = True
        return True
    except pygame.error:
        _initialized = False
        return False


def _find_first_track():
    if not os.path.isdir(AUDIO_DIR):
        return None

    files = sorted(os.listdir(AUDIO_DIR))
    for filename in files:
        _, ext = os.path.splitext(filename)
        if ext.lower() in SUPPORTED_AUDIO_EXTENSIONS:
            return os.path.join(AUDIO_DIR, filename)
    return None


def load_and_play_music(loop=-1):
    global _current_track

    if not init_audio():
        return False

    track_path = _find_first_track()
    if track_path is None:
        return False

    try:
        pygame.mixer.music.load(track_path)
        pygame.mixer.music.play(loop)
        _current_track = track_path
        return True
    except pygame.error:
        _current_track = None
        return False


def set_volume_from_level(level):
    if not init_audio():
        return

    value = max(0, min(int(level), 10))
    pygame.mixer.music.set_volume(value / 10.0)


def get_current_track():
    return _current_track
