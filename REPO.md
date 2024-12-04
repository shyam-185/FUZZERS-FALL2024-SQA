
## REPO.md

### Project Overview
The goal of this project was to piece together all of skills that we have learned through this semester's SQA workshops. Through the use of git hook, fuzzing, forensic logging, and continuous integration, our team was able to esnure that we can implement, test, and find errors within a set of code.

### Team Information
Team Members: Shyam Patel - sjp0059
              Jacob Simmons - jss0112@auburn.edu
              Dayton Malone - ddm0027@auburn.edu
              Jeffery Turnipseed - jzt0059@auburn.edu

### Activities

#### 4.a. Git Hook
- A Git Hook was created to automatically scan for security weaknesses in the project whenever a Python file is modified and committed.

#### 4.b. Fuzzing
- The `fuzz.py` script was implemented to test five methods of our choosing which are:
Method 1 - getFileLength from: /MLForensics-farzana/empirical/dataset.stats.py
Method 2 getGeneralStats from: /MLForensics-farzana/empirical/dataset.stats.py
Method 3 - dumpContentIntoFile from: MLForensics-farzana/mining/git.repo.miner.py
Method 4 - getPythonCount from: MLForensics-farzana/mining/git.repo.miner.py
Method 5 - giveTimeStamp from: MLForensics-farzana/FAME-ML/main.py

For each method 3-5 test cases were created for fuzzing, common tests were None value or empty strings.

#### 4.c. Forensic Logging
- Forensic logging was added to five methods:
  1. `giveTimeStamp` in `main.py` logs the execution of the timestamp function.
  2. `getDataLoadCount` in `lint_engine.py` logs file analysis activities.
  3. `checkLoggingPerData` in `py_parser.py` logs checks for data-related logging.
  4. Additional methods were identified and modified for meaningful forensic logs.
  5. Logging follows Python’s `logging` module for standardization and ease of use.

The outupt was saved in fuzzers.log which state each method, time, output, exception error, input, etc.

#### 4.d. Continuous Integration
- A GitHub Actions pipeline was implemented to scan all of the code for bugs and security weaknesses.

### Lessons Learned
- Integrating forensic logging can significantly improve traceability and debugging efforts.
- Fuzz testing is a great approach to find bugs and unexpected problems throughout the coding process.
- Continuous integration ensures code quality and reduces the time that manual testing would take.

### Conclusion
This project demonstrates a practical application of software quality assurance techniques, allowing us to work together as a team to ensure that our final product picked up as many bugs and security flaws as possible.
