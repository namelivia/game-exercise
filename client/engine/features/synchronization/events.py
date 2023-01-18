from client.engine.primitives.event import Event


class UpdateGameEvent(Event):
    def __init__(self, events):
        super().__init__()
        self.events = events


class RefreshGameStatusEvent(Event):
    def __init__(self, game_id, pointer):
        super().__init__()
        self.game_id = game_id
        self.pointer = pointer


class RefreshGameStatusNetworkRequestEvent(Event):
    def __init__(self, game_id, pointer):
        super().__init__()
        self.game_id = game_id
        self.pointer = pointer
