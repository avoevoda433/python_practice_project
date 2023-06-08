import csv

with open('posts.csv', newline='', encoding='utf-8') as File:
    reader = csv.reader(File)
    for row in reader:
        print(row)
