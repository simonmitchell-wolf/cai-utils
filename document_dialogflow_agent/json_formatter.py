import datetime as dt
import json
import logging
from typing import Optional, override

class JSONFormatter(logging.Formatter):

    LOG_RECORD_BUILTIN_ATTRS = [
        "name",
        "msg",
        "levelname",
        "levelno",
        "pathname"
        "filename",
        "module",
        "exc_infonfo",
        "exc_text",
        "stack_info",
        "lineno",
        "funcName",
        "created",
        "message",
        "timestamp",
        "name",
        "module",
        "funcName",
        "lineno",
        "threadName",
    ]

    def __init__(
        self,
        *,
        fmt_keys: Optional[dict[str, str]] = None
    ) -> None:
        super().__init__()
        self.fmt_keys = fmt_keys if fmt_keys is not None else {}

    @override
    def format(self, record: logging.LogRecord) -> str:
        message = self._prepare_log_dict(record)
        return json.dumps(message, default=str)

    def _prepare_log_dict(self, record: logging.LogRecord):
        always_fields = {
            "message": record.getMessage(),
            "timestamp": dt.datetime.fromtimestamp(
                record.created, tz=dt.timezone.utc
            ).isoformat(),
        }
        if record.exc_info is not None:
            always_fields["exc_info"] = self.formatException(record.exc_info)
        
        if record.stack_info is not None:
            always_fields["stack_info"] = self.formatStack(record.stack_info)

        message = {
            key: msg_val
            if (msg_val := always_fields.pop(val, None)) is not None
            else getattr(record, val)
            for key, val in self.fmt_keys.items()
        }
        message.update(always_fields)

        for key, val in record.__dict__.items():
            if key not in self.LOG_RECORD_BUILTIN_ATTRS:
                message[key] = val

        return message