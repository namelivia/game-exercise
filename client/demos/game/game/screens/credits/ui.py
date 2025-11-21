from engine.api import UIBuilder


def create_credits():
    return (
        UIBuilder(x=0, y=0)
        .with_text("Credits", 100, 100)
        .with_text("@namelivia", 100, 150)
        .build()
    )


def create_background():
    return UIBuilder(x=0, y=0).with_image("assets/images/background4.png").build()
