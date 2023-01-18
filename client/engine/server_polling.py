from client.engine.features.synchronization.commands import RequestGameStatus


class ServerPolling:
    @staticmethod
    def _get_polling_rate():
        # The polling rate is how often the server is queried for new information
        return 100

    @staticmethod
    def _is_polling_time(time):
        return time % ServerPolling._get_polling_rate() == 0

    @staticmethod
    def _is_playing_a_game(game_id):
        return game_id is not None

    @staticmethod
    def _should_do_polling(client_state):
        game_id = client_state.profile.game_id
        time = client_state.clock.get()
        return ServerPolling._is_playing_a_game(
            game_id
        ) and ServerPolling._is_polling_time(time)

    @staticmethod
    def push_polling_event_if_needed(client_state):
        if ServerPolling._should_do_polling(client_state):
            RequestGameStatus(
                client_state.profile,
                client_state.queue,
                client_state.profile.game_id,
                client_state.profile.game_event_pointer,
            ).execute()
