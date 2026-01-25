from datetime import datetime


class RegistrationPeriod:
    def __init__(self, period_id: int, start_date: datetime,
                 end_date: datetime, status: str):
        self.period_id = period_id
        self.start_date = start_date
        self.end_date = end_date
        self.status = status  # open / closed

    def is_open(self) -> bool:
        return self.start_date <= datetime.now() <= self.end_date
