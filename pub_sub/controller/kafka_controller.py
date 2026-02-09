from concurrent.futures import ThreadPoolExecutor
from typing import List
from pub_sub.constants import SUBSCRIBER_TABS
from pub_sub.controller.topic_subscriber_controller import TopicSubscriberController
from pub_sub.models.message import Message
from pub_sub.models.topic import Topic
from pub_sub.models.topic_subscriber import TopicSubscriber
from pub_sub.publisher.publisher import IPublisher
from pub_sub.subscriber.subscriber import ISubscriber
from pub_sub.utility.concurrent_hashmap import ConcurrentHashMap
from pub_sub.utility.threadsafe_list import ThreadSafeList


class KafkaController:
    def __init__(self):

        # // Map of topic IDs to Topic objects.
        self.topics = ConcurrentHashMap[str, Topic]()

        # // Map of topic IDs to their list of TopicSubscriber associations.
        self.topics_subscribers = ConcurrentHashMap[
            str, ThreadSafeList[TopicSubscriber]
        ]()

        # // ExecutorService to run subscriber tasks concurrently.
        self.subscriber_executor = ThreadPoolExecutor()

    def create_topic(self, topic_name: str) -> Topic:
        topic = Topic(topic_name)
        topic_id = topic.get_id()
        self.topics.set(topic_id, topic)
        self.topics_subscribers.set(topic_id, ThreadSafeList[TopicSubscriber]())
        print(f"Created topic: {topic_name} with id: {topic_id}")
        return topic

    def subscribe(self, subscriber: ISubscriber, topic_id: str):
        prefix = f"{SUBSCRIBER_TABS}[subscriber-{subscriber.get_id()}]"

        if not self.topics.contains_key(topic_id):
            print(f"""Topic {topic_id} does not exist""")
            return None

        topic: Topic = self.topics.get(topic_id)
        topic_subscriber = TopicSubscriber(topic, subscriber)
        self.topics_subscribers.get(topic_id).append(topic_subscriber)
        topic_subscriber_controller = TopicSubscriberController(topic_subscriber)
        # Submit the subscriber task to the executor
        self.subscriber_executor.submit(topic_subscriber_controller.run)

        print(f"""{prefix}: subscribed to topic {topic_id}""")

    def publish(self, publisher: IPublisher, topic_id: str, message: Message) -> None:
        if not self.topics.contains_key(topic_id):
            print(f"""Topic {topic_id} does not exist""")
            return None

        topic: Topic = self.topics.get(topic_id)
        topic.add_message(message)

        # // wake up each subscriber on its own monitor
        subs_snapshot: List[TopicSubscriber] = self.topics_subscribers.get(
            topic_id
        ).snapshot()
        for topicSubscriber in subs_snapshot:
            cond_ = topicSubscriber.get_condition()
            with cond_:
                cond_.notify()

        print(f"""Message "{message.get_message()}" published to topic: {topic.name}""")

    # // Resets the offset for the given subscriber on the specified topic.
    def resetOffset(self, topicId: str, subscriber: ISubscriber, newOffset: int):
        subscribers: List[TopicSubscriber] = self.topics_subscribers.get(
            topicId
        ).snapshot()
        if subscribers is None:
            print(f"Topic with id {topicId} does not exist")
            return

        print("here 1")
        for ts in subscribers:
            print("here 2")
            if ts.subscriber.get_id() == subscriber.get_id():
                print("here 3")
                ts.offset.set(newOffset)
                print("here 4")
                # // Notify in case the subscriber thread is waiting.

                _cond = ts.get_condition()
                print("here 5")
                with _cond:
                    print("here 6")
                    _cond.notify()
                    print("here 7")
                print(
                    f"Offset for subscriber {subscriber.get_id()} on topic {ts.topic.name} reset to {newOffset}"
                )
                break

    # // Shutdown the ExecutorService gracefully.
    def shutdown(self):
        self.subscriber_executor.shutdown(wait=False, cancel_futures=True)
        # try:
        #     self.subscriber_executor.shutdown(wait=True, cancel_futures=True)
        # except TimeoutError:
        #     print("Timeout occurred while shutting down executor.")
        #     self.subscriber_executor.shutdown(wait=False, cancel_futures=True)
        # except KeyboardInterrupt:
        #     print("Keyboard interrupt occurred while shutting down executor.")
        #     self.subscriber_executor.shutdown(wait=False, cancel_futures=True)
        #     raise

        print("IN THE END...")
