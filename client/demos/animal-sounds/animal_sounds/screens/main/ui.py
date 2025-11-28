from typing import Any, Dict

from animal_sounds.images import BACKGROUND
from engine.api import (
    ChangeCursor,
    ClickableUIElement,
    EnableUserInput,
    ShowCursor,
    UIBuilder,
    UIElementLogic,
)


def create_background():
    return UIBuilder(x=0, y=0).with_image(BACKGROUND).build()


class OverlayCustomLogic(UIElementLogic):

    DURATION = 2500

    def update(self, time: int, data: Dict[str, Any]) -> None:
        progress = time / OverlayCustomLogic.DURATION

        if progress > 1.0:
            progress = 1.0
            self.enabled = False
            EnableUserInput().execute()
            ShowCursor().execute()

        opacity = 1.0 - progress
        self.state.set_opacity(opacity)


def create_overlay():
    return (
        UIBuilder(x=0, y=0)
        .with_rectangle(0, 0, 640, 480, (0, 0, 0))
        .with_logic(OverlayCustomLogic)
        .build()
    )


def create_portrait(image_path: str, highlight_path: str, x: int, y: int, on_click):
    element = (
        UIBuilder(x=x, y=y)
        .with_image(image_path, 0, 0, True, "image")
        .with_image(highlight_path, 0, 0, False, "highlight")
        .build()
    )

    def on_enter():
        ChangeCursor("HAND").execute()
        element.get_render().find_shape("highlight").show()
        element.get_render().find_shape("image").hide()

    def on_leave():
        ChangeCursor("ARROW").execute()
        element.get_render().find_shape("highlight").hide()
        element.get_render().find_shape("image").show()

    return ClickableUIElement(
        element=element,
        on_click=on_click,
        on_mouse_enter=on_enter,
        on_mouse_leave=on_leave,
    )
