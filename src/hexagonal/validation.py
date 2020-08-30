import typing

import pydantic

from hexagonal.models import messages
from hexagonal.models import ports


def validate(model: typing.Type[pydantic.BaseModel], fields: dict) -> pydantic.BaseModel:
    try:
        obj = model.parse_obj(fields)
    except pydantic.ValidationError as err:
        errors = list(parse_errors(err.errors()))
        raise ports.Error(errors)
    return obj


def parse_errors(errors: typing.Sequence[dict]) -> typing.Iterator[messages.Message]:
    for error in errors:
        source_path = "/" + "/".join(str(excerpt) for excerpt in error["loc"])
        yield messages.field_error(error["msg"], source_path)
