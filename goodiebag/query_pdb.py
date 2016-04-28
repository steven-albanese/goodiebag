# Implemented by SKA and JB, Chodera Lab
# Last edited: 4/28/16

###############################

# Global Import Statments
import csv
import argparse
from Bio import PDB
import pypdb
import xmltodict
###############################

parser = argparse.ArgumentParser(description="Automated script to search PDB by chemical ID")
parser.add_argument('-l', required=True, dest='lig', help='The ligand that you want all PDBS for')
args = parser.parse_args()

ligand = args.lig

#########################################
# Helper Function
#########################################

def gen_query(search_term):
    params = dict()

    params['queryType'] = 'org.pdb.query.simple.ChemCompIdQuery'
    params['chemCompId'] = search_term

    scan_params = dict()
    scan_params['orgPdbQuery'] = params

    return scan_params


# Load up clinical-kinase-inhibitors.csv

filename = 'approved/clinical-kinase-inhibitors.csv'

reader = csv.DictReader(open(filename))

inhibitor_dict = {}

for row in reader:
    for column, value in row.items():
        inhibitor_dict.setdefault(column, []).append(value)

# Create query and do search
pdb_list = []
chem_ids = inhibitor_dict['Chem_ID'][inhibitor_dict['inhibitor'].index(ligand)]
chem_id_list = chem_ids.split()

if chem_id_list ==0:
    print('Missing ChemID for %s' % ligand)

for id in chem_id_list:
    print(id)
    query = gen_query(id)
    found_pdb = pypdb.do_search(query)
    if len(found_pdb) > 0:
        print('found %s PDBS for %s' % (len(found_pdb), id))
        for pdb in found_pdb:
            pdb_list.append(pdb)
    else:
        print('found %s PDBS for %s. Check the CSV file for a mistake' % (len(found_pdb), id))

if len(pdb_list) > 0:
    for structure in pdb_list:
        dir = structure[1:3]
        pdb1 = PDB.PDBList()
        parser = PDB.PDBParser(PERMISSIVE=1)
        struc = parser.get_structure(structure, "%s/pdb%s.ent" % (dir, structure))
        io = PDB.PDBIO()
        io.set_structure(struc)
        io.save('%s.pdb' % structure)


print(pdb_list)

