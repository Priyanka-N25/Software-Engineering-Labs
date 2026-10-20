"""Scholarship eligibility screening system.

Calculates merit scores, evaluates applicants, and persists results.
"""

import ast
import json
import math
import operator


# Application settings
state = {
    "results": {},
    "merit_formula": "gpa * 10 + credits * 2",
}
INCOME_LIMIT = 800000
CUTOFF = 85

# Supported arithmetic operations for merit formulas.
BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
}

UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def _evaluate_expression(node, values):
    """Evaluate a restricted arithmetic expression without using eval."""
    if isinstance(node, ast.Expression):
        return _evaluate_expression(node.body, values)

    if isinstance(node, ast.Constant):
        if type(node.value) in (int, float):
            return node.value
        raise ValueError("Only numeric constants are allowed.")

    if isinstance(node, ast.Name):
        if node.id in values:
            return values[node.id]
        raise ValueError(f"Unknown formula variable: {node.id}")

    if isinstance(node, ast.BinOp):
        operation = BINARY_OPERATORS.get(type(node.op))
        if operation is None:
            raise ValueError("Unsupported arithmetic operation.")

        left = _evaluate_expression(node.left, values)
        right = _evaluate_expression(node.right, values)
        return operation(left, right)

    if isinstance(node, ast.UnaryOp):
        operation = UNARY_OPERATORS.get(type(node.op))
        if operation is None:
            raise ValueError("Unsupported unary operation.")

        operand = _evaluate_expression(node.operand, values)
        return operation(operand)

    raise ValueError("Invalid or unsupported formula expression.")


def calculate_merit_score(gpa, credit_count):
    """Calculate a merit score using the configured formula."""
    try:
        expression = ast.parse(state["merit_formula"], mode="eval")
        score = _evaluate_expression(
            expression,
            {"gpa": gpa, "credits": credit_count},
        )
    except (
        SyntaxError,
        TypeError,
        ValueError,
        ZeroDivisionError,
        OverflowError,
    ) as exc:
        raise ValueError(
            "The merit formula could not be evaluated."
        ) from exc

    if not isinstance(score, (int, float)) or not math.isfinite(score):
        raise ValueError("The merit score must be a finite number.")

    return score


def evaluate_applicant(student_id, test_scores, logs=None):
    """Evaluate an applicant and record their eligibility and score."""
    if logs is None:
        logs = []

    try:
        gpa = test_scores["gpa"]
        credit_count = test_scores.get("credits", 0)
        income = test_scores.get("income", 0)

        for field_name, value in (
            ("gpa", gpa),
            ("credits", credit_count),
            ("income", income),
        ):
            if (
                isinstance(value, bool)
                or not isinstance(value, (int, float))
                or not math.isfinite(value)
            ):
                raise ValueError(f"{field_name} must be a finite number.")

        if not 0 <= gpa <= 10:
            raise ValueError("GPA must be between 0 and 10.")

        if credit_count < 0:
            raise ValueError("Credits cannot be negative.")

        if income < 0:
            raise ValueError("Income cannot be negative.")

        score = calculate_merit_score(gpa, credit_count)
        eligible = score >= CUTOFF and income < INCOME_LIMIT

    except (KeyError, ValueError, ZeroDivisionError, OverflowError) as exc:
        state["results"][student_id] = {
            "score": None,
            "eligible": False,
            "error": str(exc),
        }
        logs.append(f"{student_id} is invalid: {exc}")
        return False

    state["results"][student_id] = {
        "score": score,
        "eligible": eligible,
    }
    logs.append(f"{student_id} scored {score}")
    return eligible


def change_formula(new_formula):
    """Validate and update the merit formula safely."""
    previous_formula = state["merit_formula"]
    state["merit_formula"] = new_formula

    try:
        calculate_merit_score(5, 2)
    except (ValueError, ZeroDivisionError, OverflowError) as exc:
        state["merit_formula"] = previous_formula
        raise ValueError(
            "Invalid formula; the previous formula was retained."
        ) from exc


def persist_results(file="scholarships.json"):
    """Save applicant results to a JSON file."""
    with open(file, "w", encoding="utf-8") as output_file:
        json.dump(state["results"], output_file, indent=4)


def load_results(file="scholarships.json"):
    """Load applicant results when the JSON file is available."""
    try:
        with open(file, "r", encoding="utf-8") as input_file:
            loaded_results = json.load(input_file)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        # Keep the existing in-memory results if loading fails.
        return

    if isinstance(loaded_results, dict):
        state["results"] = loaded_results


def print_shortlist():
    """Print all eligible applicants and their merit scores."""
    print("Shortlisted applicants:")

    for student_id, applicant in state["results"].items():
        if applicant.get("eligible"):
            print(f"  {student_id} score = {applicant.get('score')}")


def main():
    """Run the scholarship screening demonstration."""
    sample_applicants = {
        "U001": {"gpa": 9.1, "credits": 4, "income": 450000},
        "U002": {"gpa": 7.2, "credits": 1, "income": 300000},
        "U003": {"gpa": 12.5, "credits": -3, "income": -1},
        "U004": {"gpa": 6.5},
    }

    for student_id, test_scores in sample_applicants.items():
        evaluate_applicant(student_id, test_scores)

    formula = input("Merit formula (Enter to keep default): ").strip()

    if formula:
        try:
            change_formula(formula)
        except ValueError as exc:
            print(f"Formula error: {exc}")

    evaluate_applicant(
        "U005",
        {"gpa": 8.4, "credits": 3, "income": 600000},
    )

    persist_results()
    load_results()
    print_shortlist()


if __name__ == "__main__":
    main()
