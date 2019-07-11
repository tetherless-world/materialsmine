import rdflib

from . import ingest_tester
from . import test_template

class L101_S3_Dang_2007(test_template.IngestTestSetup):
    @classmethod
    def setUpClass(cls):
        cls.file_under_test = "L101_S3_Dang_2007"
        super().setUpClass()

    def test_specific_surface_area(self):
        expected_surface_area = [rdflib.Literal(9)]
        expected_units = [rdflib.Literal("m^2/g")]
        ingest_tester.test_specific_surface_area(self, expected_surface_area, expected_units)

    def test_print_triples(self):
        ingest_tester.print_triples(self)