import json

from engine.api import (
    ClickableUIElement,
    DisableUserInput,
    HideCursor,
    JSONScreen,
    PlayMusic,
    PlaySound,
    UIBuilder,
)


def create_background(path):
    return UIBuilder(x=0, y=0).with_image(path).build()


ACTION_MAP = {
    "PlayMusic": PlayMusic,
    "PlaySound": PlaySound,
    "DisableUserInput": DisableUserInput,
    "HideCursor": HideCursor,
}


def parse_callbacks(data):
    print(data)
    exit()


def parse_timers(data):
    result = []
    for timer in data:
        delay = timer["delay_ms"]
        callback_name = timer["on_finish_action"]

        # TODO: This requires setting the callbacks first
        # try:
        #    callback_method = getattr(self, action_name)
        # except AttributeError:
        #    print(f"ERROR: Timer action '{action_name}' not found on Screen class.")
        #    continue

        # Create the Timer instance with the delay and the found method
        # new_timer = Timer(delay, callback_method)
        # result.append(new_timer)


def parse_initialize(data):
    result = []
    for action in data:
        command_name = action["command"]
        args = action.get("args", [])

        CommandClass = ACTION_MAP.get(command_name)

        if CommandClass:
            # Instantiate the object using the arguments
            action_instance = CommandClass(*args)
            result.append(action_instance)
        else:
            print(f"Warning: Unknown command '{command_name}' skipped.")
    return result


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
        new_screen = JSONScreen()
        background = create_background(scene_data["background"])
        clickable_elements = create_clickable_elements(scene_data["clickable_elements"])
        new_screen.ui_elements = [background, *clickable_elements]
        new_screen.initial_actions = parse_initialize(scene_data["initial_actions"])
        # Callbacks need to be parsed before timers
        parse_callbacks(scene_data["callbacks"])
        new_screen.timers = parse_timers(scene_data["timers"])

        return new_screen
