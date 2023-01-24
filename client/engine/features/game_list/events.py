from client.engine.primitives.event import Event, InGameEvent


class UpdateGameListEvent(InGameEvent):
    def __init__(self, games):
        super().__init__()
        self.games = games


class GetGameListNetworkRequestEvent(Event):
    pass


class ErrorGettingGameListEvent(Event):
    pass