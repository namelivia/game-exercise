from client.engine.primitives.screen import Screen
from .ui import ProfilesTitle, ProfileList, Background
from client.engine.events import (
    UserTypedEvent,
    UpdateProfilesInGameEvent,
    ProfileSetInGameEvent
)


class Profiles(Screen):
    def __init__(self, client_state):
        super().__init__(client_state)

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

        from client.engine.commands import GetProfiles

        GetProfiles(self.client_state.profile, self.client_state.queue).execute()

    def on_user_typed(self, event):
        if event.key == "escape":
            # Avoid circular import
            from client.game.commands import BackToLobby

            BackToLobby(self.client_state.profile, self.client_state.queue).execute()
            return
        if event.key == "0":
            # Avoid circular import
            from client.engine.commands import NewProfile

            NewProfile(self.client_state.profile, self.client_state.queue).execute()
            return
        if event.key in "123456789":
            from client.engine.commands import SetProfile

            SetProfile(
                self.client_state.profile,
                self.client_state.queue,
                self.data["profiles"][int(event.key) - 1]["name"],
            ).execute()

    def on_profiles_updated(self, event):
        self.data["profiles"] = event.profiles

    def on_profile_set(self, event):
        # Avoid circular import
        from client.game.commands import BackToLobby

        BackToLobby(
            self.client_state.profile, self.client_state.queue
        ).execute()
