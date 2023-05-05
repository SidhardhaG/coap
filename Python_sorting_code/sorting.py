import numpy as np
import pandas as pd
from collections import deque


coap_file_name = ''
seat_matrix_file_name = ''

students_data = pd.read_csv(coap_file_name)
seat_matrix = pd.read_csv(seat_matrix_file_name, index_col=0)

columns = ['applicant_id', 'coap_id', 'full_name', 'category', 'date_of_birth', 'disable_status', 'gender', 'gate_score', 'priority_1', 'priority_2', 'priority_3']

# Create a nested dictionary for the allocated students
allocated_students = {}

queue = deque(students_data[columns].values)

# Iterate over the students in the queue
while queue:
    student = queue.popleft()  # Get the next student from the queue
    allocated = False  # Flag to track if the student has been allocated

    # Iterate over the branches in the seat matrix
    for branch in seat_matrix.index:                                    # have to add the and priority check
        category = student['category']
        branch_capacity = seat_matrix.loc[branch, category]

        # Check if the branch has capacity for the category
        if branch_capacity > 0:
            # Reduce the capacity of the branch by 1
            seat_matrix.loc[branch, category] -= 1

            # Allocate the student to the branch
            if branch not in allocated_students:
                allocated_students[branch] = {}
            if category not in allocated_students[branch]:
                allocated_students[branch][category] = []
            allocated_students[branch][category].append(student)

            allocated = True
            break  # Exit the loop once allocated to a branch

    if not allocated:
        # Compare the student with the existing students in the branch
        branch = student['priority_1']                                                              # Branches should be looped wwith all the priorities
        category = student['category']                                                              # All the eligible categories should be considered
        if branch in allocated_students and category in allocated_students[branch]:
            existing_students = allocated_students[branch][category]
            
            # Compare the gate score of the student with existing students
            for i, existing_student in enumerate(existing_students):
                if student['gate_score'] > existing_student['gate_score']:
                    # Swap the student with the existing student
                    existing_students[i] = student
                    
                    # Add the existing student back to the queue
                    queue.append(existing_student)
                    
                    # Add the updated student to the allocated_students dictionary
                    allocated_students[branch][category].append(student)
                    
                    break  # Exit the loop once swapped
                    
                elif student['gate_score'] == existing_student['gate_score']:
                    # Compare the date of birth of the student and existing student
                    if student['date_of_birth'] < existing_student['date_of_birth']:
                        # Swap the student with the existing student
                         existing_students[i] = student
                    
                    # Add the existing student back to the queue
                    queue.append(existing_student)
                    
                    # Add the updated student to the allocated_students dictionary
                    allocated_students[branch][category].append(student)

                    break  # Exit the loop once swapped