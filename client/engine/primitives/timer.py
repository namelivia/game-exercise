class Timer:
    def __init__(self, time, callback):
        self.time = time
        self.executed = False
        self.callback = callback

    def update(self):
        if self.time > 0:
            self.time -= 1
        else:
            if not self.executed:
                self.callback()
                self.executed = True
