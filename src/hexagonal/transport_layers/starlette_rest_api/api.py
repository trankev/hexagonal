import typing

from starlette import routing

from hexagonal.transport_layers.starlette_rest_api import resources


def create(resources: typing.Sequence[resources.Resource]) -> typing.List[routing.BaseRoute]:
    routes = [
        route
        for resource in resources
        for route in resource.iterate_routes()
    ]
    return routes
