import math


def validate_height_and_fastpass(rider_spec):
    if not isinstance(rider_spec, str):
        raise ValueError("Rider specification must be text.")

    try:
        parts = rider_spec.strip().split(':')

        if len(parts) != 2:
            raise ValueError("Use Height:FastPass format.")

        height_str, pass_str = parts
        height = int(height_str.strip())

        if height < 0:
            raise ValueError("Height cannot be negative.")

        pass_map = {"YES": True, "NO": False}
        pass_value = pass_str.strip().upper()

        if pass_value not in pass_map:
            raise ValueError("FastPass must be YES or NO.")

        has_fastpass = pass_map[pass_value]
        eligible = height >= 120

        status = "FastPass Priority" if has_fastpass else "Standard Entry"

        return f"Height {height}cm: {'Approved' if eligible else 'Denied'} ({status})"

    except (ValueError, TypeError) as e:
        raise ValueError("Invalid rider specification.") from e


def compute_dispatch_throughput(ride_metric_str):
    if not isinstance(ride_metric_str, str):
        raise ValueError("Input must be text.")

    try:
        parts = ride_metric_str.strip().split('/')

        if len(parts) != 2:
            raise ValueError("Use riders/minutes format.")

        riders_str, mins_str = parts

        riders = float(riders_str)
        cycle_mins = float(mins_str)

        if not math.isfinite(riders) or not math.isfinite(cycle_mins):
            raise ValueError("Values must be finite numbers.")

        if riders < 0 or cycle_mins <= 0:
            raise ValueError("Invalid riders or minutes.")

        rate = riders / cycle_mins

        return round(rate, 2)

    except (ValueError, TypeError, ZeroDivisionError) as e:
        raise ValueError("Invalid ride metric.") from e


def resolve_safety_restraint_code(zone_code):
    if not isinstance(zone_code, str):
        raise ValueError("Zone code must be text.")

    prefix = zone_code.strip().upper()[:3]

    restraint_types = {
        "CST": "Over-the-Shoulder Harness",
        "WTR": "Lap Bar and Seatbelt",
        "DRP": "Hydraulic Shoulder Vest",
        "WHL": "Manual Safety Bar"
    }

    if prefix not in restraint_types:
        raise ValueError("Unknown or invalid zone code.")

    return restraint_types[prefix]


def main():
    print("==== Running validate_height_and_fastpass ====")
    r_input = input("Enter rider spec (Height:FastPass, e.g. 140:YES): ")
    print(validate_height_and_fastpass(r_input))

    print("\n==== Running compute_dispatch_throughput ====")
    t_input = input("Enter riders/mins (e.g. 48/2.5): ")
    print("Throughput (riders/min):", compute_dispatch_throughput(t_input))

    print("\n==== Running resolve_safety_restraint_code ====")
    z_input = input("Enter ride zone code (e.g. CST_01, WTR_A): ")
    print("Restraint:", resolve_safety_restraint_code(z_input))


if __name__ == "__main__":
    main()