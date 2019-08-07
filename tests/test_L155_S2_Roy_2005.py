from . import ingest_tester
from . import template
import rdflib

file_under_test = "L155_S2_Roy_2005"

class IngestTestRunner(template.IngestTestSetup):
    first_run = bool()
    @classmethod
    def setUpClass(cls):
        cls.file_under_test = file_under_test
        super().setUpClass()

    def test_triples(self):
         ingest_tester.print_triples(self)

    def test_dielectric_real_permittivity(self):
        frequency = [
            0.002078949,
            0.005239995,
            0.013207416,
            0.033289313,
            0.082305244,
            0.203493333,
            0.512905286,
            1.292778627,
            3.258450684,
            7.902591204,
            20.30583336,
            50.20459806,
            126.540773,
            318.9462293,
            773.5276395,
            1949.677704,
            4914.165902,
            12386.16334,
            30623.82819,
            78688.41195,
            190839.8845,
            481012.2468,
        ]

        real_permittivity = [
            3.21,
            2.88,
            2.595,
            2.385,
            2.2425,
            2.175,
            2.1,
            2.055,
            2.025,
            2.01,
            1.995,
            1.965,
            1.95,
            1.95,
            1.95,
            1.935,
            1.9275,
            1.935,
            1.9275,
            1.92,
            1.92,
            1.905,
        ]
        frequency = [rdflib.Literal(f) for f in frequency]
        real_permittivity = [rdflib.Literal(p) for p in real_permittivity]

        descriptions = {}
        descriptions["measurement_description"] = rdflib.Literal("Measured at 25 Celsius")
        descriptions["x_description"] = rdflib.Literal("Frequency (Hz)")
        descriptions["y_description"] = rdflib.Literal("Real Part of Dielectric Permittivity")

        ingest_tester.test_dielectric_real_permittivity(self, frequency, real_permittivity, descriptions)