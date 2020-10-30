from middleware.user_statistics import run


async def run_middleware_stack(message):
    await run(message)
