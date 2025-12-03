import json

from engine.api import ClickableUIElement, Screen, UIBuilder


def create_background(path):
    return UIBuilder(x=0, y=0).with_image(path).build()


def _create_clickable_element(definition):
    element = (
        UIBuilder(x=definition["x"], y=definition["y"])
        .with_rectangle(
            0,
            0,
            definition["width"],
            definition["height"],
        )
        .build()
    )
    element.hide()

    return ClickableUIElement(
        element=element,
        on_click=lambda *args, **kwargs: None,
        on_mouse_enter=lambda *args, **kwargs: None,
        on_mouse_leave=lambda *args, **kwargs: None,
    )


def create_clickable_elements(definitions):
    return [_create_clickable_element(definition) for definition in definitions]


def load_screen(json_path):
    with open(json_path, "r") as f:
        scene_data = json.load(f)
        new_screen = Screen()
        background = create_background(scene_data["background"])
        clickable_elements = create_clickable_elements(scene_data["clickable_elements"])
        new_screen.ui_elements = [background, *clickable_elements]

        return new_screen
