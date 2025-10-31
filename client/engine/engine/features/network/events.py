from engine.primitives.event import Event


class NetworkRequestEvent(Event):
    def __init__(self, data, on_success_callback, on_error_callback):
        super().__init__()
        self.data = data
        self.on_success_callback = on_success_callback
        self.on_error_callback = on_error_callback
