from datetime import datetime


class Notification:
    def __init__(self, notification_id: int, user_id: int,
                 message: str):
        self.notification_id = notification_id
        self.user_id = user_id
        self.message = message
        self.is_read = False
        self.create_date = datetime.now()

    def mark_as_read(self) -> None:
        self.is_read = True
