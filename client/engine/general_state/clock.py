from client.engine.external.foundational_wrapper import FoundationalWrapper


class Clock:
    def tick(self) -> None:
        pass

    def get(self) -> int:
        return FoundationalWrapper.get_clock_ticks()
