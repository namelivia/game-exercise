import pygame


class InputManager():

    # Map pygame events to custom events
    def read(self):

        mapping = {pygame.KEYDOWN: {
            pygame.K_1: "event_1",
            pygame.K_2: "event_2",
        }}

        events = pygame.event.get()
        result = []
        if events is not None and len(events) > 0:
            for event in events:
                try:
                    result.append(mapping[event.type][event.key])
                except KeyError:
                    pass  # Ignore events not mapped
        return result
