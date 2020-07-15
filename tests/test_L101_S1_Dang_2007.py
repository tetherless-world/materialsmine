from . import ingest_tester
from . import template

class L101_S1_Dang_2007(template.IngestTestSetup):
    @classmethod
    def setUpClass(cls):
        cls.file_under_test = "L101_S1_Dang_2007"
        super().setUpClass()

    def test_print_triples(self):
        ingest_tester.print_triples(self)