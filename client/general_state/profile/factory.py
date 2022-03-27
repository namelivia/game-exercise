import uuid
from .profile import Profile


class Factory():

    @staticmethod
    def new_profile(name: str) -> Profile:
        return Profile(
            uuid.uuid4(),
            name,
            None,  # game_id
            None  # game_event_pointer
        )
