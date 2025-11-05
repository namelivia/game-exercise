from typing import TYPE_CHECKING, List

from engine.features.render.ui_element import UIElementRender

from .logic import UIElementLogic
from .state import UIElementState
from .ui import UIElement

if TYPE_CHECKING:
    from engine.primitives.shape import Shape


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
