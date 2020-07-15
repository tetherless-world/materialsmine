from . import ingest_tester
from . import template

class L174_S5_Ramanathan_2008(template.IngestTestSetup):
    @classmethod
    def setUpClass(cls):
        cls.file_under_test = "L174_S5_Ramanathan_2008"
        super().setUpClass()

    def test_print_triples(self):
        ingest_tester.print_triples(self)