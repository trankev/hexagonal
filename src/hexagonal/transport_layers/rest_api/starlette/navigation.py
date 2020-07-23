import typing

import pydantic
from starlette import requests
from starlette import responses

from hexagonal.models import ports
from hexagonal.transport_layers.rest_api import api


class NavigationResponse(pydantic.BaseModel):
    links: typing.List[ports.Link]


def view(
    api_obj: api.API,
) -> typing.Callable[[requests.Request], typing.Awaitable[responses.Response]]:

    async def wrapper(request: requests.Request) -> responses.Response:
        response = ports.Response(
            data=NavigationResponse(
                links=[
                    ports.Link(
                        name=resource.name,
                        href=request.url_for(resource.main_route_id()),
                    ) for resource in api_obj.resources
                ],
            ),
            messages=[],
        )
        return responses.Response(
            response.json(),
            media_type="application/json",
        )

    return wrapper
