import csv

def check_csv(csv_file, user_input):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if user_input in row:
                return True
    return False

csv_file = 'links.csv'  # Replace with your CSV file path
user_input = input("Enter a value to check: ")

if check_csv(csv_file, user_input):
    print("FOUND!")
else:
    print("NOT FOUND!!!! 8==3")