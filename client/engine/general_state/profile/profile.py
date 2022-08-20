from client.engine.persistence.persistence import Persistence


class Profile:
    def __init__(self, *, id, game_id, game_event_pointer, sound_on):
        self.id = id
        self.game_id = game_id
        self.game_event_pointer = game_event_pointer
        self.sound_on = sound_on
        self.name = None

    def set_game(self, game_id):
        self.game_id = game_id

    def set_name(self, name):
        self.name = name

    def set_game_event_pointer(self, game_event_pointer):
        self.game_event_pointer = game_event_pointer

    def set_sound_on(self):
        self.sound_on = True
        self.save()

    def set_sound_off(self):
        self.sound_on = False
        self.save()

    def save(self):
        Persistence.save(self)
