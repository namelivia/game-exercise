from animal_sounds.images import BACKGROUND
from engine.features.game_logic.commands import ChangeCursor
from engine.graphics.shapes import Image
from engine.primitives.ui import ClickableUIElement, create_ui_element


def create_background():
    return create_ui_element([Image(BACKGROUND, 0, 0)])


def _create_portrait_enter_handler(image, highlight):
    def handle_enter():
        ChangeCursor("HAND").execute()
        highlight.show()
        image.hide()

    return handle_enter


def _create_portrait_leave_handler(image, highlight):
    def handle_leave():
        ChangeCursor("ARROW").execute()
        highlight.hide()
        image.show()

    return handle_leave


def create_portrait(image_path: str, highlight_path: str, x: int, y: int, on_click):
    default_image = Image(image_path, x, y)
    highlight_image = Image(highlight_path, x, y)
    highlight_image.hide()

    core_element = create_ui_element([default_image, highlight_image])

    enter_cb = _create_portrait_enter_handler(default_image, highlight_image)
    leave_cb = _create_portrait_leave_handler(default_image, highlight_image)

    return ClickableUIElement(
        element=core_element,
        on_click=on_click,
        on_mouse_enter=enter_cb,
        on_mouse_leave=leave_cb,
    )
