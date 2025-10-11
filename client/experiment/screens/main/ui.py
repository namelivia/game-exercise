from client.engine.features.game_logic.commands import ChangeCursor
from client.engine.graphics.shapes import Image
from client.engine.primitives.ui import ClickableUIElement, UIElement
from client.experiment.images import BACKGROUND


class Background(UIElement):
    def __init__(self) -> None:
        super().__init__()
        self.set_shapes([Image(BACKGROUND, 0, 0)])


class Portrait(ClickableUIElement):
    def __init__(self, image: str, highlight: str, x: int, y: int, on_click) -> None:
        super().__init__(on_click)
        self.image = Image(image, x, y)
        self.highlight = Image(highlight, x, y)
        self.highlight.hide()
        self.set_shapes([self.image, self.highlight])

    def on_mouse_enter(self):
        ChangeCursor("HAND").execute()
        self.highlight.show()
        self.image.hide()

    def on_mouse_leave(self):
        ChangeCursor("ARROW").execute()
        self.highlight.hide()
        self.image.show()
