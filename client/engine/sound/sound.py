from client.engine.external.foundational_wrapper import FoundationalWrapper


class Sound:
    @staticmethod
    def play(path: str) -> None:
        FoundationalWrapper.play_sound(path)
