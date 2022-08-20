from queue import SimpleQueue, Empty


class Queue:
    def __init__(self):
        self.data = SimpleQueue()

    def put(self, new_data):
        self.data.put(new_data)

    def empty(self):
        self.data.empty()

    def pop(self):
        try:
            # This is a sync queue because block is False
            return self.data.get(block=False)
        except Empty:
            return None
