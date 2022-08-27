from unittest import TestCase
from client.engine.general_state.queue import Queue


class TestQueue(TestCase):
    def setUp(self):
        self.queue = Queue()

    def test_empty_pop(self):
        assert self.queue.empty() is True
        # Empty pop returns None
        assert self.queue.pop() is None

    def test_fifo_put_pop(self):
        # Put and pop elements in FIFO order
        assert self.queue.empty() is True
        data_1 = "sample_data_1"
        self.queue.put(data_1)
        data_2 = "sample_data_2"
        self.queue.put(data_2)
        assert self.queue.empty() is False
        assert self.queue.pop() == data_1
        assert self.queue.pop() == data_2
        assert self.queue.empty() is True
