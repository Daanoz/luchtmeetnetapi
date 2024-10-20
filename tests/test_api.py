"""Tests for the api methods."""

from __future__ import annotations

from typing import TYPE_CHECKING

from aiohttp.hdrs import METH_GET
from aioresponses import aioresponses

from luchtmeetnetapi.api import LuchtmeetNetApi
from tests import load_fixture
from tests.const import MOCK_URL

if TYPE_CHECKING:
    from syrupy import SnapshotAssertion


# Some test vars
STATION_ID = "TESTA"
ORGANISATION_ID = "ORG-A"
FORMULA = "H2O"
START = "2019-09-03T09:00:00"
END = "2019-09-04T09:00:00"
LONGITUDE = 5.6462
LATITUDE = 52.1009


async def test_get_component(
    responses: aioresponses,
    snapshot: SnapshotAssertion,
) -> None:
    """Test retrieving component."""
    responses.get(
        f"{MOCK_URL}/components/{FORMULA}",
        status=200,
        body=load_fixture("get_component.json"),
    )
    async with LuchtmeetNetApi() as client:
        assert await client.get_component(FORMULA) == snapshot
        responses.assert_called_once_with(
            f"{MOCK_URL}/components/{FORMULA}", METH_GET, params=None
        )


async def test_get_components(
    responses: aioresponses,
    snapshot: SnapshotAssertion,
) -> None:
    """Test retrieving components."""
    responses.get(
        f"{MOCK_URL}/components?page=1",
        status=200,
        body=load_fixture("get_components.json"),
    )
    async with LuchtmeetNetApi() as client:
        assert await client.get_components() == snapshot
        responses.assert_called_once_with(
            f"{MOCK_URL}/components", METH_GET, params={"page": "1"}
        )


async def test_get_components_all_params(
    responses: aioresponses,
    snapshot: SnapshotAssertion,
) -> None:
    """Test retrieving components."""
    responses.get(
        f"{MOCK_URL}/components?page=5&order_by=formula",
        status=200,
        body=load_fixture("get_components.json"),
    )
    async with LuchtmeetNetApi() as client:
        assert (
            await client.get_components(
                page=5,
                order_by="formula",
            )
            == snapshot
        )
        responses.assert_called_once_with(
            f"{MOCK_URL}/components",
            METH_GET,
            params={"page": str(5), "order_by": "formula"},
        )


async def test_get_organisations(
    responses: aioresponses,
    snapshot: SnapshotAssertion,
) -> None:
    """Test retrieving organisations."""
    responses.get(
        f"{MOCK_URL}/organisations?page=1",
        status=200,
        body=load_fixture("get_organisations.json"),
    )
    async with LuchtmeetNetApi() as client:
        assert await client.get_organisations() == snapshot
        responses.assert_called_once_with(
            f"{MOCK_URL}/organisations", METH_GET, params={"page": "1"}
        )


async def test_get_organisations_all_params(
    responses: aioresponses,
    snapshot: SnapshotAssertion,
) -> None:
    """Test retrieving organisations."""
    responses.get(
        f"{MOCK_URL}/organisations?page=5",
        status=200,
        body=load_fixture("get_organisations.json"),
    )
    async with LuchtmeetNetApi() as client:
        assert await client.get_organisations(page=5) == snapshot
        responses.assert_called_once_with(
            f"{MOCK_URL}/organisations", METH_GET, params={"page": "5"}
        )


async def test_get_stations(
    responses: aioresponses,
    snapshot: SnapshotAssertion,
) -> None:
    """Test retrieving stations."""
    responses.get(
        f"{MOCK_URL}/stations?page=1",
        status=200,
        body=load_fixture("get_stations.json"),
    )
    async with LuchtmeetNetApi() as client:
        assert await client.get_stations() == snapshot
        responses.assert_called_once_with(
            f"{MOCK_URL}/stations", METH_GET, params={"page": "1"}
        )


async def test_get_stations_all_params(
    responses: aioresponses,
    snapshot: SnapshotAssertion,
) -> None:
    """Test retrieving stations."""
    responses.get(
        f"{MOCK_URL}/stations?page=5&order_by=number&organisation_id={ORGANISATION_ID}",
        status=200,
        body=load_fixture("get_stations.json"),
    )
    async with LuchtmeetNetApi() as client:
        assert (
            await client.get_stations(
                page=5,
                organisation_id=ORGANISATION_ID,
                order_by="number",
            )
            == snapshot
        )
        responses.assert_called_once_with(
            f"{MOCK_URL}/stations",
            METH_GET,
            params={
                "page": "5",
                "order_by": "number",
                "organisation_id": ORGANISATION_ID,
            },
        )


async def test_get_station(
    responses: aioresponses,
    snapshot: SnapshotAssertion,
) -> None:
    """Test retrieving station."""
    responses.get(
        f"{MOCK_URL}/stations/{STATION_ID}",
        status=200,
        body=load_fixture("get_station.json"),
    )
    async with LuchtmeetNetApi() as client:
        assert await client.get_station(STATION_ID) == snapshot
        responses.assert_called_once_with(
            f"{MOCK_URL}/stations/{STATION_ID}", METH_GET, params=None
        )


async def test_get_station_measurements(
    responses: aioresponses,
    snapshot: SnapshotAssertion,
) -> None:
    """Test retrieving station measurements."""
    responses.get(
        f"{MOCK_URL}/stations/{STATION_ID}/measurements?page=1",
        status=200,
        body=load_fixture("get_station_measurements.json"),
    )
    async with LuchtmeetNetApi() as client:
        assert await client.get_station_measurements(STATION_ID) == snapshot
        responses.assert_called_once_with(
            f"{MOCK_URL}/stations/{STATION_ID}/measurements",
            METH_GET,
            params={"page": "1"},
        )


