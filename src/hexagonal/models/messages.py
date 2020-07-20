import enum
import typing
import uuid

import pydantic


class MessageLevel(enum.Enum):
    trace = "trace"
    info = "info"
    warning = "warning"
    error = "error"
    fatal = "fatal"


class ErrorCode(enum.Enum):
    input_error = "input_error"
    missing_field = "missing_field"
    resource_not_found = "resource_not_found"


class Message(pydantic.BaseModel):
    code: ErrorCode
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
        code=ErrorCode.input_error,
        title=title,
        source=source,
    )


def missing_field(source: str, location: str) -> Message:
    return Message(
        severity=MessageLevel.error,
        code=ErrorCode.missing_field,
        title=f"missing value from {location}",
        source=source,
    )


def resource_not_found(resource_name: str, resource_id: uuid.UUID) -> Message:
    return Message(
        severity=MessageLevel.error,
        code=ErrorCode.resource_not_found,
        title=f"can not find {resource_name} with id {resource_id}",
        source=None,
    )
