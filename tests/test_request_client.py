"""Tests for the request client methods."""

from __future__ import annotations

import asyncio
from typing import Any

from aiohttp import ClientError
from aioresponses import CallbackResult, aioresponses
import pytest

from luchtmeetnetapi.api import LuchtmeetNetApi
from luchtmeetnetapi.exceptions import LuchtmeetNetConnectionError
from tests.const import MOCK_URL


async def test_unexpected_server_response(
    responses: aioresponses,
) -> None:
    """Test handling unexpected response."""
    responses.get(
        f"{MOCK_URL}/stations?page=1",
        status=404,
        headers={"Content-Type": "plain/text"},
        body="Yes",
    )
    with pytest.raises(LuchtmeetNetConnectionError):
        async with LuchtmeetNetApi() as client:
            await client.get_stations()


async def test_unauthorized(
    responses: aioresponses,
) -> None:
    """Test handling unauthorized response."""
    responses.get(
        f"{MOCK_URL}/stations?page=1",
        status=403,
        body='{"error": "forbidden"}',
    )
    with pytest.raises(LuchtmeetNetConnectionError):
        async with LuchtmeetNetApi() as client:
            await client.get_stations()


async def test_timeout(
    responses: aioresponses,
) -> None:
    """Test request timeout."""

    # Faking a timeout by sleeping
    async def response_handler(_: str, **_kwargs: Any) -> CallbackResult:
        """Response handler for this test."""
        await asyncio.sleep(2)
        return CallbackResult(body="Delayed")

    responses.get(
        f"{MOCK_URL}/stations?page=1",
        callback=response_handler,
    )
    async with LuchtmeetNetApi() as client:
        client.request_timeout = 1
        with pytest.raises(LuchtmeetNetConnectionError):
            await client.get_stations()


async def test_client_error(
    responses: aioresponses,
) -> None:
    """Test client error."""

    async def response_handler(_: str, **_kwargs: Any) -> CallbackResult:
        """Response handler for this test."""
        raise ClientError

    responses.get(
        f"{MOCK_URL}/stations?page=1",
        callback=response_handler,
    )
    with pytest.raises(LuchtmeetNetConnectionError):
        async with LuchtmeetNetApi() as client:
            await client.get_stations()
