import dataclasses
import typing

from hexagonal import interactors


@dataclasses.dataclass
class Route:
    path: str
    interactor: interactors.BRBRInteractor
    methods: typing.List[str]
    success_code: int = 200


@dataclasses.dataclass
class Resource:
    name: str
    list_interactor: typing.Optional[interactors.BRBRInteractor] = None
    create_interactor: typing.Optional[interactors.BRBRInteractor] = None
    retrieve_interactor: typing.Optional[interactors.BRBRInteractor] = None
    update_interactor: typing.Optional[interactors.BRBRInteractor] = None

    def iterate_routes(self) -> typing.Iterator[Route]:
        if self.list_interactor:
            yield Route(
                path=f"/{self.name}",
                interactor=self.list_interactor,
                methods=["GET"],
            )
        if self.create_interactor:
            yield Route(
                path=f"/{self.name}",
                interactor=self.create_interactor,
                success_code=201,
                methods=["POST"],
            )
        if self.retrieve_interactor:
            yield Route(
                path=f"/{self.name}/{{item_id}}",
                interactor=self.retrieve_interactor,
                success_code=200,
                methods=["GET"],
            )
        if self.update_interactor:
            yield Route(
                path=f"/{self.name}/{{item_id}}",
                interactor=self.update_interactor,
                success_code=200,
                methods=["PUT"],
            )
