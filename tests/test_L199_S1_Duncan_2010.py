import rdflib

from . import ingest_tester, template

file_under_test = "L199_S1_Duncan_2010"

# TODO Add test for shear loading profile
class Test_L199_S1_Duncan_2010(template.IngestTestSetup):
    @classmethod
    def setUpClass(cls):
        cls.file_under_test = file_under_test
        super().setUpClass()

    def test_triples(self):
        ingest_tester.print_triples(self)