import csv

def generate_OE_molecule(mol_smiles):
    """
    Generate an oemol with a geometry
    """
    import openeye.oechem as oechem
    import openeye.oeomega as oeomega
    mol = oechem.OEMol()
    oechem.OESmilesToMol(mol, mol_smiles)
    mol.SetTitle("MOL")
    oechem.OEAddExplicitHydrogens(mol)
    oechem.OETriposAtomNames(mol)
    oechem.OETriposBondTypeNames(mol)
    omega = oeomega.OEOmega()
    omega.SetMaxConfs(1)
    omega(mol)
    return mol

class ApprovedOEMolGenerator(object):
    """
    Stores dictionary of approved kinase inhibitors and their
    corresponding SMILES strings.
    """
    def __init__(self):
        self.inhibitor_smiles = dict()
        with open('clinical-kinase-inhibitors.csv', 'r') as csvi:
            inhibitor_reader = csv.reader(csvi)
            for inhibitor in inhibitor_reader:
                self.inhibitor_smiles[inhibitor[0]] = inhibitor[1]

    def generate_molecule(self, inhibitor_name):
        mol_smiles = self.inhibitor_smiles[inhibitor_name]
        return generate_OE_molecule(mol_smiles)

