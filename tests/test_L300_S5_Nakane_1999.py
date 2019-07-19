from . import ingest_tester
from . import template
import rdflib

class L300_S5_Nakane_1999(template.IngestTestSetup):
    @classmethod
    def setUpClass(cls):
        cls.file_under_test = "L300_S5_Nakane_1999"
        super().setUpClass()

    def test_viscoelastic_measurement_mode(self):
        expected_properties = ["tensile"]
        ingest_tester.test_viscoelastic_measurement_mode(self, expected_properties)
        ingest_tester.test_viscoelastic_measurement_mode(self)

    def test_stress(self):
        ingest_tester.test_stress(self, [rdflib.Literal(0.0792094406024)])
    
    # def test_triples(self):
    #     ingest_tester.print_triples(self)
