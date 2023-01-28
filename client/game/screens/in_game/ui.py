from typing import Any, Dict, List
from client.engine.graphics.shapes import SmallText, Image, Animation, Rectangle, WHITE
from client.engine.primitives.ui import UIElement


class GameIdIndicator(UIElement):
    def __init__(self, game_id: str):
        self.game_id = game_id
        self.shapes = [SmallText(f"Game Id: {game_id}", 20, 40)]


class GameNameIndicator(UIElement):
    def __init__(self, name: str):
        self.name = name
        self.shapes = [SmallText(f"Game name: {name}", 20, 60)]


class Player1NameIndicator(UIElement):
    def __init__(self, name: str):
        self.shapes = [SmallText(f"Player 1 name: {name}", 20, 80)]


class Player2NameIndicator(UIElement):
    def __init__(self) -> None:
        self.shapes = [SmallText("No player 2 yet", 20, 100)]

    def update(self, time: int, data: Dict[str, Any]) -> None:
        # What if data does not contain events? Throw an exception
        if len(data["players"]) > 1:
            name = data["players"][1]
            self.shapes = [SmallText(f"Player 2 name: {name}", 20, 100)]
        else:
            self.shapes = [SmallText("No player 2 yet", 20, 100)]


class Events(UIElement):
    def _get_event_string(self, event: Any, pointer: int, index: int) -> str:
        return str(event) + " <= [POINTER]" if index == pointer else str(event)

    def __init__(self, events: Dict[str, str], pointer: int):
        self.events = events
        self.shapes = [
            SmallText(
                self._get_event_string(event, pointer, index), 20, 300 + (20 * index)
            )
            for index, event in enumerate(events)
        ]

    def update(self, time: int, data: Dict[str, Any]) -> None:
        # What if data does not contain events? Throw an exception
        events = data["events"]
        pointer = data["event_pointer"]
        self.shapes = [
            SmallText(
                self._get_event_string(event, pointer, index), 20, 300 + (20 * index)
            )
            for index, event in enumerate(events)
        ]


class ChatMessages(UIElement):
    def _get_message_string(self, message: str, index: int) -> str:
        player_id = message["player_id"]
        contents = message["message"]
        confirmation = message["confirmation"]
        return f"{player_id}: {contents} | {confirmation}"

    def __init__(self, messages: Dict[str, str]):
        self.shapes = [
            SmallText(self._get_message_string(message, index), 20, 300 + (20 * index))
            for index, message in enumerate(messages)
        ]

    def update(self, time: int, data: Dict[str, Any]) -> None:
        # What if data does not contain events? Throw an exception
        messages = data["chat_messages"][
            -6:
        ]  # Show only the last 6 to fit in the screen
        self.shapes = [
            SmallText(self._get_message_string(message, index), 20, 300 + (20 * index))
            for index, message in enumerate(messages)
        ]


class Background(UIElement):
    def __init__(self) -> None:
        self.shapes = [Image("client/game/images/background5.png", 0, 0)]


class IntroAnimation(UIElement):
    def __init__(self) -> None:
        self.shapes = [
            Animation("client/game/images/coin", 0, 150),
            Animation("client/game/images/coin", 250, 0, 3),
        ]

        self.shapes[0].hide()
        self.shapes[1].hide()
        self.timer = 0

    def play(self) -> None:
        self.shapes[0].show()
        self.shapes[1].show()
        self.timer = 0

    def update(self, time: int, data: Dict[str, Any]) -> None:
        self.timer += 1
        animation_speed = 128  # The higher the slower
        if (time % animation_speed) == 0:
            self.shapes[0].update()  # Not supersure about this
            self.shapes[1].update()  # Not supersure about this
        movement_speed = 5  # The higher the slower
        self.shapes[0].set_x(
            int((time / movement_speed) % 640)
        )  # Not supersure about this
        self.shapes[1].set_y(
            int((time / movement_speed) % 480)
        )  # Not supersure about this

        if self.timer > 200:
            self.shapes[0].hide()
            self.shapes[1].hide()


class ChatInput(UIElement):
    def __init__(self) -> None:
        self.shapes = []
        self.visible = False

    def focus(self) -> None:
        self.visible = True

    def unfocus(self) -> None:
        self.visible = False

    def update(self, time: int, data: Dict[str, Any]) -> None:
        if self.visible:
            # What if data does not contain events? Throw an exception
            self.shapes = [
                Rectangle(0, 430, 640, 30),
                SmallText(f"Send message: {data['chat_input']}", 20, 440, WHITE),
            ]
        else:
            self.shapes = []


