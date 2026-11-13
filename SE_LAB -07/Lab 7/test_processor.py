from hypothesis import given, strategies as st
from processor import (
    validate_height_and_fastpass,
    compute_dispatch_throughput,
    resolve_safety_restraint_code
)


@given(st.one_of(st.text(), st.none()))
def test_validate_height_and_fastpass_no_crash(s):
    try:
        validate_height_and_fastpass(s)
    except ValueError:
        pass


@given(st.one_of(st.text(), st.none()))
def test_compute_dispatch_throughput_safe(s):
    try:
        compute_dispatch_throughput(s)
    except ValueError:
        pass


@given(st.one_of(st.text(), st.none()))
def test_resolve_safety_restraint_code_safe(s):
    try:
        resolve_safety_restraint_code(s)
    except ValueError:
        pass