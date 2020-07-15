import rdflib

from . import ingest_tester, template

file_under_test = "L256_S3_Potschke_2004"

class IngestTestRunner(template.IngestTestSetup):
    first_run = bool()
    @classmethod
    def setUpClass(cls):
        cls.file_under_test = file_under_test
        super().setUpClass()

    def test_triples(self):
         ingest_tester.print_triples(self)
   
    def test_melt_viscosity(self):
         ingest_tester.test_melt_viscosity(self, [rdflib.Literal(1793550.45609)])

    def test_rheological_storage_modulus(self):
        frequencies = [
            0.0101576131764,
            0.0178489915878,
            0.0315958400828,
            0.0567622111742,
            0.101210075602,
            0.180443901289,
            0.319284640329,
            0.569102332683,
            1.02178974301,
            1.78089842968,
            3.19702956241,
            5.73900319689,
            10.2257860201,
            18.3551617749,
            31.9863792464,
            57.412824279,
            100.786626676,
        ]

        shear_storage_modulus = [
            66307.2860753,
            126140.494744,
            232779.499531,
            418822.787095,
            701963.596659,
            1101529.27436,
            1569911.32258,
            2116167.46191,
            2630387.21654,
            3123880.7724,
            3544542.41384,
            3921252.55366,
            4250992.59018,
            4515992.79553,
            4846448.96356,
            5019788.80583,
            5173117.4147,
        ]

        frequencies = [rdflib.Literal(f) for f in frequencies]
        shear_storage_modulus = [rdflib.Literal(s) for s in shear_storage_modulus]

        types = {}
        types["independent"] = "<http://nanomine.org/ns/FrequencyRadPerSec>" 
        types["dependent"] = "<http://nanomine.org/ns/ShearStorageModulusPa>"

        descriptions = {}
        descriptions["measurement_description"] = rdflib.Literal("shear storage modulus (Pa) on frequency (rad per sec) at 170 deg C")
        descriptions["x_description"] = rdflib.Literal("frequency (rad per sec)")
        descriptions["y_description"] = rdflib.Literal("shear storage modulus (Pa)")

        ingest_tester.test_general_profile(self, frequencies, shear_storage_modulus, descriptions, types)