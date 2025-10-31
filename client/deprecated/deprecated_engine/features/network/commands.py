from typing import TYPE_CHECKING

from client.engine.primitives.command import Command

from .events import NetworkRequestEvent


class SendNetworkRequest(Command):
    def __init__(self, data, on_success_callback, on_error_callback) -> None:
        super().__init__("Sending network request")
        self.queue = "network"
        self.events = [
            NetworkRequestEvent(data, on_success_callback, on_error_callback),
        ]
