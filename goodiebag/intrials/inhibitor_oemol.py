from goodiebag import dealers
from goodiebag.dealers import Dealer

class TrialOEMolGenerator(Dealer):
    def __init__(self):
        csv_files = ['trial-kinase-inhibitors.csv']
        super(TrialOEMolGenerator, self).__init__(csv_files)

    def import_csv(self, csv_file, drug_status='trial'):
        super(TrialOEMolGenerator, self).import_csv(csv_file,
                                                       drug_status=drug_status)
