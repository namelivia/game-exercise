from abc import ABC
# from .game import Game
from client.game_specific.ui import (
    WelcomeMessage,
    NewGameMessage,
    OptionList,
    # ClockUI,
    Title,
    GameIdMessage,
    TurnIndicator,
    GameIdIndicator,
    GameNameIndicator,
    Player1NameIndicator,
    Player2NameIndicator,
    Board,
    Instructions,
)
from client.game_specific.events import UserTypedEvent

# This should be the definition of the different states


class Screen(ABC):

    def __init__(self, client_state, graphics):
        self.client_state = client_state
        self.graphics = graphics
        # For pygame
        self.ui_elements = []

    def get_ui_elements(self):
        return self.ui_elements

    def render(self):
        self.graphics.render(self)  # Tell graphics to draw current screen

    def update(self, event):
        pass


class Intro(Screen):

    def __init__(self, client_state, window):
        super().__init__(client_state, window)

        self.data = {
            "time": client_state.clock.get()
        }

        self.ui_elements = [
            # ClockUI(self.data['time']),
            Title(self.data['time']),
        ]

    def update(self, event):
        # And now here I can update the screen-specific data
        # for example the time.
        self.data['time'] = self.client_state.clock.get()

        if (self.data['time'] > 30000):  # TODO: This should be relative time
            from client.game_specific.commands import (
                BackToLobby
            )
            BackToLobby(
                self.client_state.profile,
                self.client_state.queue
            ).execute()

        if event is not None:
            if isinstance(event, UserTypedEvent):
                if event.key == "escape" or event.key == "return":
                    # Avoid circular import
                    from client.game_specific.commands import (
                        BackToLobby
                    )
                    BackToLobby(
                        self.client_state.profile,
                        self.client_state.queue
                    ).execute()

        # Update ui elements (They need to access the data to do so)
        [element.update(self.data) for element in self.ui_elements]


class Lobby(Screen):

    def __init__(self, client_state, window):
        super().__init__(client_state, window)

        # I think I need some kind of screen dependant set of data
        # for example here I could store the name and the clock value, this data is meant to be displayed.
        # The clock could be relative too. Maybe the strings to be displayed could be stored here too.
        # This data can be initialized and updated per cycle (time).
        self.data = {
            "name": client_state.profile.name,
            "time": client_state.clock.get()
        }

        # This is the graphical representation (pure graphical description). Only for pygame
        self.ui_elements = [
            # ClockUI(self.data['time']),
            WelcomeMessage(self.data['name']),
            OptionList({
                "1": "Create a new game",
                "2": "Join an existing game"
            })
        ]

    def update(self, event):
        # And now here I can update the screen-specific data
        # for example the time.
        self.data['time'] = self.client_state.clock.get()

        if event is not None:
            if isinstance(event, UserTypedEvent):
                # Avoid circular import
                # Could these be not just game specific but screen specific?
                from client.game_specific.commands import (
                    NewGame,
                    GoToJoinAGame,
                    QuitGame
                )
                # These actions, some may update the data, others run commands, who knows
                key = event.key
                if key == "1":
                    NewGame(
                        self.client_state.profile,
                        self.client_state.queue
                    ).execute()
                if key == "2":
                    GoToJoinAGame(
                        self.client_state.profile,
                        self.client_state.queue
                    ).execute()
                if event.key == "escape":
                    QuitGame(
                        self.client_state.profile,
                        self.client_state.queue
                    ).execute()

        # Update ui elements (They need to access the data to do so)
        [element.update(self.data) for element in self.ui_elements]


class NewGameScreen(Screen):

    def __init__(self, client_state, window):
        super().__init__(client_state, window)

        self.data = {
            "time": client_state.clock.get(),
            "new_game_name": ""
        }

        self.ui_elements = [
            # ClockUI(self.data['time']),
            NewGameMessage(self.data['new_game_name']),
        ]

    def update(self, event):
        # And now here I can update the screen-specific data
        # for example the time.
        self.data['time'] = self.client_state.clock.get()

        if event is not None:
            if isinstance(event, UserTypedEvent):
                if event.key == "escape":
                    # Avoid circular import
                    from client.game_specific.commands import (
                        BackToLobby
                    )
                    BackToLobby(
                        self.client_state.profile,
                        self.client_state.queue
                    ).execute()
                if event.key == "return":
                    # Avoid circular import
                    from client.game_specific.commands import (
                        RequestGameCreation
                    )
                    RequestGameCreation(
                        self.client_state.profile,
                        self.client_state.queue,
                        self.data["new_game_name"]
                    ).execute()
                if event.key == "backspace":
                    self.data["new_game_name"] = self.data["new_game_name"][:-1]
                else:
                    self.data["new_game_name"] += event.key

        # Update ui elements (They need to access the data to do so)
        [element.update(self.data) for element in self.ui_elements]


class JoinGameScreen(Screen):

    def __init__(self, client_state, window):
        super().__init__(client_state, window)

        self.data = {
            "time": client_state.clock.get(),
            "game_id": ""
        }

        self.ui_elements = [
            # ClockUI(self.data['time']),
            GameIdMessage(self.data['game_id']),
        ]

    def update(self, event):
        # And now here I can update the screen-specific data
        # for example the time.
        self.data['time'] = self.client_state.clock.get()

        if event is not None:
            if isinstance(event, UserTypedEvent):
                if event.key == "escape":
                    # Avoid circular import
                    from client.game_specific.commands import (
                        BackToLobby
                    )
                    BackToLobby(
                        self.client_state.profile,
                        self.client_state.queue
                    ).execute()
                if event.key == "return":
                    # Avoid circular import
                    from client.game_specific.commands import (
                        RequestJoiningAGame
                    )
                    RequestJoiningAGame(
                        self.client_state.profile,
                        self.client_state.queue,
                        self.data["game_id"]
                    ).execute()
                if event.key == "backspace":
                    self.data["game_id"] = self.data["game_id"][:-1]
                else:
                    self.data["game_id"] += event.key

        # Update ui elements (They need to access the data to do so)
        [element.update(self.data) for element in self.ui_elements]


class InGameScreen(Screen):
    def __init__(
        self,
        client_state,
        window,
        turn,
        board,
        game_id,
        name,
        player_1_id,
        player_2_id
    ):
        super().__init__(client_state, window)

        self.data = {
            "time": client_state.clock.get(),
            "turn": turn,
            "board": board,
            "game_id": game_id,
            "name": name,
            "player_1_id": player_1_id,
            "player_2_id": player_2_id

        }

        self.ui_elements = [
            # ClockUI(self.data['time']),
            TurnIndicator(self.data['turn']),
            GameIdIndicator(self.data['game_id']),
            GameNameIndicator(self.data['name']),
            Player1NameIndicator(self.data['player_1_id']),
            Player2NameIndicator(self.data['player_2_id']),
            Board(self.data['board']),
            Instructions(),
        ]

    def update(self, event):
        # And now here I can update the screen-specific data
        # for example the time.
        self.data['time'] = self.client_state.clock.get()

        if event is not None:
            if isinstance(event, UserTypedEvent):
                # Avoid circular import
                from client.game_specific.commands import (
                    BackToLobby,
                    RequestPlaceASymbol
                )
                if event.key == "escape":
                    BackToLobby(
                        self.client_state.profile,
                        self.client_state.queue
                    ).execute()
                if event.key in "012345678":
                    RequestPlaceASymbol(
                        self.client_state.profile,
                        self.client_state.queue,
                        event.key
                    ).execute()

        # Update ui elements (They need to access the data to do so)
        [element.update(self.data) for element in self.ui_elements]
