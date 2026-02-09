from pub_sub.models.topic import Topic
from pub_sub.publisher.publisher import IPublisher


class TopicPublisher:
    def __init__(self, topic: Topic, publisher: IPublisher):
        self.topic: Topic = topic
        self.publisher: IPublisher = publisher
