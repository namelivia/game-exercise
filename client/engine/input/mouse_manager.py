from typing import List

import pygame


class MouseManager:
    # Map pygame events to custom events
    def read(self) -> List[str]:
        events = pygame.event.get()
        return []
