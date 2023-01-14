from client.engine.features.user_input.commands import UserTyped


class UserInput:
    @staticmethod
    def process(input_manager, client_state):
        # Get events from user input
        user_events = input_manager.read()

        # Run the user typed command for each user event
        for user_event in user_events:
            UserTyped(client_state.profile, client_state.queue, user_event).execute()
