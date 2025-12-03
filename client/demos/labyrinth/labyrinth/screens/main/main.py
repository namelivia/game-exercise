from engine.api import Screen


class MainScreen(Screen):
    def __init__(self) -> None:
        super().__init__()

        self.data = {}
        self.ui_elements = []
        self.events = {}
