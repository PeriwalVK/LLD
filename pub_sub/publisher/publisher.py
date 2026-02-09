from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pub_sub.controller.kafka_controller import KafkaController
from pub_sub.models.message import Message


class IPublisher(ABC):
    _id = 1

    def __init__(self):
        self.id = f"Publisher{IPublisher._id}"
        IPublisher._id += 1

    @abstractmethod
    def publish(self, topic_id: str, message: Message):
        raise NotImplementedError

    def get_id(self):
        return self.id


class SimplePublisher(IPublisher):
    def __init__(self, kafkaController: KafkaController):
        super().__init__()
        self._kafkaController: KafkaController = kafkaController

    def publish(self, topic_id: str, message: Message):
        self._kafkaController.publish(self, topic_id, message)
        print(
            f"publisher: {self.get_id()} publishing to topic {topic_id}, message: {message}"
        )
