from pusher import Pusher
from decouple import config


class RealTimeService:
    def __init__(self) -> None:
        self.pusher = Pusher(
            app_id=config("PUSHER_APP_ID"),
            key=config("PUSHER_KEY"),
            secret=config("PUSHER_SECRET"),
            cluster=config("PUSHER_CLUSTER"),
        )

    def push_event_to_frontend(self, channel, event_name, data):
        self.pusher.trigger(channel, event_name, data)
