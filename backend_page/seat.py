import pandas as pd
COLS = ['Name','rank','category','branch']

def seat_counselling(file):
    data = pd.read_csv(file,usecols=COLS)
    sorted_data = data.sort_values(by=['branch','rank'])
    print(sorted_data)
    return sorted_data