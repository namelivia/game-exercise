from typing import List

import pygame


class KeyboardManager:
    # Map pygame events to custom events
    def read(self) -> List[str]:
        mapping = {
            pygame.KEYDOWN: {
                pygame.K_1: "event_1",
                pygame.K_2: "event_2",
                pygame.K_3: "event_3",
                pygame.K_4: "event_4",
                pygame.K_5: "event_5",
                pygame.K_6: "event_6",
                pygame.K_7: "event_7",
                pygame.K_8: "event_8",
                pygame.K_9: "event_9",
                pygame.K_0: "event_0",
                pygame.K_a: "event_a",
                pygame.K_b: "event_b",
                pygame.K_c: "event_c",
                pygame.K_d: "event_d",
                pygame.K_e: "event_e",
                pygame.K_f: "event_f",
                pygame.K_g: "event_g",
                pygame.K_h: "event_h",
                pygame.K_i: "event_i",
                pygame.K_j: "event_j",
                pygame.K_k: "event_k",
                pygame.K_l: "event_l",
                pygame.K_m: "event_m",
                pygame.K_n: "event_n",
                pygame.K_o: "event_o",
                pygame.K_p: "event_p",
                pygame.K_q: "event_q",
                pygame.K_r: "event_r",
                pygame.K_s: "event_s",
                pygame.K_t: "event_t",
                pygame.K_u: "event_u",
                pygame.K_v: "event_v",
                pygame.K_w: "event_w",
                pygame.K_x: "event_x",
                pygame.K_y: "event_y",
                pygame.K_z: "event_z",
                pygame.K_RETURN: "event_return",
                pygame.K_ESCAPE: "event_escape",
                pygame.K_BACKSPACE: "event_backspace",
                pygame.K_SPACE: "event_space",
                pygame.K_MINUS: "event_minus",
            }
        }

        events = pygame.event.get()
        result = []
        if events is not None and len(events) > 0:
            for event in events:
                try:
                    result.append(mapping[event.type][event.key])
                except KeyError:
                    pass  # Ignore events not mapped
        return result
