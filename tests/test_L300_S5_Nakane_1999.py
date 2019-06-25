from . import ingest_tester
from . import test_template
import rdflib

class L300_S5_Nakane_1999(test_template.IngestTestSetup):
    @classmethod
    def setUpClass(cls):
        cls.file_under_test = "L300_S5_Nakane_1999"
        super().setUpClass()

    def test_viscoelastic_measurement_mode(self):
        expected_properties = ["tensile"]
        ingest_tester.test_viscoelastic_measurement_mode(self, expected_properties)
        ingest_tester.test_viscoelastic_measurement_mode(self)


