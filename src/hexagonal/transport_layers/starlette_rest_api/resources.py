import typing

from starlette import routing

from hexagonal import interactors
from hexagonal.transport_layers.starlette_rest_api import views


class Resource:
    def __init__(
            self,
            name: str,
            *,
            list_interactor: typing.Optional[interactors.Interactor],
            create_interactor: typing.Optional[interactors.Interactor],
    ) -> None:
        self.name = name
        self.list_interactor = list_interactor
        self.create_interactor = create_interactor

    def iterate_routes(self) -> typing.Iterator[routing.Route]:
        if self.list_interactor:
            yield routing.Route(
                f"/{self.name}",
                views.simple_view(self.list_interactor),
                name=self.list_interactor.name
            )
        if self.create_interactor:
            yield routing.Route(
                f"/{self.name}",
                views.simple_view(self.create_interactor, success_code=201),
                methods=["POST"],
                name=self.create_interactor.name
            )
