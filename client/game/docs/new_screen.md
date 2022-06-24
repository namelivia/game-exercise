# To make a new screen

Create a new folder in screens with the name of the new screen.
Create `__init__.py` and the screen Python file `my_screen.py`.
Create `ui.py` to place the ui elements that will conform the screen.

In `my_screen.py` create `MyScreen` class, it should extend `from client.primitives.screen.Screen`

Then import and place the ui elements in the `__init__` method.
Define the the event handler dict in `self.events` the handling functions must execute commands.

Fill in the event handler implementations.

There can also be timed functions defined in `self.timers` these will execute based on the global timer of the screen.

Example:

```
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
