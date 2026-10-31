import pytest
from amusement_park_ride_access import (
    process_ride_admissions,
    inspect_safety_restraints,
)


def test_all_ride_types_and_admissions():
    groups = [
        {
            "is_open": True,
            "ride_type": "roller_coaster",
            "has_fast_lane": False,
            "patrons": [
                {"height_cm": 180, "health_warning": False, "is_child": False}
            ],
        },
        {
            "is_open": True,
            "ride_type": "water_ride",
            "has_fast_lane": False,
            "patrons": [
                {"height_cm": 130, "health_warning": False, "is_child": True}
            ],
        },
        {
            "is_open": True,
            "ride_type": "family",
            "has_fast_lane": True,
            "patrons": [
                {"height_cm": 150, "health_warning": False, "is_child": False}
            ],
        },
    ]

    result = process_ride_admissions(groups, 5.0)

    assert result["total_revenue"] == 50.8
    assert result["status"] == "COMPLETED"


def test_rejections_and_closed_ride():
    groups = [
        {
            "is_open": False,
            "ride_type": "family",
            "patrons": [],
        },
        {
            "is_open": True,
            "ride_type": "unknown",
            "patrons": [],
        },
        {
            "is_open": True,
            "ride_type": "family",
            "patrons": [
                {"height_cm": 0},
                {"height_cm": 100},
                {"height_cm": 130, "health_warning": True},
            ],
        },
    ]

    result = process_ride_admissions(groups, 5.0)

    assert result["status"] == "ZERO_ADMISSIONS"


def test_safety_audit():
    groups = [
        {
            "is_open": True,
            "ride_type": "family",
            "patrons": [
                {"height_cm": 0},
                {"height_cm": 0},
                {"height_cm": 0},
                {"height_cm": 0},
                {"height_cm": 0},
            ],
        }
    ]

    result = process_ride_admissions(groups, 5.0)

    assert result["status"] == "SAFETY_AUDIT"


def test_invalid_input():
    with pytest.raises(ValueError):
        process_ride_admissions("invalid", 5.0)

    with pytest.raises(ValueError):
        process_ride_admissions([], -1.0)


def test_roller_coaster_health_warning():
    groups = [
        {
            "is_open": True,
            "ride_type": "roller_coaster",
            "patrons": [
                {"height_cm": 180, "health_warning": False, "is_child": False},
                {"height_cm": 180, "health_warning": True},
            ],
        }
    ]

    result = process_ride_admissions(groups, 5.0)

    assert result["total_revenue"] == 0.0


def test_safety_restraints():
    assert inspect_safety_restraints([]) == "NO_DATA"
    assert inspect_safety_restraints([[1, 1, 0, 1]]) == "SAFE"
    assert inspect_safety_restraints([[1, 0, 0]]) == "EMERGENCY_LOCK"