# Reflections

### 1. How did static code analysis help improve the program?

Static code analysis helped identify potential bugs, security risks, and code-quality problems without requiring the program to be executed. Pylint highlighted maintainability and coding-standard issues, Flake8 checked style and formatting, and Bandit identified potentially unsafe code patterns. Using all three tools helped improve the program's readability, reliability, and security.

### 2. What was the most important issue found?

One of the most important issues was the use of `eval()` to calculate merit scores. Evaluating arbitrary expressions can introduce security risks. I replaced it with a restricted arithmetic expression evaluator that supports only approved operations and numeric variables. I also added input validation to reject invalid applicant data.

### 3. How did Pylint, Flake8, and Bandit differ?

Pylint examined overall code quality, including naming, documentation, and potential programming problems. Flake8 checked style and formatting issues. Bandit focused on common security risks in Python code. Using these tools together provided a more complete analysis than relying on a single tool.

### 4. What did I learn from this lab?

I learned that static analysis is useful for finding problems early and improving code before deployment. I also learned the importance of safe expression evaluation, input validation, appropriate exception handling, avoiding mutable default arguments, and using context managers for file operations. After making improvements, the final program achieved a Pylint score of 10.00/10, passed Flake8 without reported errors, and had no issues identified by Bandit.
