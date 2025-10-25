from abc import ABC
from typing import TYPE_CHECKING, Any, Dict, List, Tuple

from client.engine.features.render.temp import UIElementRender
from client.engine.features.user_input.mouse_position import MousePosition

if TYPE_CHECKING:
    from client.engine.primitives.shape import Shape


# A UI Element can accept any custom logic
# right now custom logics are re-definitions of the update
# function
def create_ui_element(shapes: List["Shape"], state=None, custom_logic=None):
    if state is None:
        state = UIElementState(0, 0)
    if custom_logic is None:
        logic = UIElementLogic(state)
    else:
        logic = custom_logic
    render = UIElementRender(state, shapes)
    return UIElement(render, logic)


# This is the logic part of the UIElement
# UI elements can hold a small state too that can be updated
# This is what will be extended.
class UIElementLogic(ABC):
    def __init__(self, state):
        self.state = state

    def update(self, time: int, data: Dict[str, Any]) -> None:
        pass


class UIElementState(ABC):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_index(self):
        return 0

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y


class AnimationState(UIElementState):
    def __init__(self, x, y, animations, fps):
        super().__init__(x, y)
        self.playing = True
        self.animations = animations
        self.current_animation = list(self.animations.keys())[0]
        self.index = 0
        self.frame_counter = 0
        actual_frame_rate = 60  # This is a constant, same as in the render thread
        self.frame_delay = actual_frame_rate / fps
        print(self.frame_delay)

    def play(self):
        self.playing = True

    def stop(self):
        self.playing = False

    def get_index(self):
        current_index = self.animations[self.current_animation][self.index]
        # Update the frame after providing one to avoid
        # frame skipping
        if self.playing:
            if self.frame_counter == self.frame_delay:
                animation_keys = self.animations[self.current_animation]
                self.index = (self.index + 1) % len(animation_keys)
                self.frame_counter = 0
            else:
                self.frame_counter += 1
        return current_index

    def get_animations(self):
        return list(self.animations.keys())

    def set_animation(self, new_animation):
        self.current_animation = new_animation
        self.index = 0


# The UI Element has three parts, the logic part, the
# render part, and the shared state between the two, it currently only holds
# the coordinates.
class UIElement(ABC):
    def __init__(self, render, logic) -> None:
        self.render = render
        self.logic = logic

    def get_render(self) -> UIElementRender:
        return self.render

    def get_logic(self) -> UIElementLogic:
        return self.logic

    def update(self, time: int, data: Dict[str, Any]) -> None:
        self.logic.update(time, data)


class ClickableUIElement:
    def __init__(
        self,
        element: "UIElement",
        on_click=None,
        on_mouse_enter=None,
        on_mouse_leave=None,
    ) -> None:
        self.element = element
        self.mouse_over = False
        self._was_mouse_over = False
        self.on_click = on_click
        self.on_mouse_enter = on_mouse_enter
        self.on_mouse_leave = on_mouse_leave

    def _is_mouse_over(self, x: int, y: int) -> bool:
        return self.element.get_render().contains_point(x, y)

    def clicked(self):
        if self.on_click is not None:
            self.on_click()

    def update(self, time: int, data: Dict[str, Any]) -> None:
        self.element.update(time, data)
        self._was_mouse_over = self.mouse_over
        mouse_position = MousePosition().get()
        self.mouse_over = self._is_mouse_over(mouse_position[0], mouse_position[1])
        if not self._was_mouse_over and self.mouse_over:
            if self.on_mouse_enter is not None:
                self.on_mouse_enter()
        elif self._was_mouse_over and not self.mouse_over:
            if self.on_mouse_leave is not None:
                self.on_mouse_leave()

    def render(self, window: Any) -> None:
        self.element.get_render().render(window)

    def load(self) -> None:
        self.element.get_render().load()

    def show(self) -> None:
        self.element.get_render().show()

    def get_render(self) -> UIElementRender:
        return self.element.get_render()

    def get_logic(self) -> UIElementLogic:
        return self.element.get_logic()
