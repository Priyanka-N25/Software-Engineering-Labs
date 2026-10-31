import pytest
from amusement_park_ride_access import (
    process_ride_admissions,
    inspect_safety_restraints,
)


def test_invalid_inputs():
    with pytest.raises(ValueError):
        process_ride_admissions("not a list", 5.0)

    with pytest.raises(ValueError):
        process_ride_admissions([], -5.0)


def test_closed_and_unknown_rides():
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
    ]

    result = process_ride_admissions(groups, 5.0)
    assert result["status"] == "ZERO_ADMISSIONS"


def test_all_valid_ride_types():
    groups = [
        {
            "is_open": True,
            "ride_type": "roller_coaster",
            "patrons": [
                {"height_cm": 150, "health_warning": False, "is_child": False}
            ],
        },
        {
            "is_open": True,
            "ride_type": "water_ride",
            "patrons": [
                {"height_cm": 150, "health_warning": False, "is_child": False}
            ],
        },
        {
            "is_open": True,
            "ride_type": "family",
            "patrons": [
                {"height_cm": 150, "health_warning": False, "is_child": True}
            ],
        },
    ]

    result = process_ride_admissions(groups, 5.0)
    assert result["status"] == "COMPLETED"


def test_patron_rejection_paths():
    groups = [
        {
            "is_open": True,
            "ride_type": "family",
            "patrons": [
                {"height_cm": 0},
                {"height_cm": 100},
                {"height_cm": 130, "health_warning": True},
            ],
        }
    ]

    result = process_ride_admissions(groups, 5.0)
    assert result["status"] == "ZERO_ADMISSIONS"


def test_child_and_adult_paths():
    groups = [
        {
            "is_open": True,
            "ride_type": "family",
            "has_fast_lane": True,
            "patrons": [
                {"height_cm": 130, "health_warning": False, "is_child": True},
                {"height_cm": 150, "health_warning": False, "is_child": False},
            ],
        }
    ]

    result = process_ride_admissions(groups, 5.0)

    assert result["total_revenue"] == 21.0
    assert result["status"] == "COMPLETED"


def test_roller_coaster_health_warning():
    groups = [
        {
            "is_open": True,
            "ride_type": "roller_coaster",
            "patrons": [
                {"height_cm": 150, "health_warning": True},
            ],
        }
    ]

    result = process_ride_admissions(groups, 5.0)
    assert result["total_revenue"] == 0.0


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


def test_safety_restraints_all_paths():
    assert inspect_safety_restraints([]) == "NO_DATA"
    assert inspect_safety_restraints([[1, 0, 1]]) == "SAFE"
    assert inspect_safety_restraints([[0, 0]]) == "EMERGENCY_LOCK"