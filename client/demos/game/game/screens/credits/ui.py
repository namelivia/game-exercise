from engine.api import Text, UIBuilder, create_ui_element


def create_credits():
    return create_ui_element([Text("Credits", 100, 100), Text("@namelivia", 100, 150)])


def create_background():
    return UIBuilder(x=0, y=0).with_image("assets/images/background4.png").build()
