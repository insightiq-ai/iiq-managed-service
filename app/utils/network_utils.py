import logging
from http import HTTPStatus
from typing import Optional, Union, Dict

from fastapi import HTTPException
from httpx import Response, AsyncClient, BasicAuth, HTTPStatusError

from app.utils.constants import EXTERNAL_CALLS_CONNECT_TIMEOUT_IN_SECONDS, Content_Type, APPLICATION_JSON
from app.utils.exceptions import TooManyRequestException


async def invoke_get_url(url: str, headers: Optional[Dict] = None, query: Optional[Dict] = None,
                         auth: Optional[BasicAuth] = None) -> dict:
    response: Response = await invoke_get_url_and_respond_raw(url=url, query=query, headers=headers, auth=auth)

    if response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
        raise TooManyRequestException(message=response.text)
    return response.json()


async def invoke_get_url_and_respond_raw(url: str, headers: Optional[Dict] = None, query: Optional[Dict] = None,
                                         auth: Optional[BasicAuth] = None) -> Response:
    logging.info(f"url: GET {url} query: {query} headers: {headers}")
    async with AsyncClient() as client:
        response: Response = await client.get(url=url, params=query, headers=headers, auth=auth,
                                              follow_redirects=True, timeout=EXTERNAL_CALLS_CONNECT_TIMEOUT_IN_SECONDS)
        logging.info(f"status: {response.status_code} response: {response.text}")

        if response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
            raise TooManyRequestException(message=response.text)
        try:
            response.raise_for_status()
        except HTTPStatusError as e:
            if e and hasattr(e, "response"):
                if hasattr(e.response, "status_code") and hasattr(e.response, "text"):
                    raise HTTPException(status_code=e.response.status_code, detail=e.response.json())
        return response


async def invoke_put_url(url: str, body: Union[str, dict], headers: dict, query: Optional[dict] = None,
                         auth=None) -> dict:
    logging.info(f"url: PUT {url} body: {body} headers: {headers} query: {query}")
    async with AsyncClient() as client:
        response: Response = await client.put(url=url, data=body, params=query, headers=headers, auth=auth,
                                              follow_redirects=True, timeout=EXTERNAL_CALLS_CONNECT_TIMEOUT_IN_SECONDS)
        logging.info(f"status: {response.status_code} response: {response.text}")

        if response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
            raise TooManyRequestException(message=response.text)
        try:
            response.raise_for_status()
        except HTTPStatusError as e:
            if e and hasattr(e, "response"):
                if hasattr(e.response, "status_code") and hasattr(e.response, "text"):
                    raise HTTPException(status_code=e.response.status_code, detail=e.response.json())
        return convert_response_to_dict(response=response)


async def invoke_post_url(url: str, body: Union[str, dict], headers: dict, query: Optional[dict] = None,
                          auth=None) -> dict:
    logging.info(f"url: POST {url} body: {body} headers: {headers} query: {query}")
    async with AsyncClient() as client:
        response: Response = await client.post(url=url, data=body, params=query, headers=headers, auth=auth,
                                               follow_redirects=True, timeout=EXTERNAL_CALLS_CONNECT_TIMEOUT_IN_SECONDS)
        logging.info(f"status: {response.status_code} response: {response.text}")

        if response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
            raise TooManyRequestException(message=response.text)

        try:
            response.raise_for_status()
        except HTTPStatusError as e:
            if e and hasattr(e, "response"):
                if hasattr(e.response, "status_code") and hasattr(e.response, "text"):
                    raise HTTPException(status_code=e.response.status_code, detail=e.response.json())
        return convert_response_to_dict(response=response)


async def invoke_delete_url(url: str, headers: Optional[dict] = None, query: Optional[dict] = None, auth=None) -> dict:
    logging.info(f"url: DELETE {url} headers: {headers} query: {query}")
    async with AsyncClient() as client:
        response: Response = await client.delete(url=url, params=query, headers=headers, auth=auth,
                                                 follow_redirects=True,
                                                 timeout=EXTERNAL_CALLS_CONNECT_TIMEOUT_IN_SECONDS)
        logging.info(f"status: {response.status_code} response: {response.text}")

        if response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
            raise TooManyRequestException(message=response.text)

        try:
            response.raise_for_status()
        except HTTPStatusError as e:
            if e and hasattr(e, "response"):
                if hasattr(e.response, "status_code") and hasattr(e.response, "text"):
                    raise HTTPException(status_code=e.response.status_code, detail=e.response.json())
        return convert_response_to_dict(response=response)


def convert_str_to_dict(response: str) -> dict:
    ret = {}
    for key_vals in [vals.split('=') for vals in response.split('&')]:
        ret[key_vals[0]] = key_vals[1]
    return ret


def convert_response_to_dict(response: Response) -> dict:
    content_type = response.headers.get(Content_Type, APPLICATION_JSON)
    if content_type.startswith(APPLICATION_JSON):
        ret = response.json()
    else:
        ret = convert_str_to_dict(response=response.text)
    return ret
