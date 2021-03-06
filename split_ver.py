import os
import csv
# %matplotlib inline

target_path = "./results/flat_csv/"
files = os.listdir(target_path)

for file in files:
    with open(target_path + file, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        if '9.1.1' in file:
            for row in reader:
                with open("./results/per_version_flat/9.1.1.csv", mode='a') as f:
                    f.write(str(row[0]) +  ', ' + str(row[1]) + "\n")
        elif '9.2.1' in file:
            for row in reader:
                with open("./results/per_version_flat/9.2.1.csv", mode='a') as f:
                    f.write(str(row[0]) +  ', ' + str(row[1]) + "\n")
        elif '9.3.1' in file:
            for row in reader:
                with open("./results/per_version_flat/9.3.1.csv", mode='a') as f:
                    f.write(str(row[0]) +  ', ' + str(row[1]) + "\n")
        elif '9.4.1' in file:
            for row in reader:
                with open("./results/per_version_flat/9.4.1.csv", mode='a') as f:
                    f.write(str(row[0]) +  ', ' + str(row[1]) + "\n")
        elif '9.5.1' in file:
            for row in reader:
                with open("./results/per_version_flat/9.5.1.csv", mode='a') as f:
                    f.write(str(row[0]) +  ', ' + str(row[1]) + "\n")
