import itertools
import csv

def generate_constructs(sequences, linker, output_file):
    perms = itertools.permutations(sequences)
    constructs = [linker.join(perm) for perm in perms]
    
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        for construct in constructs:
            writer.writerow([construct])
    return output_file
