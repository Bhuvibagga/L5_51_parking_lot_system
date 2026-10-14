# Lab 5: Static Code Analysis — Reflection

## 1. Which issues were the easiest to fix, and which were the hardest? Why?

The easiest issues were style-related problems, such as long lines, missing final newlines, unused imports, and naming conventions. These were straightforward to identify and correct.

The hardest issues were security-related problems, especially replacing `eval()` with a numeric calculation and removing shell command execution. These changes required modifying the implementation while preserving the intended behavior of the parking lot system. Refactoring the global collection variable into a class also required checking that the collection total was still updated correctly.

## 2. Did the static analysis tools report any false positives? If so, describe one example.

A static analysis warning does not always indicate an actual bug. Some warnings may be false positives or may identify code that is valid but could be improved.

In this experiment, I did not establish a confirmed false positive from the reports. For example, a warning about an apparently unused variable could be investigated to determine whether it is genuinely unnecessary. I would classify it as a false positive only if the code's intended behavior justified retaining it.

## 3. How would you integrate static analysis tools into your actual software development workflow?

I would run Pylint, Bandit, and Flake8 regularly while developing Python applications. I would configure consistent rules for the project and execute the tools before committing code.

I would also integrate them into a GitHub Actions continuous integration pipeline so that every pull request is checked automatically. Security findings and important code-quality issues would be reviewed before changes are merged. This would help identify problems early and maintain consistent coding standards across the team.

## 4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

The corrected program achieved a Pylint score of 10.00/10, compared with the original score of 4.10/10. Bandit reported no issues, and Flake8 produced no reported violations.

The changes improved readability through consistent naming and clearer function structure. Replacing `eval()` and shell execution reduced potential security risks. Using a non-mutable default argument prevented accidental sharing of a list, while context-managed file handling improved resource management. Moving collection tracking into a `ParkingLot` class also reduced reliance on global state.

These improvements made the program easier to maintain and reduced several potential sources of bugs and security vulnerabilities.
