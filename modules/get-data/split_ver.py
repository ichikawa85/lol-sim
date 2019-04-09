import os
import csv
# %matplotlib inline

target_path = "./results/gold_csv/"
output_path = "./results/per_version_gold/"
files = os.listdir(target_path)

for file in files:
    with open(target_path + file, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            with open(output_path + "all_patch.csv", mode='a') as f:
                f.write(str(row[0]) +  ', ' + str(row[1]) + ', ' + str(row[2]) + "\n")
            # if '9.1.1' in file:
            #     for row in reader:
            #         with open(output_path + "9.1.1.csv", mode='a') as f:
            #             f.write(str(row[0]) +  ', ' + str(row[1]) + "\n")
            # elif '9.2.1' in file:
            #     for row in reader:
            #         with open(output_path + "9.2.1.csv", mode='a') as f:
            #             f.write(str(row[0]) +  ', ' + str(row[1]) + "\n")
            # elif '9.3.1' in file:
            #     for row in reader:
            #         with open(output_path + "9.3.1.csv", mode='a') as f:
            #             f.write(str(row[0]) +  ', ' + str(row[1]) + "\n")
            # elif '9.4.1' in file:
            #     for row in reader:
            #         with open(output_path + "9.4.1.csv", mode='a') as f:
            #             f.write(str(row[0]) +  ', ' + str(row[1]) + "\n")
            # elif '9.5.1' in file:
            #     for row in reader:
            #         with open(output_path + "9.5.1.csv", mode='a') as f:
            #             f.write(str(row[0]) +  ', ' + str(row[1]) + "\n")
