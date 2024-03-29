from typing import List

import pygame


class KeyboardInput:
    def __init__(self, uses_pygame: bool):
        if uses_pygame:
            pass

    def _get_key_value(self, event: pygame.event) -> str:
        special_keys = {
            pygame.K_RETURN: "return",
            pygame.K_ESCAPE: "escape",
            pygame.K_BACKSPACE: "backspace",
        }
        if event.key in special_keys:
            return special_keys[event.key]
        else:
            return event.unicode

    def read(self, events: List[pygame.event]) -> List[str]:
        keydowns = [event for event in events if event.type == pygame.KEYDOWN]
        return [self._get_key_value(event) for event in keydowns]
