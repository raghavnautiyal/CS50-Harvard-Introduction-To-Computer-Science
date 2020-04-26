from sys import argv
from csv import reader, DictReader


if len(argv) < 3 or len(argv) > 3:
    print("usage error, dna.py sequence.txt database.csv")
    exit()


with open(argv[2], "r") as sequences:
    dnareader = reader(sequences)
    for row in dnareader:
        dnalist = row

dna = dnalist[0]

DNA_SEQUENCES = {}

# extract the sequences from the database into a list
with open(argv[1]) as database:
    people = reader(database)
    for row in people:
        dnaSequences = row
        dnaSequences.pop(0)
        break

for item in dnaSequences:
    DNA_SEQUENCES[item] = 1

#iterate through and find repeats
for key in DNA_SEQUENCES:
    l = len(key)
    tempMax = 0
    temp = 0
    for i in range(len(dna)):
        # after having counted a sequence it skips at the end of it to avoid counting again
        while temp > 0:
            temp -= 1
            continue

        # if the segment of dna corresponds to the key and there is a repetition of it we start counting
        if dna[i: i + l] == key:
            while dna[i - l: i] == dna[i: i + l]:
                temp += 1
                i += l

            # it compares the value to the previous longest sequence and if it is longer it overrides it
            if temp > tempMax:
                tempMax = temp

    # store the longest sequences in the dictionary using the correspondent key
    DNA_SEQUENCES[key] += tempMax

with open(argv[1], newline='') as database:
    people = DictReader(database)
    for row in people:
        match = 0
        for dna in DNA_SEQUENCES:
            if DNA_SEQUENCES[dna] == int(row[dna]):
                match += 1
        if match == len(DNA_SEQUENCES):
            print(row['name'])
            exit()

    print("No match")