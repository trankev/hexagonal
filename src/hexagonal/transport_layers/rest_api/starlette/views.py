import typing

from starlette import responses

from hexagonal import interactors
from hexagonal import models
from hexagonal.transport_layers.rest_api import mappings


async def extract_params(request, mapping_list: typing.Sequence[mappings.Mapping]) -> dict:
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
    interactor: interactors.BRBRInteractor,
    tracer,
    *,
    success_code: int = 200,
):
    async def wrapper(request):
        # with tracer.start_active_span(
        #         operation_name=f"rest_api:{interactor.name}",
        #         finish_on_close=True):
        params = await extract_params(request, interactor.rest_api_mapping)
        request = models.Request(
            params=interactor.RequestClass.parse_obj(params)
        )
        response = await interactor.run(request)
        content = response.json()
        return responses.Response(
            content=content,
            media_type="application/json",
            status_code=success_code,
        )

    return wrapper
