from datetime import timezone

from sqlalchemy import DateTime
from sqlalchemy.types import TypeDecorator


class UTCDateTime(TypeDecorator):
    impl = DateTime
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return None

        if value.tzinfo is None:
            raise ValueError("Datetime values must include timezone information.")

        return value.astimezone(timezone.utc).replace(tzinfo=None)

    def process_result_value(self, value, dialect):
        if value is None:
            return None

        return value.replace(tzinfo=timezone.utc)
