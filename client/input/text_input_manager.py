class TextInputManager:
    def read(self):

        mapping = {
            "1": "event_1",
            "2": "event_2",
            "3": "event_2",
            "4": "event_2",
            "5": "event_5",
            "6": "event_6",
            "7": "event_7",
            "8": "event_8",
            "9": "event_9",
            "0": "event_0",
            "a": "event_a",
            "b": "event_b",
            "c": "event_c",
            "d": "event_d",
            "e": "event_e",
            "f": "event_f",
            "g": "event_g",
            "h": "event_h",
            "i": "event_i",
            "j": "event_j",
            "k": "event_k",
            "l": "event_l",
            "m": "event_m",
            "n": "event_n",
            "o": "event_o",
            "p": "event_p",
            "q": "event_q",
            "r": "event_r",
            "s": "event_s",
            "t": "event_t",
            "u": "event_u",
            "v": "event_v",
            "w": "event_w",
            "x": "event_x",
            "y": "event_y",
            "z": "event_z",
            "enter": "event_return",
            "escape": "event_escape",
            "backspace": "event_backspace",
            "space": "event_space",
            "-": "event_minus",
        }
        user_input = input("Write the key you would like to press:")
        try:
            return [mapping[user_input]]
        except KeyError:
            print("Input not recognized")
            return []
