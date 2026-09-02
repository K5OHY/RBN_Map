"""
First test coverage for this repo. Covers the three grid-to-latlon wrapper functions
(rbn_to_csv.gridsquare_to_latlon, Update_spotters.grid_to_latlon, web.grid_square_to_latlon),
all of which now delegate to the maidenhead library rather than hand-rolled conversion math.

Run with: pytest test_grid_conversion.py
"""
import pytest

from rbn_to_csv import gridsquare_to_latlon
from Update_spotters import grid_to_latlon
from web import grid_square_to_latlon


# 6-character grid, all three functions accept this and should agree closely (rbn_to_csv and
# web.py return full-precision floats; Update_spotters rounds to 3 decimal places for CSV output).
SIX_CHAR_GRID = "DM81wx"
SIX_CHAR_EXPECTED_LAT = pytest.approx(31.979166666666668, abs=1e-6)
SIX_CHAR_EXPECTED_LON = pytest.approx(-102.125, abs=1e-6)


def test_gridsquare_to_latlon_six_char():
    lat, lon = gridsquare_to_latlon(SIX_CHAR_GRID)
    assert lat == SIX_CHAR_EXPECTED_LAT
    assert lon == SIX_CHAR_EXPECTED_LON


def test_gridsquare_to_latlon_rejects_non_six_char():
    with pytest.raises(ValueError):
        gridsquare_to_latlon("DM81")


def test_grid_to_latlon_six_char():
    lat, lon = grid_to_latlon(SIX_CHAR_GRID)
    assert lat == pytest.approx(31.979, abs=1e-3)
    assert lon == pytest.approx(-102.125, abs=1e-3)


def test_grid_to_latlon_four_char_returns_centre():
    # 4-character grid: centre of the 2deg x 1deg square, not a corner.
    lat, lon = grid_to_latlon("DM81")
    assert lat == pytest.approx(31.5, abs=1e-3)
    assert lon == pytest.approx(-103.0, abs=1e-3)


def test_grid_to_latlon_rejects_too_short():
    with pytest.raises(ValueError):
        grid_to_latlon("DM8")


def test_grid_square_to_latlon_six_char():
    lat, lon = grid_square_to_latlon(SIX_CHAR_GRID)
    assert lat == SIX_CHAR_EXPECTED_LAT
    assert lon == SIX_CHAR_EXPECTED_LON


def test_grid_square_to_latlon_four_char_returns_centre():
    # Consolidation fix: the old hand-rolled version returned the south-west corner for a
    # 4-character grid; the maidenhead-backed version returns the centre, consistent with the
    # other two functions and with a 6-character grid's own behaviour.
    lat, lon = grid_square_to_latlon("DM81")
    assert lat == pytest.approx(31.5, abs=1e-3)
    assert lon == pytest.approx(-103.0, abs=1e-3)


def test_all_three_agree_on_the_same_six_char_grid():
    a = gridsquare_to_latlon(SIX_CHAR_GRID)
    b = grid_to_latlon(SIX_CHAR_GRID)
    c = grid_square_to_latlon(SIX_CHAR_GRID)
    assert a[0] == pytest.approx(b[0], abs=1e-3) == pytest.approx(c[0], abs=1e-3)
    assert a[1] == pytest.approx(b[1], abs=1e-3) == pytest.approx(c[1], abs=1e-3)
