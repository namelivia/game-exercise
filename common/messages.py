class PaginatedResponseMessage:
    def __init__(self, page, next_page):
        self.page = page
        self.next_page = next_page


class GameInfoMessage:
    def __init__(self, game):
        self.id = game.id
        self.name = game.name
        self.players = game.players


class GameEventsPageMessage(PaginatedResponseMessage):
    def __init__(self, page, next_page, events):
        super().__init__(page, next_page)
        self.events = events


class GameListPageMessage(PaginatedResponseMessage):
    def __init__(self, page, next_page, game_list):
        super().__init__(page, next_page)
        self.game_list = game_list


class CreateAGameMessage:
    def __init__(self, name, player_id):
        self.name = name
        self.player_id = player_id


class JoinAGameMessage:
    def __init__(self, game_id, player_id):
        self.game_id = game_id
        self.player_id = player_id


class PlaceASymbolMessage:
    def __init__(self, game_id, player_id, position):
        self.game_id = game_id
        self.player_id = player_id
        self.position = position


class SendChatMessage:
    def __init__(self, game_id, player_id, message):
        self.game_id = game_id
        self.player_id = player_id
        self.message = message


class ErrorMessage:
    def __init__(self, message):
        self.message = message


class GetGameEventsPage:
    def __init__(self, game_id, page, player_id):
        self.game_id = game_id
        self.page = page
        self.player_id = player_id


class PingRequestMessage:
    pass


class PingResponseMessage:
    pass


class GameListRequestMessage:
    pass


class GameListResponsePageMessage(PaginatedResponseMessage):
    def __init__(self, page, next_page, games):
        super().__init__(page, next_page)
        self.games = games


class GameListResponseEntry:
    def __init__(self, game):
        self.id = game.id
        self.name = game.name
