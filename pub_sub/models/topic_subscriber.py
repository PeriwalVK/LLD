import threading
from pub_sub.models.topic import Topic
from pub_sub.subscriber.subscriber import ISubscriber
from pub_sub.utility.atomic_integer import AtomicInteger


class TopicSubscriber:
    def __init__(self, topic: Topic, subscriber: ISubscriber):
        self.topic: Topic = topic
        self.subscriber: ISubscriber = subscriber
        self.offset: AtomicInteger = AtomicInteger(0)

        self._condition = threading.Condition()

    def get_condition(self) -> threading.Condition:
        return self._condition
