import logging

from starlette import responses

from hexagonal import interactors


def simple_view(
        interactor: interactors.Interactor,
        tracer,
        *,
        success_code: int = 200,
):
    async def wrapper(request):
        span = tracer.start_span(operation_name=f"rest_api:{interactor.name}")
        response = await interactor.run()
        span.finish()
        content = response.json()
        return responses.Response(
            content=content,
            media_type="application/json",
            status_code=success_code,
        )
    return wrapper
