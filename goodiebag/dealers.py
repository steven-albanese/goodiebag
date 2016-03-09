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

def generate_OE_molecule_from_name(inhibitor_name):
    from approved import clinical
    from intrials import trial
    smiles = clinical.return_smiles(inhibitor_name)
    if not smiles:
        smiles = trial.return_smiles(inhibitor_name)
    if not smiles:
        return EOFError('Inhibitor name %s was not recognized' % inhibitor_name)
    return generate_OE_molecule(smiles)

class Dealer(object):
    """
    Stores dictionary of approved kinase inhibitors and their
    corresponding SMILES strings.

    Arguments:
    ----------
        csv_files : list of filenames
    """
    def __init__(self, csv_files):
        self._inhibitors = dict()
        self._kinases = dict()
        for csv_file in csv_files:
            self.import_csv(csv_file)

    def generate_molecule(self, drug_name):
        if drug_name not in self.inhibitor_names:
            raise KeyError('Inhibitor called %s is not recognized' % drug_name)
        mol_smiles = self.inhibitor_smiles[drug_name]
        return generate_OE_molecule(mol_smiles)

    def generate_kinase_xml(self):
        from lxml import etree
        pass

    def import_csv(self, csv_file, drug_status=None):
        with open(csv_file, 'r') as csvi:
            inhibitor_reader = csv.reader(csvi)
            for inhibitor_line in inhibitor_reader:
                drug_name = inhibitor_line[0]
                smiles = inhibitor_line[1]
                kinase_list = inhibitor_line[2].split(' ')
                self.add_inhibitor(drug_name, smiles, kinase_list,
                                   drug_status=drug_status)

    def add_inhibitor(self, drug_name, smiles, kinase_list, drug_status=None):
        inhibitor = Inhibitor(drug_name, smiles, kinase_list, self,
                              drug_status=drug_status)
        self.inhibitors[inhibitor.name] = inhibitor

    def add_kinase(self, kinase_name):
        kinase = Kinase(kinase_name, self)
        self._kinases[kinase.name] = kinase

    @property
    def kinase_names(self):
        return self._kinases.keys()

    @property
    def kinases(self):
        return self._kinases.values()

    @property
    def kinase_by_name(self, name):
        return self._kinases[name]

    @property
    def inhibitor_names(self):
        return self._inhibitors.keys()

    @property
    def inhibitors(self):
        return self._inhibitors.values()

    @property
    def inhibitor_by_name(self, name):
        return self._inhibitors[name]

    @property
    def inhibitor_smiles(self, name):
        return self._inhibitors[name].smiles

class AllKnownOEMolGenerator(Dealer):
    def __init__(self):
        from approved import clinical-kinase-inhibitors.csv
        from intrials import trial-kinase-inhibitors.csv
        csv_files = ['clinical-kinase-inhibitors.csv',
                     'trial-kinase-inhibitors.csv']
        self._csv_files = csv_files
        super(AllKnownOEMolGenerator, self).__init__(csv_files)

    def import_csv(self, csv_file, drug_status=None):
        if csv_file = self._csv_files[0]:
            drug_status = 'approved'
        elif csv_file = self._csv_files[1]:
            drug_status = 'trial'
        super(AllKnownOEMolGenerator, self).import_csv(csv_file,
                                                       drug_status=drug_status)

class Inhibitor(object):
    """
    Arguments:
    ----------
        name : string
        smiles : string
        kinase_names : list of strings
        dealer : ApprovedOEMolGenerator
        status : 'approved' or 'trial' or None (default)
    """
    def __init__(self, name, smiles, kinase_names, dealer, status=None):
        self.name = name
        self.smiles = smiles
        self.dealer = dealer
        self.status = status
        self.kinases = list()
        for kinase_name in kinase_names:
            if kinase_name in dealer.kinase_names:
                kinase = dealer.kinase_by_name(kinase_name)
            else:
                kinase = dealer.add_kinase(kinase_name)
            self.kinases.append(kinase)
            kinase.add_inhibitor(self)

    def generate_molecule(self):
        return self.dealer.generate_molecule(self.name)

    @property
    def kinase_names(self):
        return [kinase.name for kinase in self.kinases]

class Kinase(object):
    """
    Arguments:
    ----------
        name : string
        dealer : ApprovedOEMolGenerator
    """
    def __init__(self, name, dealer):
        self.name = name
        self.inhibitors = list()
        self.dealer = dealer

    def add_inhibitor(self, inhibitor):
        self.inhibitors.append(inhibitor)

    @property
    def inhibitor_names(self):
        return [inhibitor.name for inhibitor in self.inhibitors]














