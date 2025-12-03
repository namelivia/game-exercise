from typing import Any, Dict

from engine.api import MousePosition, UIBuilder, UIElementLogic


class ImageCursorLogic(UIElementLogic):

    def update(self, time: int, data: Dict[str, Any]) -> None:
        super().update(time, data)
        mouse_position = MousePosition().get()
        self.state.set_x(mouse_position[0])
        self.state.set_y(mouse_position[1])


def create_image_cursor(image_path):
    return (
        UIBuilder(x=0, y=0)
        # The image is centered over the cusor
        .with_image(image_path, -32, -31, True, "image")
        .with_logic(ImageCursorLogic)
        .build()
    )
