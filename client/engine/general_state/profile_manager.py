import uuid
from typing import TYPE_CHECKING, Any, Type

from client.engine.persistence.persistence import Persistence

from .profile.profile import Profile

if TYPE_CHECKING:
    from client.engine.general_state.profile.profile import Profile


class ProfileManager:
    _instance = None

    # This class is a singleton
    def __new__(
        cls: Type["ProfileManager"], *args: Any, **kwargs: Any
    ) -> "ProfileManager":
        if not cls._instance:
            cls._instance = super(ProfileManager, cls).__new__(cls)
        return cls._instance

    def set_profile(self, profile_key: str) -> None:
        self.profile = self._load_or_create_profile(profile_key)

    def _load_or_create_profile(self, profile_key: str) -> "Profile":
        try:
            return Persistence.load(profile_key)  # Try to load the profile from a file
        except FileNotFoundError:
            return self._create_new_profile(
                profile_key
            )  # If the file does not exist, create a new profile

    def new_random_profile(
        self,
    ) -> "Profile":  # Generate a new profile with a random key
        return self._create_new_profile(str(uuid.uuid4()))

    def _create_new_profile(self, profile_key: str) -> "Profile":
        profile = Profile(
            key=profile_key, id=uuid.uuid4(), game_id=None, game_event_pointer=None
        )
        profile.save()
        return profile
