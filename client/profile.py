import uuid


class Profile():
    def __init__(self, name):
        self.id = uuid.uuid4()
        self.name = name
        self.game_id = None

    def set_game(self, game_id):
        self.game_id = game_id
