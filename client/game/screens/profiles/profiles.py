from client.engine.primitives.screen import Screen
from .ui import ProfilesTitle, ProfileList, Background
from client.engine.events import (
    UserTypedEvent,
    UpdateProfilesInGameEvent
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
        }

        from client.engine.commands import GetProfiles

        GetProfiles(self.client_state.profile, self.client_state.queue).execute()

    def on_user_typed(self, event):
        if event.key == "escape":
            # Avoid circular import
            from client.game.commands import BackToLobby

            BackToLobby(self.client_state.profile, self.client_state.queue).execute()
            return
        if event.key in "012345678":
            pass
            # from client.engine.commands import RequestJoiningAGame

            '''
            RequestJoiningAGame(
                self.client_state.profile,
                self.client_state.queue,
                self.data["games"][int(event.key)].id,
            ).execute()
            '''

    def on_profiles_updated(self, event):
        print(event)
        self.data["profiles"] = event.profiles
