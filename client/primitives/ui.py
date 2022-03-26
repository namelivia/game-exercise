from abc import ABC


class UIElement(ABC):

    # UI elements can hold a small state too that can be updated
    def render(self, window):
        [shape.render(window) for shape in self.shapes]

    def update(self, time, data):
        pass
