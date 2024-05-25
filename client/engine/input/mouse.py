from typing import Any, List, Optional

import pygame


class MouseInput:
    def read(self, events: List[pygame.event]) -> Optional[List[int]]:
        if pygame.MOUSEBUTTONDOWN in [event.type for event in events]:
            return "click"
        return None
