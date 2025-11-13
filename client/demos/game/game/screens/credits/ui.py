from engine.api import Image, Text, create_ui_element


def create_credits():
    return create_ui_element([Text("Credits", 100, 100), Text("@namelivia", 100, 150)])


def create_background():
    return create_ui_element([Image("assets/images/background4.png", 0, 0)])
