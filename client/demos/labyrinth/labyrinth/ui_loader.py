import json

from engine.api import ChangeCursor, ClickableUIElement, UIBuilder


def _create_background(path):
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

    def on_enter():
        ChangeCursor("HAND").execute()

    def on_leave():
        ChangeCursor("ARROW").execute()

    return ClickableUIElement(
        element=element,
        on_click=lambda *args, **kwargs: None,
        on_mouse_enter=on_enter,
        on_mouse_leave=on_leave,
    )


def _create_clickable_elements(definitions):
    return [_create_clickable_element(definition) for definition in definitions]


def load_ui(json_path):
    with open(json_path, "r") as f:
        scene_data = json.load(f)
        background = _create_background(scene_data["background"])
        clickable_elements = _create_clickable_elements(
            scene_data["clickable_elements"]
        )
        return [background, *clickable_elements]
