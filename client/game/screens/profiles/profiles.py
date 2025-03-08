from client.engine.features.profile.commands import GetProfiles, NewProfile, SetProfile
from client.engine.features.profile.events import (
    ProfileSetInGameEvent,
    UpdateProfilesInGameEvent,
)
from client.engine.features.user_input.events import UserTypedEvent
from client.engine.general_state.client_state import ClientState
from client.engine.primitives.screen import Screen

from .ui import Background, ProfileList, ProfilesTitle


class Profiles(Screen):
    def __init__(self):
        super().__init__()

        self.data = {"profiles": []}

        self.ui_elements = [
            Background(),
            ProfileList(self.data["profiles"]),
            ProfilesTitle(),
        ]

        self.events = {
            UserTypedEvent: self.on_user_typed,
            UpdateProfilesInGameEvent: self.on_profiles_updated,
            ProfileSetInGameEvent: self.on_profile_set,
        }
        client_state = ClientState()
        GetProfiles(client_state.queue).execute()

    def on_user_typed(self, event: UserTypedEvent) -> None:
        if event.key == "escape":
            # Avoid circular import
            from client.game.commands import BackToLobby

            client_state = ClientState()
            BackToLobby(client_state.queue).execute()
            return
        if event.key == "0":
            client_state = ClientState()
            NewProfile(client_state.queue).execute()
            return
        if event.key in "123456789":
            client_state = ClientState()
            SetProfile(
                client_state.queue,
                self.data["profiles"][int(event.key) - 1]["name"],
            ).execute()

    def on_profiles_updated(self, event: UpdateProfilesInGameEvent) -> None:
        self.data["profiles"] = event.profiles

    def on_profile_set(self, event: ProfileSetInGameEvent) -> None:
        # Avoid circular import
        from client.game.commands import BackToLobby

        client_state = ClientState()
        BackToLobby(client_state.queue).execute()
