# import required module
import os
# assign directory
directory = 'supervised_essay'
 
# iterate over files in
# that directory
for filename in os.listdir(directory):
    file = os.path.join(directory, filename)

    # checking if it is a file
    if os.path.isfile(file):
        print(file[17:])
    
    # read file
    with open(file, 'r', encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            if "Overall:" in line:
                band = line[9:].strip()
                print(band)

    # move the supervised_essay to assets with corresponding band
    # os.rename(f'{file}', f'assets/band_{band}/{file[17:]}')

    # move the supervised_essay to assets in unassessed folder
    os.rename(f'{file}', f'assets/unassessed_essays/{file[17:]}')