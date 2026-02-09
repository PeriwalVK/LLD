from abc import ABC, abstractmethod
import time
from typing import override

from pub_sub.constants import SUBSCRIBER_TABS
from pub_sub.models.message import Message


class ISubscriber(ABC):
    _id = 1

    @abstractmethod
    def __init__(self):
        self.id = f"Subscriber{ISubscriber._id}"
        ISubscriber._id += 1

    def get_id(self):
        return self.id

    @abstractmethod
    def on_message(self, message: Message):
        # does not consume message from a topic
        # but just processing (i.e. telling what to do with a message)
        raise NotImplementedError


class SimpleSubscriber(ISubscriber):
    @override
    def __init__(self):
        super().__init__()

    @override
    def on_message(self, message: Message):
        prefix = f"{SUBSCRIBER_TABS}[subscriber-{self.get_id()}]"
        print(f"{prefix}: received message: {message}")
        time.sleep(0.5)
        print(f"{prefix}: processed message: {message}")
