import uuid
from .profile import Profile


class Factory:
    @staticmethod
    def new_profile(key) -> Profile:
        return Profile(
            key=key,
            id=uuid.uuid4(),
            game_id=None,
            game_event_pointer=None,
            sound_on=True,
        )
