import csv

candidates = [
    {"reg_no": "C1", "dob": "2000-01-01", "gate_score": 90, "category": "GEN",
     "choices": [("CSE", 1), ("ECE", 2), ("ME", 3)], "status":'wait','assigned':''},
    {"reg_no": "C2", "dob": "2000-01-02", "gate_score": 80, "category": "OBC",
     "choices": [("ECE", 1), ("CSE", 2), ("ME", 3)], "status":'wait','assigned':''},
    {"reg_no": "C3", "dob": "2000-01-03", "gate_score": 70, "category": "SC",
     "choices": [("ME", 1), ("CSE", 2), ("ECE", 3)], "status":'wait','assigned':''},
    {"reg_no": "C4", "dob": "2000-01-04", "gate_score": 60, "category": "ST",
     "choices": [("ECE", 1), ("ME", 2), ("CSE", 3)], "status":'reject','assigned':''},
    {"reg_no": "C5", "dob": "2000-01-05", "gate_score": 50, "category": "GEN",
     "choices": [("CSE", 1), ("ECE", 2), ("ME", 3)], "status":'wait','assigned':''},
    {"reg_no": "C6", "dob": "2000-01-06", "gate_score": 40, "category": "GEN",
     "choices": [("ME", 1), ("ECE", 2), ("CSE", 3)], "status":'wait','assigned':''},
    {"reg_no": "C7", "dob": "2000-01-07", "gate_score": 30, "category": "OBC",
     "choices": [("CSE", 1), ("ME", 2), ("ECE", 3)], "status":'wait','assigned':''},
    {"reg_no": "C8", "dob": "2000-01-08", "gate_score": 20, "category": "SC",
     "choices": [("ECE", 1), ("CSE", 2), ("ME", 3)], "status":'wait','assigned':''},
    {"reg_no": "C9", "dob": "2000-01-09", "gate_score": 10, "category": "ST",
     "choices": [("ME", 1), ("CSE", 2), ("ECE", 3)], "status":'wait','assigned':''},
    {"reg_no": "C10", "dob": "2000-01-10", "gate_score": 5, "category": "GEN",
     "choices": [("CSE", 1), ("ECE", 2), ("ME", 3)], "status":'wait','assigned':''},
]

# candidates = [
#     {"reg_no": "C1", "dob": "2000-01-01", "gate_score": 90, "category": "GEN",
#      "choices": [("CSE", 1), ("ECE", 2), ("ME", 3)], "status":'wait','assigned':''},
#     {"reg_no": "C2", "dob": "2000-01-02", "gate_score": 80, "category": "OBC",
#      "choices": [("CSE", 1), ("ECE", 2), ("ME", 3)], "status":'wait','assigned':''},
# ]

# candidates = [
#     {"reg_no": "C1", "dob": "2000-01-01", "gate_score": 90, "category": "GEN",
#      "choices": [("CSE", 1), ("ECE", 2), ("ME", 3)], "status":'quit','assigned':''},
#     {"reg_no": "C2", "dob": "2000-01-02", "gate_score": 80, "category": "OBC",
#      "choices": [("ECE", 1), ("CSE", 2), ("ME", 3)], "status":'reject','assigned':'ECE'},
# ]

# define the list of branches with seat matrix
branches = [
    {"name": "CSE", "seats": {"GEN": 2, "OBC": 1, "SC": 1, "ST": 1}, "students": {'GEN':[],'SC':[],'ST':[],'OBC':[]}},
    {"name": "ECE", "seats": {"GEN": 2, "OBC": 1, "SC": 1, "ST": 1}, "students": {'GEN':[],'SC':[],'ST':[],'OBC':[]}},
    {"name": "ME", "seats": {"GEN": 2, "OBC": 1, "SC": 1, "ST": 1}, "students": {'GEN':[],'SC':[],'ST':[],'OBC':[]}},
]

#Removing candidates who have opted out
for i in range(len(candidates)-1,-1,-1):
    if candidates[i]['status'] == 'quit':
        del candidates[i]
    elif candidates[i]['status'] == 'reject':
        for j in candidates[i]["choices"]:
            if j[0] == candidates[i]['assigned']:
                candidates[i]["choices"].remove(j)
                candidates[i]['assigned'] = ''
                candidates[i]['status'] = 'wait'
                break

# sort the candidates based on GATE score, and then date of birth
candidates.sort(key=lambda x: (x['gate_score'], x['dob']), reverse=True)

# loop through the sorted candidates and assign them to their first choice branch, or their next available choice
for candidate in candidates:
    assigned = False
    for choice in candidate['choices']:
        branch_name = choice[0]
        priority = choice[1]
        branch = next((x for x in branches if x['name'] == branch_name), None)
        if branch and (branch['seats'][candidate['category']] > 0 or branch['seats']["GEN"] > 0):
            if branch['seats']["GEN"]>0:
                branch['students']['GEN'].append(candidate)
                branch['seats']['GEN'] -= 1
            else:
                branch['students'][candidate["category"]].append(candidate)
                branch['seats'][candidate['category']] -= 1
            candidate['assigned'] = branch_name
            break
        
# print the list of students for each branch
for branch in branches:
    print(f"{branch['name']} branch:")
    for category in branch['students']:
        print(f"\t{category}:")
        for student in branch['students'][category]:
            print(f"\t\tReg. No.: {student['reg_no']}, GATE Score: {student['gate_score']}")
    print()
