from typing import List

from client.engine.foundational_wrapper import FoundationalWrapper


class KeyboardInput:
    def _get_key_value(self, event: any) -> str:
        special_keys = {
            FoundationalWrapper.K_RETURN: "return",
            FoundationalWrapper.K_ESCAPE: "escape",
            FoundationalWrapper.K_BACKSPACE: "backspace",
        }
        if event.key in special_keys:
            return special_keys[event.key]
        else:
            return event.unicode

    def read(self, events: List[any]) -> List[str]:
        keydowns = [
            event for event in events if event.type == FoundationalWrapper.KEYDOWN
        ]
        return [self._get_key_value(event) for event in keydowns]
