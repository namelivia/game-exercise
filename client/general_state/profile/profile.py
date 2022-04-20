class Profile:
    def __init__(self, id, name, game_id, game_event_pointer):
        self.id = id
        self.name = name
        self.game_id = game_id
        self.game_event_pointer = game_event_pointer

    def set_game(self, game_id):
        self.game_id = game_id

    def set_game_event_pointer(self, game_event_pointer):
        self.game_event_pointer = game_event_pointer
