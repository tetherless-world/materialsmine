import rdflib
from . import ingest_tester
from . import template

file_under_test = "L254_S35_Castillo_2011"

class IngestTestRunner(template.IngestTestSetup):
    first_run = bool()
    @classmethod
    def setUpClass(cls):
        cls.file_under_test = file_under_test
        super().setUpClass()

    def test_triples(self):
        ingest_tester.print_triples(self)
    
    def test_non_spherical_shape_width(self):
        expected_width_value = rdflib.Literal(10.5, datatype=rdflib.XSD.double)
        ingest_tester.test_non_spherical_shape_width(self, expected_width_value)
