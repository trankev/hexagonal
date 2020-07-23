import abc
import dataclasses
import typing

from hexagonal import services


@dataclasses.dataclass
class Route:
    path: str
    interactor: services.ABBService
    methods: typing.List[str]
    success_code: int = 200


@dataclasses.dataclass
class Resource(abc.ABC):
    name: str

    def iterate_routes(self) -> typing.Iterator[Route]:
        raise NotImplementedError()


@dataclasses.dataclass
class ResourceCollection(Resource):
    list_service: typing.Optional[services.ABBService] = None
    create_service: typing.Optional[services.ABBService] = None
    retrieve_service: typing.Optional[services.ABBService] = None
    update_service: typing.Optional[services.ABBService] = None

    def iterate_routes(self) -> typing.Iterator[Route]:
        if self.list_service:
            yield Route(
                path=f"/{self.name}",
                interactor=self.list_service,
                methods=["GET"],
            )
        if self.create_service:
            yield Route(
                path=f"/{self.name}",
                interactor=self.create_service,
                success_code=201,
                methods=["POST"],
            )
        if self.retrieve_service:
            yield Route(
                path=f"/{self.name}/{{item_id}}",
                interactor=self.retrieve_service,
                success_code=200,
                methods=["GET"],
            )
        if self.update_service:
            yield Route(
                path=f"/{self.name}/{{item_id}}",
                interactor=self.update_service,
                success_code=200,
                methods=["PUT"],
            )


@dataclasses.dataclass
class UniqueResource(Resource):
    retrieve_service: typing.Optional[services.ABBService] = None

    def iterate_routes(self) -> typing.Iterator[Route]:
        if self.retrieve_service:
            yield Route(
                path=f"/{self.name}",
                interactor=self.retrieve_service,
                success_code=200,
                methods=["GET"],
            )
