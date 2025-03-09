import logging
from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Type

from client.engine.general_state.profile_manager import ProfileManager
from client.engine.persistence.persistence import Persistence
from client.engine.primitives.event_handler import EventHandler

from .commands import ProfileIsSet, SetProfile, UpdateProfiles
from .events import GetProfilesEvent, NewProfileEvent, SetProfileEvent

if TYPE_CHECKING:
    from client.engine.primitives.event import Event


logger = logging.getLogger(__name__)


class SetProfileEventHandler(EventHandler[SetProfileEvent]):
    def handle(self, event: "SetProfileEvent") -> None:
        profile_manager = ProfileManager()
        profile_manager.set_profile(event.key)
        ProfileIsSet(event.key).execute()


class NewProfileEventHandler(EventHandler[NewProfileEvent]):
    def handle(self, event: "NewProfileEvent") -> None:
        profile_manager = ProfileManager()
        new_profile_key = profile_manager.new_random_profile().key
        SetProfile(new_profile_key).execute()


class GetProfilesEventHandler(EventHandler[GetProfilesEvent]):
    def handle(self, event: "GetProfilesEvent") -> None:
        # TODO retrieve profiles from disk
        profiles = self._build_profiles_index(Persistence.list())
        UpdateProfiles(profiles).execute()

    def _build_profiles_index(self, profiles: Iterable[Any]) -> List[Dict[str, str]]:
        # TODO: Excluding gitkeep should happen in the persistence layer, not here
        return [{"name": profile} for profile in profiles if profile != ".gitkeep"]


handlers_map: Dict[Type["Event"], Any] = {
    SetProfileEvent: SetProfileEventHandler,
    NewProfileEvent: NewProfileEventHandler,
    GetProfilesEvent: GetProfilesEventHandler,
}