class Board(UIElement):
    def __init__(self) -> None:
        self.positions = [
            (310, 60),
            (364, 60),
            (418, 60),
            (310, 117),
            (364, 117),
            (418, 117),
            (310, 174),
            (364, 174),
            (418, 174),
        ]
        self.shapes = [
            Image("client/game/images/board.png", 300, 50),
            Image(
                "client/game/images/tile.png",
                self.positions[0][0],
                self.positions[0][1],
            ),
            Image(
                "client/game/images/tile.png",
                self.positions[1][0],
                self.positions[1][1],
            ),
            Image(
                "client/game/images/tile.png",
                self.positions[2][0],
                self.positions[2][1],
            ),
            Image(
                "client/game/images/tile.png",
                self.positions[3][0],
                self.positions[3][1],
            ),
            Image(
                "client/game/images/tile.png",
                self.positions[4][0],
                self.positions[4][1],
            ),
            Image(
                "client/game/images/tile.png",
                self.positions[5][0],
                self.positions[5][1],
            ),
            Image(
                "client/game/images/tile.png",
                self.positions[6][0],
                self.positions[6][1],
            ),
            Image(
                "client/game/images/tile.png",
                self.positions[7][0],
                self.positions[7][1],
            ),
            Image(
                "client/game/images/tile.png",
                self.positions[8][0],
                self.positions[8][1],
            ),
        ]

    def _get_current_board_positions(self, data: Dict[str, Any]) -> List[int]:
        return [board_entry["current"] for board_entry in data["board"]]

    def update(self, time: int, data: Dict[str, Any]) -> None:
        self.shapes = [
            Image("client/game/images/board.png", 300, 50),
            Image(
                "client/game/images/tile.png",
                self.positions[0][0],
                self.positions[0][1],
            ),
            Image(
                "client/game/images/tile.png",
                self.positions[1][0],
                self.positions[1][1],
            ),
            Image(
                "client/game/images/tile.png",
                self.positions[2][0],
                self.positions[2][1],
            ),
            Image(
                "client/game/images/tile.png",
                self.positions[3][0],
                self.positions[3][1],
            ),
            Image(
                "client/game/images/tile.png",
                self.positions[4][0],
                self.positions[4][1],
            ),
            Image(
                "client/game/images/tile.png",
                self.positions[5][0],
                self.positions[5][1],
            ),
            Image(
                "client/game/images/tile.png",
                self.positions[6][0],
                self.positions[6][1],
            ),
            Image(
                "client/game/images/tile.png",
                self.positions[7][0],
                self.positions[7][1],
            ),
            Image(
                "client/game/images/tile.png",
                self.positions[8][0],
                self.positions[8][1],
            ),
        ]

        for index, ball in enumerate(self._get_current_board_positions(data)):
            if ball is not None:
                if ball["color"] == "blue" and ball["confirmation"] == "OK":
                    self.shapes.append(
                        Image(
                            "client/game/images/blue_ball.png",
                            self.positions[index][0],
                            self.positions[index][1],
                        )
                    )
                if ball["color"] == "blue" and ball["confirmation"] == "pending":
                    self.shapes.append(
                        Image(
                            "client/game/images/blue_ball_pending.png",
                            self.positions[index][0],
                            self.positions[index][1],
                        )
                    )
                if ball["color"] == "red" and ball["confirmation"] == "OK":
                    self.shapes.append(
                        Image(
                            "client/game/images/red_ball.png",
                            self.positions[index][0],
                            self.positions[index][1],
                        )
                    )
                if ball["color"] == "red" and ball["confirmation"] == "pending":
                    self.shapes.append(
                        Image(
                            "client/game/images/red_ball_pending.png",
                            self.positions[index][0],
                            self.positions[index][1],
                        )
                    )


class StatusIndicator(UIElement):
    def __init__(self, status: str):
        self.shapes = [SmallText(f"Status: {status}", 20, 150)]

    def update(self, time: int, data: Dict[str, Any]) -> None:
        status = data["status"]
        self.shapes = [SmallText(f"Status: {status}", 20, 150)]


class WinnerIndicator(UIElement):
    def __init__(self, status: str):
        self.shapes = []

    def update(self, time: int, data: Dict[str, Any]) -> None:
        winner = data["winner"]
        if winner is None:
            self.shapes = []
        else:
            self.shapes = [SmallText(f"{winner} wins the game!!!", 20, 170)]
