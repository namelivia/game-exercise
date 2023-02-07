import logging
import pickle
import socketserver
from typing import TYPE_CHECKING, Any

from common.messages import (
    CreateAGameMessage,
    ErrorMessage,
    GameListRequestMessage,
    GetGameStatus,
    JoinAGameMessage,
    PingRequestMessage,
    PlaceASymbolMessage,
    SendChatMessage,
)

from .commands import (
    CreateGame,
    GameStatus,
    GetGameList,
    JoinGame,
    Ping,
    PlaceSymbol,
    SendChat,
)
from .errors import InvalidCommandError

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from .commands import Command

"""
This just intializes the server
"""


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def decode_command(self, raw_command: Any) -> "Command":
        decoded = pickle.loads(raw_command)
        # TODO: Deal with malformed commands
        if isinstance(decoded, PlaceASymbolMessage):
            return PlaceSymbol(
                decoded.game_id, decoded.event_id, decoded.player_id, decoded.position
            )
        if isinstance(decoded, SendChatMessage):
            return SendChat(
                decoded.game_id, decoded.event_id, decoded.player_id, decoded.message
            )
        if isinstance(decoded, CreateAGameMessage):
            return CreateGame(decoded.name, decoded.player_id)
        if isinstance(decoded, JoinAGameMessage):
            return JoinGame(decoded.game_id, decoded.player_id)
        if isinstance(decoded, GetGameStatus):
            return GameStatus(decoded.game_id, decoded.pointer, decoded.player_id)
        if isinstance(decoded, PingRequestMessage):
            return Ping()
        if isinstance(decoded, GameListRequestMessage):
            return GetGameList()
        raise InvalidCommandError("Unknown command")

    def handle(self) -> None:
        logger.info(f"Incoming message from {self.client_address}")
        # When getting a request
        request_data = self.request.recv(1024)  # TODO: Set a value for this

        try:
            # Using the command map get the command
            command = self.decode_command(request_data)
            logger.info(f"Command is {command.name}")

            # Execute the command to get the response message
            message = command.execute()

        except InvalidCommandError as err:
            message = ErrorMessage(f"The command is invalid: {err}")
        # And return the message
        self.request.sendall(pickle.dumps(message))


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass
