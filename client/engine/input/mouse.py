from typing import Any, List, Optional

import pygame


class MouseInput:
    def __init__(self, uses_pygame: bool):
        if uses_pygame:
            pass

    def read(self, events: List[pygame.event]) -> Optional[List[int]]:
        if pygame.MOUSEBUTTONDOWN in [event.type for event in events]:
            return "click"
        return None
