import aiohttp


def default_headers():
    header = {'X-API-KEY': 'f3d5fd72-747b-4f6d-904a-46188d0a9944'}
    return header


class WebSession(object):
    session = None

    @classmethod
    def create(cls):
        cls.session = aiohttp.ClientSession()
        return cls.session

    @classmethod
    def close(cls):
        if cls.session is not None:
            # apparently this is supposed to return a future?
            return cls.session.close()


async def request(method, url, **kwargs):

    if kwargs.get('headers', None) is None:
        kwargs['headers'] = default_headers()

    if WebSession.session is None:
        session = WebSession.create()
    else:
        session = WebSession.session

    return await session.request(method=method, url=url, **kwargs)
