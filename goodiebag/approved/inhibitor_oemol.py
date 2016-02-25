from goodiebag import dealers
from goodiebag.dealers import Dealer

class ApprovedOEMolGenerator(Dealer):
    def __init__(self):
        csv_files = ['clinical-kinase-inhibitors.csv']
        super(ApprovedOEMolGenerator, self).__init__(csv_files)

    def import_csv(self, csv_file, drug_status='approved'):
        super(ApprovedOEMolGenerator, self).import_csv(csv_file,
                                                       drug_status=drug_status)
