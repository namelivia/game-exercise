import json

from engine.api import ClickableUIElement, PlaySound, ScreenTransition, UIBuilder
from labyrinth.commands import SetCustomCursor


def on_scene1_left():
    from labyrinth.screens.another.another import AnotherScreen

    ScreenTransition(AnotherScreen).execute()


def on_scene1_forward():
    from labyrinth.screens.another.another import AnotherScreen

    ScreenTransition(AnotherScreen).execute()


def on_scene1_window():
    PlaySound(
        "assets/sounds/window.ogg",
    ).execute()


def on_scene1_back():
    print("I can't go back")


actions = {
    "scene1_left": on_scene1_left,
    "scene1_forward": on_scene1_forward,
    "scene1_window": on_scene1_window,
    "scene1_back": on_scene1_back,
}


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

    def on_click():
        actions[definition["action"]]()

    def on_enter():
        SetCustomCursor(definition["cursor"]).execute()

    def on_leave():
        SetCustomCursor("default").execute()

    return ClickableUIElement(
        element=element,
        on_click=on_click,
        on_mouse_enter=on_enter,
        on_mouse_leave=on_leave,
    )


def _create_clickable_elements(definitions):
    return [_create_clickable_element(definition) for definition in definitions]


def load_ui(json_path):
    with open(json_path, "r") as f:
        scene_data = json.load(f)
        background = _create_background(scene_data["background"])
        try:
            clickable_elements = _create_clickable_elements(
                scene_data["clickable_elements"]
            )
        except KeyError:
            clickable_elements = []
        return [background, *clickable_elements]
