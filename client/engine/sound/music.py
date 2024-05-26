from client.engine.foundational_wrapper import FoundationalWrapper


class Music:
    @staticmethod
    def load(path: str) -> None:
        FoundationalWrapper.load_music(path)

    @staticmethod
    def play() -> None:
        FoundationalWrapper.play_music()

    @staticmethod
    def stop() -> None:
        FoundationalWrapper.stop_music()
