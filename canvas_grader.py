#!/usr/bin/env python3

import os
import subprocess
import json
import argparse
from canvasapi import Canvas
import re

def run_tests():
    """Run the CMake tests and return the grade."""
    # Check if we're in GitHub Actions (test results already generated)
    if os.path.exists('build/test_results.txt'):
        with open('build/test_results.txt', 'r') as f:
            test_output = f.read()
    else:
        # Create build directory if it doesn't exist
        if not os.path.exists('build'):
            os.makedirs('build')
        
        # Run CMake and make
        subprocess.run(['cmake', '..'], cwd='build', check=True)
        subprocess.run(['make'], cwd='build', check=True)
        
        # Run the tests and capture output
        result = subprocess.run(['./run_tests'], cwd='build', capture_output=True, text=True)
        test_output = result.stdout
    
    # Parse the test output to get the grade
    passed_tests = len(re.findall(r'\[  PASSED  \]', test_output))
    total_tests = len(re.findall(r'\[  FAILED  \]', test_output)) + passed_tests
    
    if total_tests == 0:
        return 0
    
    grade = (passed_tests / total_tests) * 100
    return grade

def submit_to_canvas(grade, canvas_url, api_token, course_id, assignment_id, student_id):
    """Submit the grade to Canvas."""
    canvas = Canvas(canvas_url, api_token)
    course = canvas.get_course(course_id)
    assignment = course.get_assignment(assignment_id)
    
    # Submit the grade
    assignment.submit({
        'submission_type': 'online_text_entry',
        'body': f'Grade: {grade:.2f}%',
        'user_id': student_id
    })
    
    print(f"Grade {grade:.2f}% submitted to Canvas successfully!")

def main():
    parser = argparse.ArgumentParser(description='Run tests and submit grades to Canvas')
    parser.add_argument('--canvas-url', required=True, help='Canvas API URL')
    parser.add_argument('--api-token', required=True, help='Canvas API token')
    parser.add_argument('--course-id', required=True, help='Canvas course ID')
    parser.add_argument('--assignment-id', required=True, help='Canvas assignment ID')
    parser.add_argument('--student-id', required=True, help='Canvas student ID')
    
    args = parser.parse_args()
    
    try:
        grade = run_tests()
        submit_to_canvas(
            grade,
            args.canvas_url,
            args.api_token,
            args.course_id,
            args.assignment_id,
            args.student_id
        )
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)

if __name__ == '__main__':
    main() 