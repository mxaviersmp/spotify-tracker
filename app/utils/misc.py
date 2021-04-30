from typing import Any, Optional, Text

import httpx
from httpx._types import (
    CookieTypes,
    HeaderTypes,
    QueryParamTypes,
    RequestData,
    RequestFiles,
    URLTypes,
)

DEFAULT_TIMEOUT = httpx.Timeout(timeout=10)


async def async_request(
    method: Text,
    url: URLTypes,
    params: QueryParamTypes = None,
    data: RequestData = None,
    files: RequestFiles = None,
    json: Any = None,
    headers: HeaderTypes = None,
    cookies: CookieTypes = None,
    timeout: Optional[int] = DEFAULT_TIMEOUT
):
    """
    Makes an asynchronous request.

    DEFAULT_TIMEOUT is 10 secongs.
    """
    if isinstance(timeout, int):
        timeout = httpx.Timeout(timeout=timeout)
    async with httpx.AsyncClient(
        cookies=cookies,
        timeout=timeout
    ) as client:
        return await client.request(
            method=method,
            url=url,
            params=params,
            data=data,
            files=files,
            json=json,
            headers=headers
        )
