class GameCreated:
    def __init__(self, player_id):
        self.player_id = player_id


class PlayerJoined:
    def __init__(self, player_id):
        self.player_id = player_id


class PlayerPlacedSymbol:
    def __init__(self, player_id, position):
        self.player_id = player_id
        self.position = position
