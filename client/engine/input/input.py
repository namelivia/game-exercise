from .input_manager import InputManager
from .text_input_manager import TextInputManager


class Input:
    def __init__(self, uses_pygame):
        if uses_pygame:
            self.manager = InputManager()
        else:
            self.manager = TextInputManager()

    def read(self):
        input_manager_events = self.manager.read()

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
        return [
            values_map[input_manager_event]
            for input_manager_event in input_manager_events
        ]
