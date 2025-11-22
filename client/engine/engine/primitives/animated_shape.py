from .shape import Shape


class AnimatedShape(Shape):
    def __init__(self, x, y, animations, fps):
        super().__init__(x, y)
        self.playing = True
        self.animations = animations
        self.current_animation = list(self.animations.keys())[0]
        self.index = 0
        self.frame_counter = 0
        actual_frame_rate = 60  # This is a constant, same as in the render thread
        self.frame_delay = actual_frame_rate / fps

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
