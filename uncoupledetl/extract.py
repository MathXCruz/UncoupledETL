from typing import List, Callable, Optional
import asyncio
import httpx


class APIExtractor:
    def __init__(
        self,
        url: str,
        endpoints: List[str],
        params: dict = None,
        headers: dict = None,
    ):
        """Initializes the Extractor.

        Args:
            url (str): The url to extract data from.
            endpoints (List[str], optional): The endpoints where the data is.
            params (dict, optional): The request parameters. Defaults to None.
            headers (dict, optional): The request headers. Defaults to None.
        """
        self.url = url
        self.endpoints = endpoints
        self.params = params
        self.headers = headers

    async def get_data(
        self,
        get_strategy: Callable[
            [str, Optional[List[str]], Optional[dict], Optional[dict]],
            List[dict],
        ],
    ) -> List[dict]:
        """Uses the extraction strategy chosen to extract the data.

        Args:
            get_strategy (Callable[ [str, Optional[List[str]], Optional[dict], Optional[dict]], List[dict] ]): The extraction strategy to use.

        Returns:
            List[dict]: The extracted data.
        """
        return await get_strategy(
            self.url, self.endpoints, self.params, self.headers
        )


async def get_multiple_data(
    url: str, endpoints: List[str], params: dict = None, headers: dict = None
) -> List[dict]:
    """Return the data for multiple endpoints.

    Args:
        url (str): The API base URL.
        endpoints (List[str]): The endpoints where the data is.
        params (dict, optional): Request parameters. Defaults to None.
        headers (dict, optional): Request headers. Defaults to None.

    Returns:
        List[dict]: The raw data returned.
    """
    reqs = [
        httpx.Request(
            'GET', url=f'{url}{endpoint}', params=params, headers=headers
        )
        for endpoint in endpoints
    ]
    req_list = await get_async_data(reqs)
    response = [res.json() for res in req_list]
    return response


async def get_async_data(reqs: List[httpx.Request]) -> List[httpx.Response]:
    """Create a client and manage the creation and execution of the requests.
    Args:
        reqs (List[httpx.Request]): A list of requests to make.
    Returns:
        List[httpx.Response]: A list of responses from the requests.
    """
    limits = httpx.Limits(max_connections=10, max_keepalive_connections=10)
    timeout = httpx.Timeout(60)
    async with httpx.AsyncClient(timeout=timeout, limits=limits) as client:
        tasks = [client.send(req) for req in reqs]
        return await asyncio.gather(*tasks)


async def get_specific_data(
    url: str, endpoint: str, params: dict = None, headers: dict = None
) -> List[dict]:
    """Return the data for a specific endpoint.

    Args:
        url (str): The API base URL.
        endpoint (str): The endpoint where the data is.
        params (dict, optional): Request parameters. Defaults to None.
        headers (dict, optional): Request headers. Defaults to None.

    Returns:
        List[dict]: The raw data returned.
    """
    with httpx.Client(params=params, headers=headers) as client:
        response = client.get(f'{url}{endpoint}')
    return response.json()
