import enum
import typing

import pydantic


class MessageLevel(enum.Enum):
    trace = "trace"
    info = "info"
    warning = "warning"
    error = "error"
    fatal = "fatal"


class Message(pydantic.BaseModel):
    code: str
    severity: MessageLevel
    title: str
    source: typing.Optional[str]


def parse_errors(errors: typing.Sequence[dict]) -> typing.Iterator[Message]:
    for error in errors:
        source_path = "/".join(("", ) + error["loc"])
        yield field_error(error["msg"], source_path)


def field_error(title: str, source: str) -> Message:
    return Message(
        severity=MessageLevel.error,
        code="input_error",
        title=title,
        source=source,
    )
