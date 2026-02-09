from __future__ import annotations

import sys
import os
import time


""" Get the absolute path of the folder containing main.py """
root_folder = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)  # path/to/project_root

""" Add that folder to the list of places Python looks for modules """
if root_folder not in sys.path:
    sys.path.insert(0, root_folder)
    # adds root_folder to start of sys.path list, so it gets prioritised while looking at imports


if __name__ == "__main__":
    from pub_sub.controller.kafka_controller import KafkaController
    from pub_sub.models.message import Message
    from pub_sub.models.topic import Topic
    from pub_sub.publisher.publisher import IPublisher, SimplePublisher
    from pub_sub.subscriber.subscriber import ISubscriber, SimpleSubscriber

    kafkaController: KafkaController = KafkaController()

    # // Create topics.
    topic1: Topic = kafkaController.create_topic("Topic1")
    topic2: Topic = kafkaController.create_topic("Topic2")

    # // Create subscribers.
    subscriber1: ISubscriber = SimpleSubscriber()
    subscriber2: ISubscriber = SimpleSubscriber()
    subscriber3: ISubscriber = SimpleSubscriber()

    # // Subscribe: subscriber1 subscribes to both topics,
    # // subscriber2 subscribes to topic1, and subscriber3 subscribes to topic2.
    kafkaController.subscribe(subscriber1, topic1.get_id())
    kafkaController.subscribe(subscriber2, topic1.get_id())

    kafkaController.subscribe(subscriber1, topic2.get_id())
    kafkaController.subscribe(subscriber3, topic2.get_id())

    # // Create publishers.
    publisher1: IPublisher = SimplePublisher(kafkaController)
    publisher2: IPublisher = SimplePublisher(kafkaController)

    # // Publish some messages.
    publisher1.publish(topic1.get_id(), Message("Message m1"))
    publisher1.publish(topic1.get_id(), Message("Message m2"))
    publisher2.publish(topic2.get_id(), Message("Message m3"))
    # // Allow time for subscribers to process messages.
    # try:
    time.sleep(5)
    # except Exception as e:
    #     e.printStackTrace();
    # }
    print("\n\n\n")
    publisher2.publish(topic2.get_id(), Message("Message m4"))
    publisher1.publish(topic1.get_id(), Message("Message m5"))

    # // Reset offset for subscriber1 on topic1 (for example, to re-process messages).
    kafkaController.resetOffset(topic1.get_id(), subscriber1, 0)

    # // Allow some time before shutting down.
    # try:
    print("before final sleep")
    time.sleep(5)
    print("after final sleep")
    # } catch (InterruptedException e) {
    #     e.printStackTrace();
    # }
    kafkaController.shutdown()
