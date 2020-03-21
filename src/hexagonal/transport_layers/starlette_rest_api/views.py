import logging

from starlette import responses

from hexagonal import interactors


def simple_view(
        interactor: interactors.BRBRInteractor,
        tracer,
        *,
        success_code: int = 200,
):
    async def wrapper(request):
        with tracer.start_active_span(operation_name=f"rest_api:{interactor.name}", finish_on_close=True):
            response = await interactor.run()
        content = response.json()
        return responses.Response(
            content=content,
            media_type="application/json",
            status_code=success_code,
        )
    return wrapper
