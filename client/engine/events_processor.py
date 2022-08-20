class EventsProcessor:
    def __init__(self, event_handlers):
        self.event_handlers = event_handlers  # Initial list of event handlers

    def add_event_handler(self, event_handler):
        self.event_handlers.append(event_handler)

    def handle(self, event, client_state):
        if event is None:
            return
        print(event)
        handled = False
        for event_handler in self.event_handlers:
            try:
                event_handler.handle(event, client_state)
                handled = True
            except KeyError:  # TODO: Restrict this, it should only catch non-handeable events
                pass
        if not handled:
            pass  # TODO: Inform that no handler was able to handle the event
