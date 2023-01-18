from client.engine.primitives.event import Event


class NewGameRequestEvent(Event):
    def __init__(self, new_game_name):
        super().__init__()
        self.new_game_name = new_game_name


class JoinExistingGameEvent(Event):
    def __init__(self, game_id):
        super().__init__()
        self.game_id = game_id


class CreateAGameNetworkRequestEvent(Event):
    def __init__(self, new_game_name):
        super().__init__()
        self.new_game_name = new_game_name


class JoinAGameNetworkRequestEvent(Event):
    def __init__(self, game_id):
        super().__init__()
        self.game_id = game_id


class ErrorCreatingGameEvent(Event):
    pass


class ErrorJoiningGameEvent(Event):
    pass
