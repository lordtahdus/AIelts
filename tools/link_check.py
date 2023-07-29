import csv

def check_csv(csv_file, user_input):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if user_input in row:
                return True
    return False