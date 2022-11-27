from client.engine.graphics.shapes import SmallText, WHITE, Rectangle
from client.engine.primitives.ui import UIElement


class ChatMessages(UIElement):
    def _get_message_string(self, message, index):
        player_id = message["player_id"]
        contents = message["message"]
        return f"{player_id}: {contents}"

    def __init__(self, messages):
        self.shapes = [
            SmallText(self._get_message_string(message, index), 20, 300 + (20 * index))
            for index, message in enumerate(messages)
        ]

    def update(self, time, data):
        # What if data does not contain events? Throw an exception
        messages = data["chat_messages"][
            -6:
        ]  # Show only the last 6 to fit in the screen
        self.shapes = [
            SmallText(self._get_message_string(message, index), 20, 300 + (20 * index))
            for index, message in enumerate(messages)
        ]


class ChatInput(UIElement):
    def __init__(self):
        self.shapes = []
        self.visible = False

    def focus(self):
        self.visible = True

    def unfocus(self):
        self.visible = False

    def update(self, time, data):
        if self.visible:
            # What if data does not contain events? Throw an exception
            self.shapes = [
                Rectangle(0, 430, 640, 30),
                SmallText(f"Send message: {data['chat_input']}", 20, 440, WHITE),
            ]
        else:
            self.shapes = []