async def test_get_station_measurements_all_params(
    responses: aioresponses,
    snapshot: SnapshotAssertion,
) -> None:
    """Test retrieving station measurements."""
    responses.get(
        f"{MOCK_URL}/stations/{STATION_ID}/measurements?page=5&order=formula&order_direction=desc&formula={FORMULA}",
        status=200,
        body=load_fixture("get_station_measurements.json"),
    )
    async with LuchtmeetNetApi() as client:
        assert (
            await client.get_station_measurements(
                STATION_ID,
                page=5,
                order="formula",
                order_direction="desc",
                formula=FORMULA,
            )
            == snapshot
        )
        responses.assert_called_once_with(
            f"{MOCK_URL}/stations/{STATION_ID}/measurements",
            METH_GET,
            params={
                "page": "5",
                "order": "formula",
                "order_direction": "desc",
                "formula": FORMULA,
            },
        )


async def test_get_measurements(
    responses: aioresponses,
    snapshot: SnapshotAssertion,
) -> None:
    """Test retrieving measurements."""
    responses.get(
        f"{MOCK_URL}/measurements?page=1",
        status=200,
        body=load_fixture("get_measurements.json"),
    )
    async with LuchtmeetNetApi() as client:
        assert await client.get_measurements() == snapshot
        responses.assert_called_once_with(
            f"{MOCK_URL}/measurements", METH_GET, params={"page": "1"}
        )


async def test_get_measurements_all_params(
    responses: aioresponses,
    snapshot: SnapshotAssertion,
) -> None:
    """Test retrieving measurements."""
    responses.get(
        f"{MOCK_URL}/measurements?page=5&order_by=formula&order_direction=desc&formula={FORMULA}&station_number={STATION_ID}&start={START}&end={END}",
        status=200,
        body=load_fixture("get_measurements.json"),
    )
    async with LuchtmeetNetApi() as client:
        assert (
            await client.get_measurements(
                page=5,
                start=START,
                end=END,
                order_by="formula",
                order_direction="desc",
                formula=FORMULA,
                station_number=STATION_ID,
            )
            == snapshot
        )
        responses.assert_called_once_with(
            f"{MOCK_URL}/measurements",
            METH_GET,
            params={
                "page": "5",
                "start": START,
                "end": END,
                "order_by": "formula",
                "order_direction": "desc",
                "formula": FORMULA,
                "station_number": STATION_ID,
            },
        )


async def test_get_lki(
    responses: aioresponses,
    snapshot: SnapshotAssertion,
) -> None:
    """Test retrieving lki."""
    responses.get(
        f"{MOCK_URL}/lki?page=1",
        status=200,
        body=load_fixture("get_lki.json"),
    )
    async with LuchtmeetNetApi() as client:
        assert await client.get_lki() == snapshot
        responses.assert_called_once_with(
            f"{MOCK_URL}/lki", METH_GET, params={"page": "1"}
        )


async def test_get_lki_all_params(
    responses: aioresponses,
    snapshot: SnapshotAssertion,
) -> None:
    """Test retrieving lki."""
    responses.get(
        f"{MOCK_URL}/lki?page=5&start={START}&end={END}&order_by=formula&order_direction=desc&station_number={STATION_ID}",
        status=200,
        body=load_fixture("get_lki.json"),
    )
    async with LuchtmeetNetApi() as client:
        assert (
            await client.get_lki(
                page=5,
                start=START,
                end=END,
                order_by="formula",
                order_direction="desc",
                station_number=STATION_ID,
            )
            == snapshot
        )
        responses.assert_called_once_with(
            f"{MOCK_URL}/lki",
            METH_GET,
            params={
                "page": "5",
                "start": START,
                "end": END,
                "order_by": "formula",
                "order_direction": "desc",
                "station_number": STATION_ID,
            },
        )


async def test_get_concentrations(
    responses: aioresponses,
    snapshot: SnapshotAssertion,
) -> None:
    """Test retrieving concentrations."""
    responses.get(
        f"{MOCK_URL}/concentrations?formula={FORMULA}&longitude={LONGITUDE}&latitude={LATITUDE}",
        status=200,
        body=load_fixture("get_concentrations.json"),
    )
    async with LuchtmeetNetApi() as client:
        assert (
            await client.get_concentrations(
                formula=FORMULA, longitude=LONGITUDE, latitude=LATITUDE
            )
            == snapshot
        )
        responses.assert_called_once_with(
            f"{MOCK_URL}/concentrations",
            METH_GET,
            params={
                "formula": FORMULA,
                "longitude": str(LONGITUDE),
                "latitude": str(LATITUDE),
            },
        )


async def test_get_concentrations_all_params(
    responses: aioresponses,
    snapshot: SnapshotAssertion,
) -> None:
    """Test retrieving concentrations."""
    responses.get(
        f"{MOCK_URL}/concentrations?formula={FORMULA}&longitude={LONGITUDE}&latitude={LATITUDE}&start={START}&end={END}&station_number={STATION_ID}",
        status=200,
        body=load_fixture("get_concentrations.json"),
    )
    async with LuchtmeetNetApi() as client:
        assert (
            await client.get_concentrations(
                formula=FORMULA,
                longitude=LONGITUDE,
                latitude=LATITUDE,
                start=START,
                end=END,
                station_number=STATION_ID,
            )
            == snapshot
        )
        responses.assert_called_once_with(
            f"{MOCK_URL}/concentrations",
            METH_GET,
            params={
                "formula": FORMULA,
                "longitude": str(LONGITUDE),
                "latitude": str(LATITUDE),
                "start": START,
                "end": END,
                "station_number": STATION_ID,
            },
        )
