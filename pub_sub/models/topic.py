import copy
import threading
from typing import List

from pub_sub.models.message import Message


class Topic:
    _id = 1

    def __init__(self, name: str):
        self.id = f"Topic{Topic._id}"
        Topic._id += 1
        self.name: str = name
        self.messages: List[Message] = []

        self._lock = threading.Lock()

    def get_id(self):
        return self.id

    def add_message(self, message: Message):
        with self._lock:
            self.messages.append(message)

    def get_messages_count(self) -> int:
        with self._lock:
            return len(self.messages)

    def get_message(self, offset: int) -> Message:
        with self._lock:
            if offset >= 0 and offset < len(self.messages):
                return self.messages[offset]
            else:
                raise IndexError(f"offset {offset} out of range")

    def get_messages(self) -> List[Message]:
        """
        Returns a list of all messages associated with this topic.
        The returned list is a copy of the internal list, so
        modifying it will not affect the topic's internal state.
        """

        with self._lock:
            return copy.deepcopy(self.messages)
