from typing import TYPE_CHECKING

from client.engine.features.synchronization.commands import RequestGameStatus
from client.engine.general_state.client_state import ClientState
from client.engine.general_state.profile_what import ProfileWhat

if TYPE_CHECKING:
    from uuid import UUID


class ServerPolling:
    @staticmethod
    def _get_polling_rate() -> int:
        # The polling rate is how often the server is queried for new information
        return 100

    @staticmethod
    def _should_do_polling(time: int) -> bool:
        return time % ServerPolling._get_polling_rate() == 0

    @staticmethod
    def push_polling_event_if_needed() -> None:
        client_state = ClientState()
        profile_what = ProfileWhat()
        game_id = profile_what.profile.game_id
        pointer = profile_what.profile.game_event_pointer
        if game_id is not None and pointer is not None:
            time = client_state.clock.get()
            if ServerPolling._should_do_polling(time):
                RequestGameStatus(
                    game_id,
                    pointer,
                ).execute()
