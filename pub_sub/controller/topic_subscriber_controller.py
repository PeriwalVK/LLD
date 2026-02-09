from pub_sub.models.message import Message
from pub_sub.models.topic import Topic
from pub_sub.models.topic_subscriber import TopicSubscriber
from pub_sub.subscriber.subscriber import ISubscriber


class TopicSubscriberController:
    def __init__(self, topic_subscriber: TopicSubscriber):
        self.topicSubscriber: TopicSubscriber = topic_subscriber
        # self._condition = self.topicSubscriber.get_condition()
        # self._lock = threading.Lock()

    def run(self):
        topic: Topic = self.topicSubscriber.topic
        subscriber: ISubscriber = self.topicSubscriber.subscriber
        # condition: threading.Condition = self.topicSubscriber.fetch_condition()
        while True:
            messageToProcess: Message = None
            # with self._condition:
            with self.topicSubscriber.get_condition():
                # // Wait until there is a new message (offset is less than the number of messages)
                while self.topicSubscriber.offset.value >= topic.get_messages_count():
                    try:
                        # self._condition.wait()
                        self.topicSubscriber.get_condition().wait()
                    except InterruptedError as e:
                        # threading.current_thread().interrupt()
                        return

                # // Retrieve the next message and increment the offset
                currentOffset: int = self.topicSubscriber.offset.getAndIncrement()
                messageToProcess = topic.get_message(currentOffset)

            # // Process the message outside of the synchronized block
            # or can also be done in a separate thread
            try:
                subscriber.on_message(messageToProcess)
            except InterruptedError as e:
                # threading.current_thread().interrupt()
                return
