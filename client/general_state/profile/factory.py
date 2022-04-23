import uuid
from .profile import Profile


class Factory:
    @staticmethod
    def new_profile(name: str) -> Profile:
        return Profile(
            id=uuid.uuid4(),
            name=name,
            game_id=None,
            game_event_pointer=None,
            sound_on=True,
        )
