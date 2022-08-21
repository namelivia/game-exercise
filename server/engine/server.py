import logging
import socketserver
import pickle
from .commands import (
    PlaceSymbol,
    SendChat,
    JoinGame,
    CreateGame,
    GameStatus,
    Ping,
    GetGameList,
)
from common.messages import (
    ErrorMessage,
    PlaceASymbolMessage,
    SendChatMessage,
    CreateAGameMessage,
    JoinAGameMessage,
    GetGameStatus,
    PingRequestMessage,
    GameListRequestMessage,
)
from .errors import InvalidCommandError

logger = logging.getLogger(__name__)

"""
This just intializes the server
"""


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def decode_command(self, raw_command):
        decoded = pickle.loads(raw_command)
        # TODO: Deal with malformed commands
        if isinstance(decoded, PlaceASymbolMessage):
            return PlaceSymbol(decoded.game_id, decoded.player_id, decoded.position)
        if isinstance(decoded, SendChatMessage):
            return SendChat(decoded.game_id, decoded.player_id, decoded.message)
        if isinstance(decoded, CreateAGameMessage):
            return CreateGame(decoded.name, decoded.player_id)
        if isinstance(decoded, JoinAGameMessage):
            return JoinGame(decoded.game_id, decoded.player_id)
        if isinstance(decoded, GetGameStatus):
            return GameStatus(decoded.game_id, decoded.player_id)
        if isinstance(decoded, PingRequestMessage):
            return Ping()
        if isinstance(decoded, GameListRequestMessage):
            return GetGameList()
        raise InvalidCommandError("Unknown command")

    def handle(self):
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