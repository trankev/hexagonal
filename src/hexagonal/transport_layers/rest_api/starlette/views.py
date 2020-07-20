import json
import typing

import pydantic
from starlette import requests
from starlette import responses

from hexagonal import services
from hexagonal.models import messages
from hexagonal.models import ports
from hexagonal.transport_layers.rest_api import mappings


async def extract_params(
    request: requests.Request,
    mapping_list: typing.Sequence[mappings.Mapping],
) -> typing.Tuple[dict, typing.List[messages.Message]]:
    body = None
    tried_parse_body = False
    params = {}
    errors: typing.List[messages.Message] = []
    for mapping in mapping_list:
        if mapping.source == mappings.Source.path:
            params[mapping.attribute] = request.path_params[mapping.field]
        elif mapping.source == mappings.Source.header:
            try:
                params[mapping.attribute] = request.headers[mapping.field]
            except KeyError:
                error = messages.missing_field(f"/{mapping.field}", "header")
                errors.append(error)
        elif mapping.source == mappings.Source.query:
            params[mapping.attribute] = request.query_params[mapping.field]
        elif mapping.source == mappings.Source.body:
            if body is None:
                if tried_parse_body:
                    error = messages.missing_field(f"/{mapping.field}", "body")
                    errors.append(error)
                    continue
                try:
                    body = await request.json()
                except json.JSONDecodeError:
                    error = messages.missing_field(f"/{mapping.field}", "body")
                    errors.append(error)
                    tried_parse_body = True
                    continue
            params[mapping.attribute] = body[mapping.field]
    return params, errors


def brbr_view(
    interactor: services.ABBService,
    *,
    success_code: int = 200,
) -> typing.Callable[[requests.Request], responses.Response]:

    async def wrapper(request: requests.Request) -> responses.Response:
        params_dict, errors = await extract_params(request, interactor.rest_api_mapping)
        if errors:
            return error_response(errors)
        try:
            params = interactor.RequestClass.parse_obj(params_dict)
        except pydantic.ValidationError as err:
            errors = list(messages.parse_errors(err.errors()))
            return error_response(errors)
        request = ports.Request(params=params)
        response = await interactor.run(request)
        content = response.json()
        return responses.Response(
            content=content,
            media_type="application/json",
            status_code=success_code,
        )

    return wrapper


# Sorted mapping of internal error code to HTTP code
# higher errors in the list will have priority
ERROR_CODES = [
    (400, (messages.ErrorCode.input_error, messages.ErrorCode.missing_field)),
]


def error_response(errors: typing.List[messages.Message]) -> responses.Response:
    status_code = 500
    for http_code, message_codes in ERROR_CODES:
        if any(error.code in message_codes for error in errors):
            status_code = http_code
    response = ports.Response(data=None, messages=errors)
    return responses.JSONResponse(
        content=response.dict(),
        status_code=status_code,
    )
