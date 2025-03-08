import uuid
from typing import TYPE_CHECKING, Any, Type

from client.engine.persistence.persistence import Persistence

from .profile.factory import Factory

if TYPE_CHECKING:
    from client.engine.general_state.profile.profile import Profile


# This is a singleton
class ProfileWhat:
    _instance = None

    def __new__(cls: Type["ProfileWhat"], *args: Any, **kwargs: Any) -> "ProfileWhat":
        if not cls._instance:
            cls._instance = super(ProfileWhat, cls).__new__(cls)
        return cls._instance

    def _get_new_profile(self, profile_key: str) -> "Profile":
        profile = Factory.new_profile(profile_key)
        profile.save()
        return profile

    def _initialize_status(self, profile_key: str) -> "Profile":
        try:
            return Persistence.load(profile_key)
        except FileNotFoundError:
            return self._get_new_profile(profile_key)

    def set_profile(self, profile_key: str) -> None:
        self.profile = self._initialize_status(profile_key)

    def new_profile(self) -> "Profile":  # Generate a new profile with a random name
        return self._get_new_profile(str(uuid.uuid4()))
