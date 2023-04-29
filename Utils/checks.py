def is_blacklisted(func):
    async def decorator(*args, **kwargs):
        print(args, kwargs)
        response = await func(args, kwargs)

    return decorator
