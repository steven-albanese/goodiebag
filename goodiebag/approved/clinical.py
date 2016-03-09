import csv

def return_smiles(inhibitor_name):
    with open('clinical-kinase-inhibitors.csv','r') as csv1:
        csv1_reader = csv.reader(csv1)
        for inhibitor_line in csv1_reader:
            if inhibitor_name in inhibitor_line:
                return inhibitor_line[1]
    return False
