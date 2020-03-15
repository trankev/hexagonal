from starlette import responses

from hexagonal import interactors


def simple_view(service: interactors.Interactor, success_code: int = 200):
    async def wrapper(request):
        response = await service.run()
        content = response.json()
        return responses.Response(
            content=content,
            media_type="application/json",
            status_code=success_code,
        )
    return wrapper
