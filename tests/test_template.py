from . import ingest_tester
from testcase import WhyisTestCase


class IngestTestSetup(WhyisTestCase):
    @classmethod
    def setUpClass(cls):
        print("Setting Up Class")
        cls.maxDiff = None
        cls.expected_data = ingest_tester.autoparse(cls.file_under_test)

    def setUp(self):
        ingest_tester.setUp(self, self.file_under_test)

class IngestTestTests(IngestTestSetup):  
    def test_nanocomposites(self):
        ingest_tester.test_nanocomposites(self)

    def test_authors(self):
        ingest_tester.test_authors(self, self.expected_data["authors"])

    def test_language(self):
        ingest_tester.test_language(self, self.expected_data["language"])

    def test_keywords(self):
        ingest_tester.test_keywords(self, self.expected_data["keywords"])

    def test_devices(self):
        ingest_tester.test_devices(self, self.expected_data["equipment"])

    def test_volume(self):
        ingest_tester.test_volume(self, self.expected_data["journ_vol"])

    def test_matrix_chemical_names(self):
        ingest_tester.test_matrix_chemical_names(self)

    def test_matrix_trade_names(self):
        ingest_tester.test_matrix_trade_names(self)

    def test_filler_chemical_names(self):
        ingest_tester.test_filler_chemical_names(self)

    def test_filler_trade_names(self):
        ingest_tester.test_filler_trade_names(self)

    def test_temperatures(self):
        ingest_tester.test_temperatures(self)

    def test_abbreviations(self):
        ingest_tester.test_abbreviations(self)

    def test_manufacturers(self):
        ingest_tester.test_manufacturers(self)

    def test_complete_material(self):
        ingest_tester.test_complete_material(self)

    def test_filler_processing(self):
        ingest_tester.test_filler_processing(self)
