from pub_sub.controller.kafka_controller import KafkaController
from pub_sub.models.message import Message
from pub_sub.models.topic_publisher import TopicPublisher


class TopicPublisherController:
    def __init__(self, topic_publisher: TopicPublisher):
        self._topic_publisher: TopicPublisher = topic_publisher

    def publish(self, message: Message, kafka_controller: KafkaController) -> None:
        kafka_controller.publish(
            self._topic_publisher.publisher,
            self._topic_publisher.topic.get_id(),
            message,
        )
        print(
            f"Publisher {self._topic_publisher.publisher.get_id()} published to topic {self._topic_publisher.topic.name}"
        )
