import typing

from starlette import routing

from hexagonal.transport_layers.rest_api import api
from hexagonal.transport_layers.rest_api.starlette import views


def create_routes(api_obj: api.API, tracer) -> typing.List[routing.Route]:
    routes = [
        routing.Route(
            route.path,
            views.brbr_view(route.interactor, tracer=tracer, success_code=route.success_code),
            name=route.interactor.name,
            methods=route.methods,
        )
        for resource in api_obj.resources
        for route in resource.iterate_routes()
    ]
    return routes
