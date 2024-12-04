
## REPO.md

### Project Overview
This project integrates software quality assurance activities into the existing MLForensics Python project. It incorporates automation for testing, security analysis, fuzzing, and forensic logging based on concepts learned in the Software Quality Assurance course.

### Team Information
Team Members: Shyam Patel - sjp0059
              Jacob Simmons - jss0112@auburn.edu
              Dayton Malone - ddm0027@auburn.edu
              Jeffery Turnipseed - jzt0059@auburn.edu

### Activities

#### 4.a. Git Hook
- A Git Hook was created to automatically scan for security weaknesses in the project whenever a Python file is modified and committed.
- Output is stored in a CSV file named `hook_report.csv`.

#### 4.b. Fuzzing
- The `fuzz.py` script was implemented to test five critical Python methods.
- The script automatically runs as part of the CI pipeline.
- Bugs discovered during fuzzing are logged for review.

#### 4.c. Forensic Logging
- Forensic logging was added to five methods:
  1. `giveTimeStamp` in `main.py` logs the execution of the timestamp function.
  2. `getDataLoadCount` in `lint_engine.py` logs file analysis activities.
  3. `checkLoggingPerData` in `py_parser.py` logs checks for data-related logging.
  4. Additional methods were identified and modified for meaningful forensic logs.
  5. Logging follows Python’s `logging` module for standardization and ease of use.

#### 4.d. Continuous Integration
- A GitHub Actions pipeline was implemented to:
  - Run `pytest` to execute test cases and generate reports.
  - Execute `fuzz.py` for automated fuzzing.
  - Perform static security analysis with `Bandit`.
- Workflow is triggered on every push and pull request to the `main` branch.

### Execution Evidence
#### Git Hook Output
- The CSV report of security scans (`hook_report.csv`) contains the following columns:
  - File Name
  - Line Number
  - Issue Description
  - Severity Level

#### Fuzzing Results
- The `fuzz.py` script executed successfully, testing five methods.
- No critical crashes were observed, but logs show detailed execution traces.

#### Forensic Logs
- Forensic logs provide a trail of execution for key methods. Examples include:
  - `INFO: Executing giveTimeStamp method`
  - `INFO: Analyzing file: sample.py`
  - `INFO: Checking logging for data: user_input`

#### CI Pipeline Logs
- Test results and analysis outputs are generated in each pipeline run. Key reports include:
  - `pytest` JUnit XML report
  - `Bandit` security analysis report
  - Fuzzing execution logs

### Lessons Learned
- Integrating forensic logging can significantly improve traceability and debugging.
- Fuzz testing is a robust approach to uncover edge cases and unexpected behaviors.
- Continuous integration ensures code quality and reduces manual testing efforts.
- Security tools like Bandit help identify vulnerabilities early in the development process.

### Conclusion
The project demonstrates a practical application of software quality assurance techniques, enabling a systematic approach to improving software reliability and security.
