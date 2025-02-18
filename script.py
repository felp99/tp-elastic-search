import csv

input_file = './input.csv'
output_file = './crime_data.csv'

with open(input_file, 'r', newline='') as infile, open(output_file, 'w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    
    for i, row in enumerate(reader):
        if i < 50000:
            writer.writerow(row)
        else:
            break