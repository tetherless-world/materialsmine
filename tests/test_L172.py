from . import ingest_tester
from . import test_template

class L172Test(test_template.IngestTestTests):
    @classmethod
    def setUpClass(cls):
        cls.file_under_test = "L172_S18_Huo_2015"
        super().setUpClass()
