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
) -> dict:
    body = None
    params = {}
    for mapping in mapping_list:
        if mapping.source == mappings.Source.path:
            params[mapping.attribute] = request.path_params[mapping.field]
        elif mapping.source == mappings.Source.header:
            params[mapping.attribute] = request.headers[mapping.field]
        elif mapping.source == mappings.Source.query:
            params[mapping.attribute] = request.query_params[mapping.field]
        elif mapping.source == mappings.Source.body:
            if body is None:
                body = await request.json()
            params[mapping.attribute] = body[mapping.field]
    return params


def brbr_view(
    interactor: services.ABBService,
    *,
    success_code: int = 200,
) -> typing.Callable[[requests.Request], responses.Response]:

    async def wrapper(request: requests.Request) -> responses.Response:
        params_dict = await extract_params(request, interactor.rest_api_mapping)
        try:
            params = interactor.RequestClass.parse_obj(params_dict)
        except pydantic.ValidationError as err:
            errors = list(messages.parse_errors(err.errors()))
            response = ports.Response(data=None, messages=errors)
            return responses.Response(
                content=response.json(),
                media_type="application/json",
                status_code=400,  # TODO: proper status code
            )
        request = ports.Request(params=params)
        response = await interactor.run(request)
        content = response.json()
        return responses.Response(
            content=content,
            media_type="application/json",
            status_code=success_code,
        )

    return wrapper
