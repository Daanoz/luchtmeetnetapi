"""Tests for the util methods."""

import pytest

from luchtmeetnetapi.util import get_approximate_distance


def test_approximate_distance_calculation() -> None:
    """Test approximate distance haversine calculation."""
    assert get_approximate_distance(
        (5.5433281, 51.69818779), (4.860319, 52.374786)
    ) == pytest.approx(88.559, 0.001)
    assert get_approximate_distance(
        (5.5433281, 51.69818779), (5.5433281, 51.69818779)
    ) == pytest.approx(0.0, 0.001)
