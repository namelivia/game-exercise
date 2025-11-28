from typing import Any, Dict

from engine.api import EnableUserInput, ShowCursor, UIBuilder, UIElementLogic


class OverlayCustomLogic(UIElementLogic):

    DURATION = 2500

    def update(self, time: int, data: Dict[str, Any]) -> None:
        progress = time / OverlayCustomLogic.DURATION

        if progress > 1.0:
            progress = 1.0
            self.enabled = False
            EnableUserInput().execute()
            ShowCursor().execute()

        opacity = 1.0 - progress
        self.state.set_opacity(opacity)


def create_overlay():
    return (
        UIBuilder(x=0, y=0)
        .with_rectangle(0, 0, 640, 480, (0, 0, 0))
        .with_logic(OverlayCustomLogic)
        .build()
    )
