# Lab 05 — Static Code Analysis: Issues and Fixes

## Project
**Scholarship Screener**

Repository: https://github.com/SETAPESU26/L5_11_scholarship_screener

## 1. Issues Identified and Fixed

| No. | Issue | Tool(s) | Fix Applied |
|---|---|---|---|
| 1 | Unsafe use of `eval()` to calculate merit scores | Pylint, Bandit | Replaced `eval()` with a restricted AST-based arithmetic evaluator that permits only approved numeric operations and variables. |
| 2 | Mutable default argument `logs=[]` | Pylint | Changed the default to `None` and initialized a new list inside the function. |
| 3 | Bare `except` and ignored exceptions | Flake8, Bandit | Replaced broad exception handling with specific exception types and preserved existing results when loading fails. |
| 4 | Unused imports | Pylint, Flake8 | Removed imports that were not needed. The revised implementation uses `math` for numeric validation. |
| 5 | File operations without context managers or explicit encoding | Pylint | Used `with open(...)` and UTF-8 encoding for reading and writing JSON files. |
| 6 | Comparison with `True` | Flake8 | Replaced explicit Boolean comparison with a direct condition. |
| 7 | Incorrect function naming convention | Pylint | Renamed `printShortlist()` to `print_shortlist()` to follow Python naming conventions. |
| 8 | Missing input validation | Manual review and code improvement | Added checks for GPA, credits, income, and finite numeric values. Invalid applicants are recorded as ineligible. |
| 9 | Formula input could execute arbitrary code | Bandit and security review | Restricted formula evaluation to approved arithmetic expressions instead of executing arbitrary Python code. |
| 10 | Missing documentation and inconsistent formatting | Pylint, Flake8 | Added module and function docstrings and corrected formatting issues. |

## Final Static Analysis Results

| Tool | Final Result |
|---|---|
| Pylint | **10.00/10** — no warnings reported |
| Flake8 | **No style or formatting errors reported** |
| Bandit | **No security issues identified** |

### Summary

The initial analysis identified several code-quality and security concerns, including unsafe use of `eval()`, a mutable default argument, a bare exception handler, unused imports, inconsistent naming, and file handling without context managers.

The code was improved by replacing `eval()` with a restricted arithmetic expression evaluator, validating applicant data, removing the mutable default argument, handling exceptions more specifically, using context managers for file operations, and following Python naming and documentation conventions.

After these improvements, all three static analysis tools completed successfully. The final Pylint score was **10.00/10**, Flake8 reported no errors, and Bandit identified no security issues.