from client.engine.external.foundational_wrapper import FoundationalWrapper


class Clock:
    def get(self) -> int:
        return FoundationalWrapper.get_clock_ticks()
