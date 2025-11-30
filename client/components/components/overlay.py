from typing import Any, Dict

from engine.api import (
    AnimationFinished,
    EnableUserInput,
    ShowCursor,
    UIBuilder,
    UIElementLogic,
)


class FadeInCustomLogic(UIElementLogic):

    DURATION = 2500

    def update(self, time: int, data: Dict[str, Any]) -> None:
        progress = time / FadeInCustomLogic.DURATION

        if progress > 1.0:
            progress = 1.0
            self.enabled = False
            AnimationFinished("fade_in").execute()

        opacity = 1.0 - progress
        self.state.set_opacity(opacity)


def create_fade_in():
    return (
        UIBuilder(x=0, y=0)
        .with_rectangle(0, 0, 640, 480, (0, 0, 0))
        .with_logic(FadeInCustomLogic)
        .build()
    )
