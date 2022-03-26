from .game_specific.events import (
    ScreenTransitionEvent,
    NewGameRequestEvent,
    PlaceASymbolRequestEvent,
    JoinExistingGameEvent,
    QuitGameEvent,
    InitiateGameEvent
)
from client.game_specific.commands import UserTyped, CreateAGame, JoinAGame, PlaceASymbol

# This should manage transitions between states


class ScreenManager():

    # This will go somewhere else
    # Would I need all this? Maybe not, only someties if using pygame
    def __init__(self, client_state, input_manager, graphics):
        self.client_state = client_state  # Always
        self.graphics = graphics  # Only pygame
        self.input_manager = input_manager  # Only pygame

    def run(self):
        # THIS IS THE MAIN CYCLE!!!!

        # CLOCK
        self.client_state.clock.tick()  # Update the clock

        # QUEUE
        # TODO: Am I ready to pickup the next event from the queue? Maybe not! But for now OK.
        queued_event = self.client_state.queue.pop()  # Get the event from the queue
        # The event can perform an action on the general state
        # or the current screen state.
        # And to do so we need to check what type of event it is.

        # PROCESS GENERAL STATE EVENTS
        # This is an event that acts on the general state
        if isinstance(queued_event, QuitGameEvent):  # This could go somewhere else (not not on the event)
            import pygame  # This is pygame dependent
            import sys
            pygame.quit()
            sys.exit()
        if isinstance(queued_event, InitiateGameEvent):  # This could go somewhere else (not not on the event)
            # TODO: Why is it not an screen transition event???
            from client.game_specific.screens.screens import InGameScreen
            self.current_screen = InGameScreen(
                self.client_state,
                self.graphics,
                queued_event.turn,
                queued_event.board,
                queued_event.game_id,
                queued_event.name,
                queued_event.player_1_id,
                queued_event.player_2_id,
            )
        if isinstance(queued_event, ScreenTransitionEvent):  # This could go somewhere else (not not on the event)
            # Circular import
            from client.game_specific.screens.screens import Lobby, NewGameScreen, Intro, JoinGameScreen, InGameScreen
            if queued_event.dest_screen == "intro":
                self.current_screen = Intro(self.client_state, self.graphics)
            if queued_event.dest_screen == "lobby":
                self.current_screen = Lobby(self.client_state, self.graphics)
            if queued_event.dest_screen == "new_game_screen":
                self.current_screen = NewGameScreen(self.client_state, self.graphics)
            if queued_event.dest_screen == "join_a_game":
                self.current_screen = JoinGameScreen(self.client_state, self.graphics)
            # if queued_event.dest_screen == "in_game":
                # self.current_screen = InGameScreen(self.client_state, self.graphics)

        # PROCESS NETWORK RELATED EVENTS
        if isinstance(queued_event, NewGameRequestEvent):  # This could go somewhere else (not not on the event)
            CreateAGame(
                self.client_state.profile,
                self.client_state.queue
            ).execute(queued_event.new_game_name)

        if isinstance(queued_event, PlaceASymbolRequestEvent):  # This could go somewhere else (not not on the event)
            PlaceASymbol(
                self.client_state.profile,
                self.client_state.queue
            ).execute(queued_event.position)

        if isinstance(queued_event, JoinExistingGameEvent):  # This could go somewhere else (not not on the event)
            JoinAGame(
                self.client_state.profile,
                self.client_state.queue
            ).execute(queued_event.game_id)

        self.current_screen.render()  # Display

        if self.input_manager is not None:
            user_events = self.input_manager.read()  # Get the user input
            actions_mapping = {
                "event_1": UserTyped(
                    self.client_state.profile,
                    self.client_state.queue,
                    "1"  # maybe here I can pass the key from the event
                ),
                "event_2": UserTyped(
                    self.client_state.profile,
                    self.client_state.queue,
                    "2"
                ),
                "event_3": UserTyped(
                    self.client_state.profile,
                    self.client_state.queue,
                    "3"
                ),
                "event_4": UserTyped(
                    self.client_state.profile,
                    self.client_state.queue,
                    "4"
                ),
                "event_5": UserTyped(
                    self.client_state.profile,
                    self.client_state.queue,
                    "5"
                ),
                "event_6": UserTyped(
                    self.client_state.profile,
                    self.client_state.queue,
                    "6"
                ),
                "event_7": UserTyped(
                    self.client_state.profile,
                    self.client_state.queue,
                    "7"
                ),
                "event_8": UserTyped(
                    self.client_state.profile,
                    self.client_state.queue,
                    "8"
                ),
                "event_9": UserTyped(
                    self.client_state.profile,
                    self.client_state.queue,
                    "9"
                ),
                "event_0": UserTyped(
                    self.client_state.profile,
                    self.client_state.queue,
                    "0"
                ),
                "event_a": UserTyped(
                    self.client_state.profile,
                    self.client_state.queue,
                    "a"
                ),
                "event_b": UserTyped(
                    self.client_state.profile,
                    self.client_state.queue,
                    "b"
                ),
                "event_c": UserTyped(
                    self.client_state.profile,
                    self.client_state.queue,
                    "c"
                ),
                "event_d": UserTyped(
                    self.client_state.profile,
                    self.client_state.queue,
                    "d"
                ),
                "event_e": UserTyped(
                    self.client_state.profile,
                    self.client_state.queue,
                    "e"
                ),
                "event_f": UserTyped(
                    self.client_state.profile,
                    self.client_state.queue,
                    "f"
                ),
                "event_g": UserTyped(
                    self.client_state.profile,
                    self.client_state.queue,
                    "g"
                ),
                "event_h": UserTyped(
                    self.client_state.profile,
                    self.client_state.queue,
                    "h"
                ),
                "event_i": UserTyped(
                    self.client_state.profile,
                    self.client_state.queue,
                    "i"
                ),
                "event_j": UserTyped(
                    self.client_state.profile,
                    self.client_state.queue,
                    "j"
                ),
                "event_k": UserTyped(
                    self.client_state.profile,
                    self.client_state.queue,
                    "k"
                ),
                "event_l": UserTyped(
                    self.client_state.profile,
                    self.client_state.queue,
                    "l"
                ),
                "event_m": UserTyped(
                    self.client_state.profile,
                    self.client_state.queue,
                    "m"
                ),
                "event_n": UserTyped(
                    self.client_state.profile,
                    self.client_state.queue,
                    "n"
                ),
                "event_o": UserTyped(
                    self.client_state.profile,
                    self.client_state.queue,
                    "o"
                ),
                "event_p": UserTyped(
                    self.client_state.profile,
                    self.client_state.queue,
                    "p"
                ),
                "event_q": UserTyped(
                    self.client_state.profile,
                    self.client_state.queue,
                    "q"
                ),
                "event_r": UserTyped(
                    self.client_state.profile,
                    self.client_state.queue,
                    "r"
                ),
                "event_s": UserTyped(
                    self.client_state.profile,
                    self.client_state.queue,
                    "s"
                ),
                "event_t": UserTyped(
                    self.client_state.profile,
                    self.client_state.queue,
                    "t"
                ),
                "event_u": UserTyped(
                    self.client_state.profile,
                    self.client_state.queue,
                    "u"
                ),
                "event_v": UserTyped(
                    self.client_state.profile,
                    self.client_state.queue,
                    "v"
                ),
                "event_w": UserTyped(
                    self.client_state.profile,
                    self.client_state.queue,
                    "w"
                ),
                "event_x": UserTyped(
                    self.client_state.profile,
                    self.client_state.queue,
                    "x"
                ),
                "event_y": UserTyped(
                    self.client_state.profile,
                    self.client_state.queue,
                    "y"
                ),
                "event_z": UserTyped(
                    self.client_state.profile,
                    self.client_state.queue,
                    "z"
                ),
                "event_return": UserTyped(
                    self.client_state.profile,
                    self.client_state.queue,
                    "return"
                ),
                "event_escape": UserTyped(
                    self.client_state.profile,
                    self.client_state.queue,
                    "escape"
                ),
                "event_backspace": UserTyped(
                    self.client_state.profile,
                    self.client_state.queue,
                    "backspace"
                ),
                "event_space": UserTyped(
                    self.client_state.profile,
                    self.client_state.queue,
                    " "
                ),
                "event_minus": UserTyped(
                    self.client_state.profile,
                    self.client_state.queue,
                    "-"
                ),
            }

            # Transform user events into commands and execute them
            [actions_mapping[user_event].execute() for user_event in user_events if user_event in actions_mapping]

        # Execute commands using all together (this may add new events to the queue)
        # And apply it on the screen (may add new events to the queue?)
        self.current_screen.update(queued_event)
