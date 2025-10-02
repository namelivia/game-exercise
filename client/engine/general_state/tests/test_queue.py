from unittest import TestCase

from client.engine.general_state.queue import QueueManager


class TestQueueManager(TestCase):
    def setUp(self):
        self.queue = QueueManager()
        self.queue.initialize(None)

    def test_empty_pop(self):
        assert self.queue.main_queue().empty() is True
        # Empty pop returns None
        assert self.queue.main_queue().pop() is None

    def test_fifo_put_pop(self):
        # Put and pop elements in FIFO order
        assert self.queue.main_queue().empty() is True
        data_1 = "sample_data_1"
        self.queue.main_queue().put(data_1)
        data_2 = "sample_data_2"
        self.queue.main_queue().put(data_2)
        assert self.queue.main_queue().empty() is False
        assert self.queue.main_queue().pop() == data_1
        assert self.queue.main_queue().pop() == data_2
        assert self.queue.main_queue().empty() is True
