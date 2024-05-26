from client.engine.external.foundational_wrapper import FoundationalWrapper


class Mouse:
    def get(self) -> int:
        return FoundationalWrapper.get_mouse_position()
