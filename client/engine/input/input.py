from typing import Dict, List

from .keyboard_manager import KeyboardManager
from .mouse_manager import MouseManager


class Input:
    def __init__(self, uses_pygame: bool):
        if uses_pygame:
            self.keyboard = KeyboardManager()
            self.mouse = MouseManager()

    def read(self) -> Dict[str, List[str]]:
        keyboard_events = self.keyboard.read()
        mouse_events = self.keyboard.read()

        # This translates the normalized event names (needed for both text input and regular input)
        # into the normally corresponding value for the key.
        # This could be replaced for "something" that would tell corresponding value for the key
        # just if needed.
        values_map = {
            "event_1": "1",
            "event_2": "2",
            "event_3": "3",
            "event_4": "4",
            "event_5": "5",
            "event_6": "6",
            "event_7": "7",
            "event_8": "8",
            "event_9": "9",
            "event_0": "0",
            "event_a": "a",
            "event_b": "b",
            "event_c": "c",
            "event_d": "d",
            "event_e": "e",
            "event_f": "f",
            "event_g": "g",
            "event_h": "h",
            "event_i": "i",
            "event_j": "j",
            "event_k": "k",
            "event_l": "l",
            "event_m": "m",
            "event_n": "n",
            "event_o": "o",
            "event_p": "p",
            "event_q": "q",
            "event_r": "r",
            "event_s": "s",
            "event_t": "t",
            "event_u": "u",
            "event_v": "v",
            "event_w": "w",
            "event_x": "x",
            "event_y": "y",
            "event_z": "z",
            "event_return": "return",
            "event_escape": "escape",
            "event_backspace": "backspace",
            "event_space": " ",
            "event_minus": "-",
        }
        return {
            "keyboard": [
                values_map[keyboard_event] for keyboard_event in keyboard_events
            ],
            "mouse": [],
        }
