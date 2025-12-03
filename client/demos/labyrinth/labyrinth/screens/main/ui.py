from engine.api import ChangeCursor, ClickableUIElement, UIBuilder


def create_background():
    return UIBuilder(x=0, y=0).with_image("assets/images/test_screen.png").build()


def create_clickable_area_1(on_click):
    element = UIBuilder(x=150, y=148).with_rectangle(0, 0, 69, 237).build()
    element.hide()

    def on_enter():
        ChangeCursor("HAND").execute()

    def on_leave():
        ChangeCursor("ARROW").execute()

    return ClickableUIElement(
        element=element,
        on_click=on_click,
        on_mouse_enter=on_enter,
        on_mouse_leave=on_leave,
    )


def create_clickable_area_2(on_click):
    element = UIBuilder(x=295, y=221).with_rectangle(0, 0, 46, 44).build()
    element.hide()

    def on_enter():
        ChangeCursor("HAND").execute()

    def on_leave():
        ChangeCursor("ARROW").execute()

    return ClickableUIElement(
        element=element,
        on_click=on_click,
        on_mouse_enter=on_enter,
        on_mouse_leave=on_leave,
    )


def create_clickable_area_3(on_click):
    element = UIBuilder(x=433, y=196).with_rectangle(0, 0, 47, 97).build()
    element.hide()

    def on_enter():
        ChangeCursor("HAND").execute()

    def on_leave():
        ChangeCursor("ARROW").execute()

    return ClickableUIElement(
        element=element,
        on_click=on_click,
        on_mouse_enter=on_enter,
        on_mouse_leave=on_leave,
    )


def create_clickable_area_4(on_click):
    element = UIBuilder(x=223, y=407).with_rectangle(0, 0, 198, 80).build()
    element.hide()

    def on_enter():
        ChangeCursor("HAND").execute()

    def on_leave():
        ChangeCursor("ARROW").execute()

    return ClickableUIElement(
        element=element,
        on_click=on_click,
        on_mouse_enter=on_enter,
        on_mouse_leave=on_leave,
    )
