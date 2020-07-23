import typing

from starlette import routing

from hexagonal.transport_layers.rest_api import api
from hexagonal.transport_layers.rest_api.starlette import navigation
from hexagonal.transport_layers.rest_api.starlette import views


def create_routes(api_obj: api.API) -> typing.List[routing.Route]:
    routes = [
        routing.Route(
            route.path,
            views.abb_view(route.interactor, success_code=route.success_code),
            name=route.interactor.name,
            methods=route.methods,
        ) for resource in api_obj.resources for route in resource.iterate_routes()
    ]
    routes.append(routing.Route(
        "/",
        navigation.view(api_obj),
        name="root",
        methods=["GET"],
    ), )
    return routes
