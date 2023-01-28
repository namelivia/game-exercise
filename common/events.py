class GameCreated:
    def __init__(self, player_id: str):
        self.player_id = player_id


class PlayerJoined:
    def __init__(self, player_id: str):
        self.player_id = player_id


class PlayerPlacedSymbol:
    def __init__(self, event_id: str, player_id: str, position: int):
        self.event_id = event_id
        self.player_id = player_id
        self.position = position


class ChatMessageEvent:
    def __init__(self, event_id: str, player_id: str, message: str):
        self.event_id = event_id
        self.player_id = player_id
        self.message = message


class PlayerWins:
    def __init__(self, player_id: str):
        self.player_id = player_id
