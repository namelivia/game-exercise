**Disclaimer**: These are mainly notes for myself for when I pickup this project from time to time

# To make a new screen

Create a new folder in screens with the name of the new screen.
Create `__init__.py` and the screen Python file `my_screen.py`.
Create `ui.py` to place the ui elements that will conform the screen.

In `my_screen.py` create `MyScreen` class, it should extend `from client.engine.primitives.screen.Screen`

Then import and place the ui elements in the `__init__` method.
Define the the event handler dict in `self.events` the handling functions must execute commands.

Fill in the event handler implementations.

There can also be timed functions defined in `self.timers` these will execute based on the global timer of the screen.

Example:

```python
class MyScreen(Screen):
    def __init__(self, client_state):
        super().__init__(client_state)
        
        self.ui_elements = [
            MyUIElement(),
            AnotherUIElement(),
        ]
        
        self.events = {UserTypedEvent: self.on_user_typed_event}
        self.timers = {10000: self.move_to_next_screen}
        
    def on_user_typed(self, event):
        if event.key == "escape":
            MyCommand(self.client_state.profile, self.client_state.queue).execute()
            
    def move_to_next_screen(self, event):
        MyCommand(self.client_state.profile, self.client_state.queue).execute()
```

# To make a command

Commands go on `commands.py` and are classes that extend `from client.engine.primitives.command.Command`.
Then the `__init__` function is defined, should have `profile` and `queue` parameters and then any arbitrary data needed.
When calling `super().__init__` a third parameter with the description of the command is providen.
Finally commands are just lists of `Events` with data associated to them, so to decribe what a command does we just have to define it's `self.events` array.

Example:

```python
class MyCommand(Command):
    def __init__(self, profile, queue, my_data)
        super().__init__(
            profile, queue, f"I will use this data for something {my_data}"
        )
        self.events[
            MyCustomEvent(my_data),
            AnotherCustomEvent("hardcoded_data")
        ]
```

# To make an event

Events go on `events.py` and are pushed to a queue to be processed. Events are classes
extending `from client.engine.primitives.event.Event` define the operation to be performed when extracted from the queue and also hold the data needed to perform such operation.


Example:

```python
class MyCustomEvent(Event):
    def __init__(self, my_data):
        super().__init__()
        self.my_data = my_data
        
class AnotherCustomEvent(Event):
    pass
```

# To make an event handler

Events need to be processed when being extracted from the queue, there are two places to decide what to do with them, the first is on the screen events dictionary defined above. The second one is `event_handler.py`.
This file contains a dictionary called `handlers_map` in which Events are paired with their event handlers, event handlers are classes that extend from `client.engine.primitives.event_handler.EventHandler` and need to define a handle function that will recieve and process the event.

Processing the event can be accesing the sound manager, the network manager, altering the client state, or calling new commands.

Example:

```python
class MyCustomEventHandler(EventHandler):
    def handle(self, event, client_state):
        client_state.something = my_data
        
class AnotherCustomEventHandler(EventHandler):
    def handle(self, event):
        AnotherCommand().execute()
```

```python
    handlers_map = {
        MyCustomEvent: MyCustomEventHandler,
        AnotherCustomEvent: AnotherCustomEventHandler,
    }
```

# The flow

Let's for example examine the following use case, when a user is in the "Credits" screen, will hit the escape key and some sound will be played, and the user will be taken to the main screen.

We would have to create a new screen called `credits`, in that screen we could make a new ui element to display the rolling credits. Then, we would put an event handler for the escape key thay will execute a new command called for example `GoBackToMain`.

The command can define contain two events, one for playing a sound and another one to
make te transition to the main screen, so we can define 2 events for that.

Finally on the event handler, we would add both events to the handlers map and define its handlers, the sound one will ask the sound manager to play the sound, And the other will update the internal state to set the new screen.
