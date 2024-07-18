# Software-Development-Home-Assignment


# Candidate Profile Processing

This project processes candidate profiles fetched from a given URL. It extracts relevant information, calculates job gaps, and generates a formatted text output.

## How to Run the Scripts

1. **Ensure you have Python installed**:
   - This script requires Python 3.x.
   - You can download Python from [python.org](https://www.python.org/).

2. **Install necessary libraries**:
   - Run the following command to install the required libraries:
     ```
     pip install requests
     ```

3. **Run the script**:
   - Save the code below to a file named `candidate_profile_processing.py`.
   - Open a terminal or command prompt.
   - Navigate to the directory where `candidate_profile_processing.py` is saved.
   - Run the script using the following command:
     ```
     python candidate_profile_processing.py
     ```

4. **View the output**:
   - The script will generate an output file named `SampleCodeOutput.txt` in the same directory.
   - The script will also print the formatted output to the terminal.

## Assumptions and Design Decisions

- **Date Parsing**:
  - The date format used in the JSON data is `%b/%d/%Y` (e.g., `Jan/01/2020`).
  - The `datetime` module is used for parsing and calculating date differences.

- **Handling Missing Information**:
  - If a candidate's name is not available, `"N/A"` is used as the default name.
  - If any necessary job information (role, start date, end date, location) is missing, that job entry is skipped.

- **Gap Calculation**:
  - Gaps between consecutive jobs are calculated in days.
  - If a gap exists, it is noted in the output as `"Gap in CV for X days"`.

- **Output Generation**:
  - The output is formatted as a string for each candidate, including job details and any gaps.
  - The formatted output is saved to a text file and printed to the terminal.

