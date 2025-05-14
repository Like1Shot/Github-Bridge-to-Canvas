# Bridge to Canvas

This repository contains a template for a course assignment that automatically grades student submissions and sends the results to Canvas using GitHub Actions.

## Project Structure

- `.github/workflows/grade-submission.yml`: GitHub Actions workflow for automated grading
- `CMakeLists.txt`: CMake configuration for building the project
- `canvas_grader.py`: Python script to parse test results and submit grades to Canvas
- `requirements.txt`: Python dependencies for Canvas integration

## How It Works

1. When a student pushes their code to the main branch or creates a pull request:
   - GitHub Actions automatically triggers the grading workflow
   - The workflow builds the project using CMake
   - Runs the test suite
   - Calculates the grade based on passed tests
   - Submits the grade to Canvas

2. The grade is calculated as:
   ```
   grade = (passed_tests / total_tests) * 100
   ```

## For Students

1. Clone this repository
2. Complete your implementation
3. Push your changes to GitHub
4. The grade will be automatically submitted to Canvas

## For Instructors

To set up this system for your course:

1. Add the following secrets to your GitHub repository (Settings > Secrets and variables > Actions):
   - `CANVAS_URL`: Your Canvas instance URL
   - `CANVAS_TOKEN`: Your Canvas API token
   - `COURSE_ID`: The Canvas course ID
   - `ASSIGNMENT_ID`: The Canvas assignment ID
   - `STUDENT_ID`: The student's Canvas ID

2. Make sure your test suite is properly configured in the CMake files

## Local Testing

To test your implementation locally before pushing:

```bash
mkdir build
cd build
cmake ..
make
./run_tests
```

## Notes

- The grading is fully automated through GitHub Actions
- Grades are calculated based on the number of passed tests
- Test results are automatically submitted to Canvas
- Make sure to keep your Canvas API token secure in GitHub Secrets 
