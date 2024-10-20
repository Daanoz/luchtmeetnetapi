"""Tests for the client methods."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from aiohttp.hdrs import METH_GET
from aioresponses import aioresponses

from luchtmeetnetapi import LuchtmeetNetClient
from tests import load_fixture
from tests.const import MOCK_URL

if TYPE_CHECKING:
    from syrupy import SnapshotAssertion


# Some test vars
FIRST_PAGE = 1
LAST_PAGE = 3
STATION_ID = "TESTA"
CACHED_STATION_ID = "NL01491"


async def test_get_closest_station(
    responses: aioresponses,
) -> None:
    """Test retrieving coordinate from cache."""
    responses.get(
        f"{MOCK_URL}/stations?page=1",
        status=200,
        body=load_fixture("get_stations.json"),
    )
    async with LuchtmeetNetClient() as client:
        station = await client.get_closest_station(longitude=4.4307, latitude=51.93858)
        assert station == CACHED_STATION_ID


async def test_get_station_coordinate_from_cache() -> None:
    """Test retrieving coordinate from cache."""
    async with LuchtmeetNetClient() as client:
        coord = await client.get_station_coordinate(CACHED_STATION_ID, use_cache=True)
        assert coord == (4.4307, 51.93858)


async def test_get_station_coordinate_without_cache(
    responses: aioresponses,
) -> None:
    """Test retrieving coordinate from cache."""
    responses.get(
        f"{MOCK_URL}/stations/{CACHED_STATION_ID}",
        status=200,
        body=load_fixture("get_station.json"),
    )
    async with LuchtmeetNetClient() as client:
        coord = await client.get_station_coordinate(CACHED_STATION_ID, use_cache=False)
        assert coord == (5.6462, 52.1009)
        responses.assert_called_once_with(
            f"{MOCK_URL}/stations/{CACHED_STATION_ID}", METH_GET, params=None
        )


async def test_get_all_components(
    responses: aioresponses,
    snapshot: SnapshotAssertion,
) -> None:
    """Test retrieving all components."""
    fixture = load_fixture("get_components.json")
    for page in range(FIRST_PAGE, LAST_PAGE + 1):
        fixture = _set_pagination(page, fixture)
        responses.add(f"{MOCK_URL}/components?page={page}", status=200, body=fixture)
    async with LuchtmeetNetClient() as client:
        assert await client.get_all_components() == snapshot
        for page in range(FIRST_PAGE, LAST_PAGE + 1):
            responses.assert_called_with(
                f"{MOCK_URL}/components", METH_GET, params={"page": str(page)}
            )


async def test_get_all_organisations(
    responses: aioresponses,
    snapshot: SnapshotAssertion,
) -> None:
    """Test retrieving all organisations."""
    fixture = load_fixture("get_organisations.json")
    for page in range(FIRST_PAGE, LAST_PAGE + 1):
        fixture = _set_pagination(page, fixture)
        responses.add(f"{MOCK_URL}/organisations?page={page}", status=200, body=fixture)
    async with LuchtmeetNetClient() as client:
        assert await client.get_all_organisations() == snapshot
        for page in range(FIRST_PAGE, LAST_PAGE + 1):
            responses.assert_called_with(
                f"{MOCK_URL}/organisations", METH_GET, params={"page": str(page)}
            )


async def test_get_all_stations(
    responses: aioresponses,
    snapshot: SnapshotAssertion,
) -> None:
    """Test retrieving all stations."""
    fixture = load_fixture("get_stations.json")
    for page in range(FIRST_PAGE, LAST_PAGE + 1):
        fixture = _set_pagination(page, fixture)
        responses.add(f"{MOCK_URL}/stations?page={page}", status=200, body=fixture)
    async with LuchtmeetNetClient() as client:
        assert await client.get_all_stations() == snapshot
        for page in range(FIRST_PAGE, LAST_PAGE + 1):
            responses.assert_called_with(
                f"{MOCK_URL}/stations", METH_GET, params={"page": str(page)}
            )


async def test_get_all_station_measurements(
    responses: aioresponses,
    snapshot: SnapshotAssertion,
) -> None:
    """Test retrieving all station measurements."""
    fixture = load_fixture("get_station_measurements.json")
    for page in range(FIRST_PAGE, LAST_PAGE + 1):
        fixture = _set_pagination(page, fixture)
        responses.add(
            f"{MOCK_URL}/stations/{STATION_ID}/measurements?page={page}",
            status=200,
            body=fixture,
        )
    async with LuchtmeetNetClient() as client:
        assert (
            await client.get_all_station_measurements(station_number=STATION_ID)
            == snapshot
        )
        for page in range(FIRST_PAGE, LAST_PAGE + 1):
            responses.assert_called_with(
                f"{MOCK_URL}/stations/{STATION_ID}/measurements",
                METH_GET,
                params={"page": str(page)},
            )


async def test_get_all_measurements(
    responses: aioresponses,
    snapshot: SnapshotAssertion,
) -> None:
    """Test retrieving all measurements."""
    fixture = load_fixture("get_measurements.json")
    for page in range(FIRST_PAGE, LAST_PAGE + 1):
        fixture = _set_pagination(page, fixture)
        responses.add(
            f"{MOCK_URL}/measurements?page={page}",
            status=200,
            body=fixture,
        )
    async with LuchtmeetNetClient() as client:
        assert await client.get_all_measurements() == snapshot
        for page in range(FIRST_PAGE, LAST_PAGE + 1):
            responses.assert_called_with(
                f"{MOCK_URL}/measurements",
                METH_GET,
                params={"page": str(page)},
            )


async def test_get_all_lki(
    responses: aioresponses,
    snapshot: SnapshotAssertion,
) -> None:
    """Test retrieving all lki."""
    fixture = load_fixture("get_lki.json")
    for page in range(FIRST_PAGE, LAST_PAGE + 1):
        fixture = _set_pagination(page, fixture)
        responses.add(
            f"{MOCK_URL}/lki?page={page}",
            status=200,
            body=fixture,
        )
    async with LuchtmeetNetClient() as client:
        assert await client.get_all_lki() == snapshot
        for page in range(FIRST_PAGE, LAST_PAGE + 1):
            responses.assert_called_with(
                f"{MOCK_URL}/lki",
                METH_GET,
                params={"page": str(page)},
            )


def _set_pagination(current_page: int, fixture: str) -> str:
    pagination_fixture = load_fixture("pagination.json")
    prev_page = current_page - 1 if current_page > FIRST_PAGE else FIRST_PAGE
    next_page = current_page + 1 if current_page < LAST_PAGE else LAST_PAGE
    page_list = ",".join(map(str, range(FIRST_PAGE, LAST_PAGE + 1)))
    pagination = (
        pagination_fixture.replace('"CURRENT_PAGE"', str(current_page))
        .replace('"LAST_PAGE"', str(LAST_PAGE))
        .replace('"FIRST_PAGE"', str(FIRST_PAGE))
        .replace('"PREV_PAGE"', str(prev_page))
        .replace('"NEXT_PAGE"', str(next_page))
        .replace('"PAGE_LIST"', page_list)
    )
    return re.sub(
        r'("pagination": ){.*?}', r"\1" + pagination, fixture, flags=re.DOTALL
    )
