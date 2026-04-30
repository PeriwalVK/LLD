from abc import ABC, abstractmethod


# -----------------------------
# Core Models
# -----------------------------

class Notification:
    def __init__(self, user_id: int, message: str):
        self.user_id = user_id
        self.message = message


class NotificationEvent:
    """
    Represents a business event like ORDER_PLACED, PAYMENT_FAILED etc.  
    """
    def __init__(self, user_id: int, event_type: str, data: dict):
        self.user_id = user_id
        self.event_type = event_type
        self.data = data


# -----------------------------
# Channel Strategy
# -----------------------------

class NotificationChannel(ABC):

    @abstractmethod
    def send(self, notification: Notification):
        pass


class EmailChannel(NotificationChannel):

    def send(self, notification: Notification):
        print(f"[EMAIL] -> User {notification.user_id}: {notification.message}")


class SMSChannel(NotificationChannel):

    def send(self, notification: Notification):
        print(f"[SMS] -> User {notification.user_id}: {notification.message}")


class PushChannel(NotificationChannel):

    def send(self, notification: Notification):
        print(f"[PUSH] -> User {notification.user_id}: {notification.message}")


# -----------------------------
# Template Service
# -----------------------------

class TemplateService:
    """
    Responsible for rendering templates based on event + channel
    """

    def __init__(self):
        self.templates = {
            ("ORDER_PLACED", "email"):
                "Hi {name}, your order {order_id} is confirmed.",
            ("ORDER_PLACED", "sms"):
                "Order {order_id} confirmed.",
            ("ORDER_PLACED", "push"):
                "🎉 Order {order_id} placed successfully!",
        }

    def render(self, event_type: str, channel: str, data: dict) -> str:
        template = self.templates.get((event_type, channel))

        if not template:
            raise Exception(f"No template for {event_type} on {channel}")

        return template.format(**data)


# -----------------------------
# User Preference Service
# -----------------------------

class UserPreferenceService:
    """
    Stores which channels a user prefers for each event
    """

    def __init__(self):
        self.preferences = {
            101: {
                "ORDER_PLACED": ["email", "push"],
            },
            102: {
                "ORDER_PLACED": ["sms"],
            }
        }

    def get_enabled_channels(self, user_id: int, event_type: str):
        return self.preferences.get(user_id, {}).get(event_type, [])


# -----------------------------
# Notification Service (Orchestrator)
# -----------------------------

class NotificationService:

    def __init__(self, template_service: TemplateService,
                 preference_service: UserPreferenceService):
        self.template_service = template_service
        self.preference_service = preference_service
        self.channels = {}

    def register_channel(self, name: str, channel: NotificationChannel):
        self.channels[name] = channel

    def notify(self, event: NotificationEvent):

        # Step 1: Get user preferred channels
        channels = self.preference_service.get_enabled_channels(
            event.user_id,
            event.event_type
        )

        if not channels:
            print(f"No channels enabled for user {event.user_id}")
            return

        # Step 2: For each channel → render template → send
        for channel_name in channels:

            if channel_name not in self.channels:
                print(f"Channel {channel_name} not registered")
                continue

            try:
                message = self.template_service.render(
                    event.event_type,
                    channel_name,
                    event.data
                )

                notification = Notification(event.user_id, message)

                self.channels[channel_name].send(notification)

            except Exception as e:
                print(f"Failed for {channel_name}: {e}")


# -----------------------------
# Example Usage
# -----------------------------

if __name__ == "__main__":

    # Initialize services
    template_service = TemplateService()
    preference_service = UserPreferenceService()

    notification_service = NotificationService(
        template_service,
        preference_service
    )

    # Register channels
    notification_service.register_channel("email", EmailChannel())
    notification_service.register_channel("sms", SMSChannel())
    notification_service.register_channel("push", PushChannel())

    # Create event
    event = NotificationEvent(
        user_id=101,
        event_type="ORDER_PLACED",
        data={
            "name": "Rahul",
            "order_id": "1234"
        }
    )

    # Trigger notification
    notification_service.notify(event)